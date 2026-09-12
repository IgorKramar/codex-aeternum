package ru.kramar.codex;

import com.google.gson.JsonParser;
import ru.kramar.codex.book.Book;
import ru.kramar.codex.book.Quest;
import ru.kramar.codex.progress.Progress;
import ru.kramar.codex.progress.Rules;
import ru.kramar.codex.progress.Tracker;
import ru.kramar.codex.net.Payloads;

import java.nio.file.Files;
import java.util.List;

/** Зависит только от модели, файловой системы и библиотек игры; без игрового процесса. */
public final class RuntimeRegression {
    private static final String SECTIONS = "{\"s\":{\"title\":\"Этап\"}}";

    public static void main(String[] args) throws Exception {
        alternativesAndMaps();
        legacyChapterMaps();
        longReverseChain();
        rejectedReloadRetainsBook();
        aggregateConsumption();
        snapshotsAndRecovery();
        networkBoundsAndLocalProgress();
        bundledBook();
        System.out.println("Runtime regression: 8 сценариев пройдены");
    }

    private static void alternativesAndMaps() {
        Book book = Book.CLIENT;
        book.loadFromDocuments(SECTIONS, List.of(mappedChapter("a", """
                {"id":"base","title":"Base"},
                {"id":"left","title":"Left"},
                {"id":"right","title":"Right"},
                {"id":"end","title":"End","deps":["base"],"any_deps":["left","right"]}
                """), mappedChapter("b", "{\"id\":\"base\",\"title\":\"Other base\"}")));
        Progress p = new Progress();
        Quest end = book.quest("a/end");
        p.completed.add("a/left");
        check(!Rules.unlocked(book, p, end), "ANY не заменяет обязательный ALL");
        p.completed.add("a/base");
        check(Rules.unlocked(book, p, end), "Достаточно одной альтернативы");
        p.completed.remove("a/left");
        check(!Rules.unlocked(book, p, end), "Пустой ANY блокирует задание");
        check(book.maps().size() == 1 && book.map("s").quests.size() == 5, "Главы объединяются в карту");
        check(book.map("s").title.equals("Этап"), "Общая карта использует название раздела");
        check(book.map("s").quests.getFirst() == book.quest("a/base"), "Карта сохраняет объекты и globalId");
        check(book.chapters().size() == 2, "Канонические главы сохраняются");
        check(Rules.validFlag(book, "a/base") && !Rules.validFlag(book, "invented"), "Проверка ручных ключей");
    }

    private static void legacyChapterMaps() {
        Book book = Book.CLIENT;
        book.loadFromDocuments(SECTIONS, List.of("""
                [{"id":"s","section":"s","title":"Первая глава","quests":[
                    {"id":"start","title":"Start","x":0,"y":0}]},
                 {"id":"second","section":"s","title":"Вторая глава","quests":[
                    {"id":"start","title":"Start","x":0,"y":0}]}]
                """));
        check(book.maps().size() == 2, "Старые главы с локальными координатами остаются отдельными картами");
        check(book.map("s") == book.chapter("s") && book.map("second") == book.chapter("second"),
                "Отдельные карты сохраняют канонические главы");
        check(book.map("s").title.equals("Первая глава") && book.map("second").title.equals("Вторая глава"),
                "Название раздела не заменяет названия старых глав");
    }

    private static void longReverseChain() {
        StringBuilder quests = new StringBuilder();
        Progress p = new Progress();
        for (int i = 79; i >= 0; i--) {
            if (!quests.isEmpty()) quests.append(',');
            quests.append("{\"id\":\"q").append(i).append("\",\"title\":\"Q\"");
            if (i > 0) quests.append(",\"deps\":[\"q").append(i - 1).append("\"]");
            quests.append('}');
            p.manual.add("a/q" + i);
        }
        Book.CLIENT.loadFromDocuments(SECTIONS, List.of(chapter("a", quests.toString())));
        check(Rules.recompute(Book.CLIENT, p).size() == 80, "Нет потолка 32 прохода");
        check(Rules.recompute(Book.CLIENT, p).isEmpty(), "Повторный пересчёт идемпотентен");
    }

    private static void rejectedReloadRetainsBook() {
        Book book = Book.CLIENT;
        String original = chapter("a", "{\"id\":\"safe\",\"title\":\"Safe\"}");
        book.loadFromDocuments(SECTIONS, List.of(original));
        for (String invalid : List.of(
                "{\"id\":\"x\",\"title\":\"X\",\"deps\":[\"missing\"]}",
                "{\"id\":\"x\",\"title\":\"X\",\"any_deps\":[\"x\"]}",
                "{\"id\":\"x\",\"title\":\"X\"},{\"id\":\"x\",\"title\":\"X\"}",
                "{\"id\":\"x\",\"title\":\"X\",\"tasks\":[{\"type\":\"typo\"}]}",
                "{\"id\":\"x\",\"title\":\"X\",\"tasks\":[{\"type\":\"check\",\"count\":0}]}")) {
            rejects(() -> book.loadFromDocuments(SECTIONS, List.of(chapter("a", invalid))));
            check(book.quest("a/safe") != null && book.rawDocuments().equals(List.of(original)), "Ошибка не меняет опубликованную книгу");
        }
        check(Book.REMOTE != Book.CLIENT && Book.SERVER != Book.CLIENT, "Изоляция источников книги");
    }

