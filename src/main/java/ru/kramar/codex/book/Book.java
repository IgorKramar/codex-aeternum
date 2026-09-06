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
    public static final Book SERVER = new Book("сервер");

    private final String side;
    private final Map<String, Section> sections = new LinkedHashMap<>();
    private final Map<String, Chapter> chapters = new LinkedHashMap<>();
    private final List<Chapter> ordered = new ArrayList<>();
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
        clear();
        ResourceLocation sectionsFile = ResourceLocation.fromNamespaceAndPath("codex", "book/sections.json");
        for (Resource res : rm.getResourceStack(sectionsFile)) {
            try (BufferedReader r = res.openAsReader()) {
                String text = readAll(r);
                rawSections = text;
                parseSections(text);
            } catch (Exception ex) {
                LOG.error("Кодекс ({}): не удалось прочитать sections.json", side, ex);
            }
        }
        Map<ResourceLocation, Resource> files =
                rm.listResources("book/chapters", loc -> loc.getPath().endsWith(".json"));
        List<ResourceLocation> keys = new ArrayList<>(files.keySet());
        keys.sort(Comparator.comparing(ResourceLocation::toString));
        for (ResourceLocation key : keys) {
            if (!"codex".equals(key.getNamespace())) continue;
            try (BufferedReader r = files.get(key).openAsReader()) {
                String text = readAll(r);
                rawDocuments.add(text);
                parseChapters(text);
            } catch (Exception ex) {
                LOG.error("Кодекс ({}): ошибка в файле главы {}", side, key, ex);
            }
        }
        finish();
    }

    /** Загрузка из документов, присланных сервером. */
    public synchronized void loadFromDocuments(String sectionsJson, List<String> chapterJsons) {
        clear();
        rawSections = sectionsJson;
        try {
            parseSections(sectionsJson);
        } catch (Exception ex) {
            LOG.error("Кодекс ({}): разделы от сервера не разобраны", side, ex);
        }
        for (String doc : chapterJsons) {
            rawDocuments.add(doc);
            try {
                parseChapters(doc);
            } catch (Exception ex) {
                LOG.error("Кодекс ({}): глава от сервера не разобрана", side, ex);
            }
        }
        finish();
    }

    private void clear() {
        sections.clear();
        chapters.clear();
        ordered.clear();
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
        if (chapters.containsKey(c.id)) {
            LOG.warn("Кодекс ({}): глава {} объявлена дважды, берётся последняя", side, c.id);
        }
        chapters.put(c.id, c);
    }

    private int sectionOrder(String id) {
        Section s = sections.get(id);
        return s == null ? 10_000 : s.order;
    }

    public Section section(String id) {
        return sections.get(id);
    }

    public Chapter chapter(String id) {
        return chapters.get(id);
    }

    public Quest quest(String globalId) {
        int slash = globalId.indexOf('/');
        if (slash < 0) return null;
        Chapter c = chapters.get(globalId.substring(0, slash));
        return c == null ? null : c.byId.get(globalId.substring(slash + 1));
    }

    public List<Chapter> chapters() {
        return ordered;
    }

    public List<Section> sections() {
        List<Section> out = new ArrayList<>(sections.values());
        out.sort(Comparator.comparingInt((Section s) -> s.order).thenComparing(s -> s.id));
        return out;
    }

    public int totalQuests() {
        int n = 0;
        for (Chapter c : ordered) n += c.quests.size();
        return n;
    }

    public boolean isEmpty() {
        return ordered.isEmpty();
    }

    public String rawSections() {
        return rawSections;
    }

    public List<String> rawDocuments() {
        return List.copyOf(rawDocuments);
    }
}
