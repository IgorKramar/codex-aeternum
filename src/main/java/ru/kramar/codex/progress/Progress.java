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
        this.file = path;
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
        try {
            Files.createDirectories(file.getParent());
            try (BufferedWriter w = Files.newBufferedWriter(file, StandardCharsets.UTF_8)) {
                GSON.toJson(toJson(), w);
            }
            dirty = false;
        } catch (Exception ex) {
            LOG.error("Кодекс: не удалось сохранить прогресс в {}", file, ex);
        }
    }

    private void load() {
        if (file == null || !Files.isRegularFile(file)) return;
        try (BufferedReader r = Files.newBufferedReader(file, StandardCharsets.UTF_8)) {
            fromJson(JsonParser.parseReader(r).getAsJsonObject());
        } catch (Exception ex) {
            LOG.error("Кодекс: не удалось прочитать прогресс из {}", file, ex);
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

    public void fromJson(JsonObject o) {
        clear();
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
