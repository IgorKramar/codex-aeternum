package ru.kramar.codex.book;

import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.packs.resources.Resource;
import net.minecraft.server.packs.resources.ResourceManager;
import net.minecraft.server.packs.resources.ResourceManagerReloadListener;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.BufferedReader;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Содержимое книги. На клиенте читается из assets/codex/book (запасной
 * вариант без мода на сервере), на сервере — из data/codex/book и затем
 * рассылается игрокам. Два экземпляра нужны из-за встроенного сервера,
 * живущего в одном процессе с клиентом.
 */
public final class Book {

    private static final Logger LOG = LoggerFactory.getLogger("codex");
    public static final Book CLIENT = new Book("клиент");
    public static final Book REMOTE = new Book("книга сервера на клиенте");
    public static final Book SERVER = new Book("сервер");

    private final String side;
    private final Map<String, Section> sections = new LinkedHashMap<>();
    private final Map<String, Chapter> chapters = new LinkedHashMap<>();
    private final List<Chapter> ordered = new ArrayList<>();
    private List<Chapter> displayMaps = List.of();
    private List<Chapter> orderedView = List.of();
    private Map<String, List<Quest>> successors = Map.of();
    /** Сырые JSON-документы для пересылки клиентам. */
    private final List<String> rawDocuments = new ArrayList<>();
    private String rawSections = "{}";

    private Book(String side) {
        this.side = side;
    }

    /** Слушатель перезагрузки ресурсов для клиента или сервера. */
    public ResourceManagerReloadListener listener() {
        return rm -> loadFrom(rm);
    }

    public synchronized void loadFrom(ResourceManager rm) {
        try {
            ResourceLocation sectionsFile = ResourceLocation.fromNamespaceAndPath("codex", "book/sections.json");
            String sectionsText = "{}";
            var resource = rm.getResource(sectionsFile);
            if (resource.isPresent()) try (BufferedReader r = resource.get().openAsReader()) {
                sectionsText = readAll(r);
            }
            Map<ResourceLocation, Resource> files = rm.listResources("book/chapters", loc -> loc.getPath().endsWith(".json"));
            List<ResourceLocation> keys = new ArrayList<>(files.keySet());
            keys.sort(Comparator.comparing(ResourceLocation::toString));
            List<String> docs = new ArrayList<>();
            for (ResourceLocation key : keys) {
                if (!"codex".equals(key.getNamespace())) continue;
                try (BufferedReader r = files.get(key).openAsReader()) { docs.add(readAll(r)); }
            }
            loadFromDocuments(sectionsText, docs);
        } catch (Exception ex) {
            LOG.error("Кодекс ({}): новая книга отклонена, предыдущая сохранена", side, ex);
            throw new IllegalArgumentException("Не удалось загрузить книгу", ex);
        }
    }

    /** Проверяем весь набор до публикации: ошибочный датапак не уничтожает рабочую книгу. */
    public synchronized void loadFromDocuments(String sectionsJson, List<String> chapterJsons) {
        Book next = new Book(side);
        next.rawSections = sectionsJson;
        next.parseSections(sectionsJson);
        for (String doc : chapterJsons) {
            next.parseChapters(doc);
            next.rawDocuments.add(doc);
        }
        next.validate();
        next.finish();
        clear();
        sections.putAll(next.sections);
        chapters.putAll(next.chapters);
        ordered.addAll(next.ordered);
        displayMaps = next.displayMaps;
        orderedView = next.orderedView;
        successors = next.successors;
        rawSections = next.rawSections;
        rawDocuments.addAll(next.rawDocuments);
    }

    private void validate() {
        for (Chapter c : chapters.values()) {
            requireId(c.id);
            requireId(c.mapId);
            if (!sections.containsKey(c.sectionId)) throw new IllegalArgumentException("Нет раздела: " + c.sectionId);
            for (Quest q : c.quests) {
                requireId(q.id);
                if (q.reward.xp < 0) throw new IllegalArgumentException("Отрицательный опыт: " + q.globalId());
                for (Reward.Stack stack : q.reward.items)
                    if (stack.count() <= 0 || ResourceLocation.tryParse(stack.id()) == null)
                        throw new IllegalArgumentException("Неверная награда: " + q.globalId());
                ru.kramar.codex.progress.Rules.consumedItems(q); // проверка переполнения суммы
            }
        }
        Map<String, Integer> colors = new java.util.HashMap<>();
        for (Chapter c : chapters.values()) for (Quest q : c.quests) visit(q, colors);
    }

    private static void requireId(String id) {
        if (!id.matches("[a-zA-Z0-9_.-]+")) throw new IllegalArgumentException("Неверный ID: " + id);
    }

    private void visit(Quest q, Map<String, Integer> colors) {
        int color = colors.getOrDefault(q.globalId(), 0);
        if (color == 2) return;
        if (color == 1) throw new IllegalArgumentException("Цикл зависимостей: " + q.globalId());
        colors.put(q.globalId(), 1);
        List<String> dependencies = new ArrayList<>(q.deps);
        dependencies.addAll(q.anyDeps);
        for (String dep : dependencies) {
            String id = dep.contains("/") ? dep : q.chapterId + "/" + dep;
            Quest target = quest(id);
            if (target == null) throw new IllegalArgumentException(q.globalId() + ": нет зависимости " + id);
            visit(target, colors);
        }
        colors.put(q.globalId(), 2);
    }

