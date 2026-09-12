package ru.kramar.codex.progress;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedHashSet;
import java.util.Map;
import java.util.Set;

/**
 * Состояние прохождения одного игрока. Одна и та же структура живёт на
 * сервере (истина) и на клиенте (зеркало либо локальный режим без сервера).
 */
public final class Progress {

    private static final Logger LOG = LoggerFactory.getLogger("codex");
    private static final Gson GSON = new GsonBuilder().setPrettyPrinting().create();

    /** Максимальное количество предмета, которое игрок держал за всё время. */
    public final Map<String, Integer> itemsSeen = new HashMap<>();
    /** Текущее количество предметов в инвентаре (не сохраняется, нужно для consume). */
    public final Map<String, Integer> itemsNow = new HashMap<>();
    public final Set<String> advancements = new HashSet<>();
    public final Set<String> dimensions = new LinkedHashSet<>();
    public final Set<String> biomes = new LinkedHashSet<>();
    /** Цели, отмеченные вручную, и просмотренные сцены Ponder. */
    public final Set<String> manual = new HashSet<>();
    /** Задания, чьи цели выполнены. */
    public final Set<String> completed = new LinkedHashSet<>();
    /** Задания, за которые получена награда. */
    public final Set<String> claimed = new LinkedHashSet<>();
    public final Set<String> announced = new HashSet<>();
    public final Set<String> pinned = new LinkedHashSet<>();

    private Path file;
    private boolean dirty;
    private long lastSave;

    // ------------------------------------------------------------------ файл

    public void bind(Path path) {
        this.file = path.toAbsolutePath();
        lastSave = 0;
        clear();
        load();
    }

    public void unbind() {
        saveNow();
        this.file = null;
        clear();
    }

    public boolean bound() {
        return file != null;
    }

    public void clear() {
        itemsSeen.clear();
        itemsNow.clear();
        advancements.clear();
        dimensions.clear();
        biomes.clear();
        manual.clear();
        completed.clear();
        claimed.clear();
        announced.clear();
        pinned.clear();
        dirty = false;
    }

    public void markDirty() {
        dirty = true;
    }

    public boolean isDirty() {
        return dirty;
    }

    public void tickSave(long gameTime) {
        if (dirty && file != null && gameTime - lastSave > 200) {
            lastSave = gameTime;
            saveNow();
        }
    }

    public void saveNow() {
        if (file == null || !dirty) return;
        Path temporary = null;
        try {
            Files.createDirectories(file.getParent());
            temporary = Files.createTempFile(file.getParent(), file.getFileName().toString(), ".tmp");
            Files.writeString(temporary, GSON.toJson(toJson()), StandardCharsets.UTF_8);
            if (Files.isRegularFile(file)) {
                Path backupTemp = Files.createTempFile(file.getParent(), "codex-backup", ".tmp");
                try {
                    Files.copy(file, backupTemp, java.nio.file.StandardCopyOption.REPLACE_EXISTING);
                    replace(backupTemp, backup());
                } finally { Files.deleteIfExists(backupTemp); }
            }
            replace(temporary, file);
            dirty = false;
        } catch (Exception ex) {
            LOG.error("Кодекс: не удалось сохранить прогресс в {}", file, ex);
        } finally {
            if (temporary != null) try { Files.deleteIfExists(temporary); } catch (java.io.IOException ignored) { }
        }
    }

    private Path backup() { return file.resolveSibling(file.getFileName() + ".bak"); }

    private static void replace(Path source, Path target) throws java.io.IOException {
        try {
            Files.move(source, target, java.nio.file.StandardCopyOption.ATOMIC_MOVE,
                    java.nio.file.StandardCopyOption.REPLACE_EXISTING);
        } catch (java.nio.file.AtomicMoveNotSupportedException ex) {
            Files.move(source, target, java.nio.file.StandardCopyOption.REPLACE_EXISTING);
        }
    }