    private static void aggregateConsumption() {
        Quest quest = Quest.parse("a", JsonParser.parseString("""
                {"id":"pay","title":"Pay","tasks":[
                  {"id":"minecraft:stone","count":3,"consume":true},
                  {"id":"minecraft:stone","count":4,"consume":true}]}
                """).getAsJsonObject());
        Progress p = new Progress();
        p.itemsNow.put("minecraft:stone", 4);
        check(!Rules.tasksDone(p, quest), "Повторные требования складываются");
        p.itemsNow.put("minecraft:stone", 7);
        check(Rules.tasksDone(p, quest), "Полный платёж доступен");
    }

    private static void snapshotsAndRecovery() throws Exception {
        var directory = Files.createTempDirectory("codex-progress-test");
        var file = directory.resolve("player.json");
        try {
            Progress p = new Progress();
            p.bind(file);
            p.recordItem("minecraft:stone", 12);
            p.itemsNow.put("minecraft:stone", 3);
            check(!p.toJson().has("itemsNow"), "Текущий инвентарь не сохраняется на диск");
            Progress client = new Progress();
            client.fromJson(p.snapshot());
            check(client.now("minecraft:stone") == 3 && client.seen("minecraft:stone") == 12, "Сетевой снимок содержит текущий инвентарь");
            p.itemsNow.clear();
            client.fromJson(p.snapshot());
            check(client.now("minecraft:stone") == 0, "Уменьшение инвентаря до нуля синхронизируется");
            p.saveNow();
            p.completed.add("a/safe");
            p.markDirty();
            p.saveNow();
            Files.writeString(file, "{broken");
            Progress recovered = new Progress();
            recovered.bind(file);
            check(recovered.seen("minecraft:stone") == 12, "Резервная копия восстанавливается");
            try (var paths = Files.list(directory)) {
                check(paths.anyMatch(path -> path.getFileName().toString().contains(".corrupt-")), "Повреждённый файл сохранён отдельно");
            }
            rejects(() -> recovered.fromJson(JsonParser.parseString("{\"items\":[],\"completed\":42}").getAsJsonObject()));
            check(recovered.seen("minecraft:stone") == 12, "Некорректный снимок не стирает прогресс");
            recovered.saveNow();
            check(Files.readString(file).contains("minecraft:stone"), "Восстановленное состояние сохраняется");
        } finally {
            try (var paths = Files.list(directory)) { for (var path : paths.toList()) Files.delete(path); }
            Files.delete(directory);
        }
    }

    private static void bundledBook() throws Exception {
        var directory = java.nio.file.Path.of("src/main/resources/assets/codex/book");
        List<String> documents = new java.util.ArrayList<>();
        try (var paths = Files.walk(directory.resolve("chapters"))) {
            for (var path : paths.filter(p -> p.toString().endsWith(".json")).sorted().toList())
                documents.add(Files.readString(path));
        }
        Book.CLIENT.loadFromDocuments(Files.readString(directory.resolve("sections.json")), documents);
        check(Book.CLIENT.totalQuests() > 0, "Опубликованная книга проходит runtime validation");
    }

    private static void networkBoundsAndLocalProgress() {
        String text = "Подробная книга — проверка UTF-8";
        check(Payloads.gunzip(Payloads.gzip(text)).equals(text), "Сжатие сохраняет текст книги");
        rejects(() -> Payloads.gunzip(new byte[]{1, 2, 3}));
        byte[] oversized = Payloads.gzip("a".repeat(Payloads.MAX_UNCOMPRESSED_BYTES + 1));
        rejects(() -> Payloads.gunzip(oversized));
        Tracker.PROGRESS.itemsNow.put("minecraft:stone", 9);
        Tracker.applyServerProgress(new com.google.gson.JsonObject());
        check(Tracker.PROGRESS.now("minecraft:stone") == 9, "Пакет без серверной книги не стирает локальный прогресс");
        Tracker.PROGRESS.clear();
    }

    private static String chapter(String id, String quests) {
        return "{\"id\":\"" + id + "\",\"section\":\"s\",\"title\":\"Chapter\",\"quests\":[" + quests + "]}";
    }
    private static String mappedChapter(String id, String quests) {
        var document = JsonParser.parseString(chapter(id, quests)).getAsJsonObject();
        document.addProperty("map", "s");
        return document.toString();
    }
    private static void rejects(Runnable action) {
        try { action.run(); } catch (RuntimeException expected) { return; }
        throw new AssertionError("Некорректные данные приняты");
    }
    private static void check(boolean condition, String message) {
        if (!condition) throw new AssertionError(message);
    }
}