    private void clear() {
        sections.clear();
        chapters.clear();
        ordered.clear();
        displayMaps = List.of();
        rawDocuments.clear();
    }

    private void parseSections(String text) {
        JsonObject root = JsonParser.parseString(text).getAsJsonObject();
        for (Map.Entry<String, JsonElement> e : root.entrySet()) {
            Section s = Section.parse(e.getKey(), e.getValue().getAsJsonObject());
            sections.put(s.id, s);
        }
    }

    private void parseChapters(String text) {
        JsonElement parsed = JsonParser.parseString(text);
        if (parsed.isJsonArray()) {
            for (JsonElement c : (JsonArray) parsed) addChapter(Chapter.parse(c.getAsJsonObject()));
        } else {
            addChapter(Chapter.parse(parsed.getAsJsonObject()));
        }
    }

    private void finish() {
        ordered.addAll(chapters.values());
        ordered.sort(Comparator
                .comparingInt((Chapter c) -> sectionOrder(c.sectionId))
                .thenComparingInt(c -> c.order)
                .thenComparing(c -> c.id));
        displayMaps = buildMaps();
        orderedView = List.copyOf(ordered);
        Map<String, List<Quest>> reverse = new LinkedHashMap<>();
        for (Chapter c : ordered) for (Quest q : c.quests) {
            List<String> deps = new ArrayList<>(q.deps);
            deps.addAll(q.anyDeps);
            for (String dep : deps) {
                String gid = dep.contains("/") ? dep : q.chapterId + "/" + dep;
                List<Quest> children = reverse.computeIfAbsent(gid, key -> new ArrayList<>());
                if (!children.contains(q)) children.add(q);
            }
        }
        reverse.replaceAll((id, children) -> List.copyOf(children));
        successors = Map.copyOf(reverse);
        LOG.info("Кодекс ({}): загружено разделов — {}, глав — {}, заданий — {}",
                side, sections.size(), chapters.size(), totalQuests());
    }

    private static String readAll(BufferedReader r) throws java.io.IOException {
        StringBuilder sb = new StringBuilder();
        char[] buf = new char[8192];
        int n;
        while ((n = r.read(buf)) > 0) sb.append(buf, 0, n);
        return sb.toString();
    }

    private void addChapter(Chapter c) {
        if (chapters.putIfAbsent(c.id, c) != null)
            throw new IllegalArgumentException("Глава объявлена дважды: " + c.id);
    }

    private int sectionOrder(String id) {
        Section s = sections.get(id);
        return s == null ? 10_000 : s.order;
    }

    public synchronized Section section(String id) {
        return sections.get(id);
    }

    public synchronized Chapter chapter(String id) {
        return chapters.get(id);
    }

    public synchronized Quest quest(String globalId) {
        int slash = globalId.indexOf('/');
        if (slash < 0) return null;
        Chapter c = chapters.get(globalId.substring(0, slash));
        return c == null ? null : c.byId.get(globalId.substring(slash + 1));
    }

    public synchronized List<Chapter> chapters() {
        return orderedView;
    }

    private List<Chapter> buildMaps() {
        Map<String, List<Quest>> grouped = new LinkedHashMap<>();
        Map<String, Chapter> first = new LinkedHashMap<>();
        for (Chapter c : ordered) {
            grouped.computeIfAbsent(c.mapId, key -> new ArrayList<>()).addAll(c.quests);
            first.putIfAbsent(c.mapId, c);
        }
        List<Chapter> result = new ArrayList<>();
        grouped.forEach((id, quests) -> {
            Chapter source = first.get(id);
            result.add(id.equals(source.id) && quests.size() == source.quests.size()
                    ? source : Chapter.displayMap(id, source, sections.get(id), quests));
        });
        return List.copyOf(result);
    }

    public synchronized List<Quest> successors(Quest q) {
        return successors.getOrDefault(q.globalId(), List.of());
    }

    public synchronized List<Chapter> maps() { return displayMaps; }

    public synchronized Chapter map(String id) {
        for (Chapter c : maps()) if (c.id.equals(id)) return c;
        return null;
    }

    public synchronized List<Section> sections() {
        List<Section> out = new ArrayList<>(sections.values());
        out.sort(Comparator.comparingInt((Section s) -> s.order).thenComparing(s -> s.id));
        return out;
    }

    public synchronized int totalQuests() {
        int n = 0;
        for (Chapter c : ordered) n += c.quests.size();
        return n;
    }

    public synchronized boolean isEmpty() {
        return ordered.isEmpty();
    }

    public synchronized String rawSections() {
        return rawSections;
    }

    public synchronized List<String> rawDocuments() {
        return List.copyOf(rawDocuments);
    }
}