    private void load() {
        if (file == null) return;
        if (Files.isRegularFile(file)) {
            try {
                fromJson(JsonParser.parseString(Files.readString(file, StandardCharsets.UTF_8)).getAsJsonObject());
                return;
            } catch (Exception ex) {
                LOG.error("Кодекс: повреждён прогресс {}, пробуем резервную копию", file, ex);
                try {
                    Files.move(file, file.resolveSibling(file.getFileName() + ".corrupt-" + java.util.UUID.randomUUID()));
                } catch (java.io.IOException preserveFailure) {
                    throw new IllegalStateException("Не удалось сохранить повреждённый файл " + file, preserveFailure);
                }
            }
        }
        if (Files.isRegularFile(backup())) try {
            fromJson(JsonParser.parseString(Files.readString(backup(), StandardCharsets.UTF_8)).getAsJsonObject());
            dirty = true;
        } catch (Exception ex) {
            LOG.error("Кодекс: резервная копия также не читается: {}", backup(), ex);
        }
    }

    // ---------------------------------------------------------------- данные

    public void toggleManual(String key) {
        if (!manual.remove(key)) manual.add(key);
        dirty = true;
    }

    public void setManual(String key, boolean value) {
        boolean changed = value ? manual.add(key) : manual.remove(key);
        if (changed) dirty = true;
    }

    public void togglePin(String globalQuestId) {
        if (!pinned.remove(globalQuestId)) pinned.add(globalQuestId);
        dirty = true;
    }

    public int seen(String itemId) {
        Integer v = itemsSeen.get(itemId);
        return v == null ? 0 : v;
    }

    public int now(String itemId) {
        Integer v = itemsNow.get(itemId);
        return v == null ? 0 : v;
    }

    public void recordItem(String itemId, int count) {
        Integer old = itemsSeen.get(itemId);
        if (old == null || old < count) {
            itemsSeen.put(itemId, count);
            dirty = true;
        }
    }

    public void resetAll() {
        clear();
        dirty = true;
        saveNow();
    }

    // ----------------------------------------------------------------- JSON

    public JsonObject toJson() {
        JsonObject o = new JsonObject();
        JsonObject items = new JsonObject();
        itemsSeen.forEach(items::addProperty);
        o.add("items", items);
        o.add("advancements", array(advancements));
        o.add("dimensions", array(dimensions));
        o.add("biomes", array(biomes));
        o.add("manual", array(manual));
        o.add("completed", array(completed));
        o.add("claimed", array(claimed));
        o.add("announced", array(announced));
        o.add("pinned", array(pinned));
        return o;
    }

    public String toJsonString() {
        return toJson().toString();
    }

    public JsonObject snapshot() {
        JsonObject o = toJson();
        JsonObject current = new JsonObject();
        itemsNow.forEach(current::addProperty);
        o.add("itemsNow", current);
        return o;
    }

    public void fromJson(JsonObject o) {
        Progress next = new Progress();
        next.readJson(o);
        clear();
        itemsSeen.putAll(next.itemsSeen);
        itemsNow.putAll(next.itemsNow);
        advancements.addAll(next.advancements);
        dimensions.addAll(next.dimensions);
        biomes.addAll(next.biomes);
        manual.addAll(next.manual);
        completed.addAll(next.completed);
        claimed.addAll(next.claimed);
        announced.addAll(next.announced);
        pinned.addAll(next.pinned);
    }

    private void readJson(JsonObject o) {
        if (o.has("itemsNow")) for (var e : o.getAsJsonObject("itemsNow").entrySet())
            itemsNow.put(e.getKey(), e.getValue().getAsInt());
        if (o.has("items")) {
            for (Map.Entry<String, JsonElement> e : o.getAsJsonObject("items").entrySet()) {
                itemsSeen.put(e.getKey(), e.getValue().getAsInt());
            }
        }
        readSet(o, "advancements", advancements);
        readSet(o, "dimensions", dimensions);
        readSet(o, "biomes", biomes);
        readSet(o, "manual", manual);
        readSet(o, "completed", completed);
        readSet(o, "claimed", claimed);
        readSet(o, "announced", announced);
        readSet(o, "pinned", pinned);
    }

    private static void readSet(JsonObject o, String name, Set<String> into) {
        if (!o.has(name)) return;
        for (JsonElement e : o.getAsJsonArray(name)) into.add(e.getAsString());
    }

    private static JsonArray array(Set<String> set) {
        JsonArray a = new JsonArray();
        set.forEach(a::add);
        return a;
    }

    public static String sanitize(String s) {
        String out = s.replaceAll("[^A-Za-z0-9._-]", "_");
        if (out.length() > 64) out = out.substring(0, 64);
        return out.isEmpty() ? "default" : out;
    }
}
