package ru.kramar.codex.book;

import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;

import java.util.ArrayList;
import java.util.List;

/** Награда за задание: предметы, опыт и пояснительный текст. */
public final class Reward {

    public record Stack(String id, int count) {
    }

    public static final Reward NONE = new Reward(List.of(), 0, List.of());

    public final List<Stack> items;
    public final int xp;
    public final List<String> text;

    private Reward(List<Stack> items, int xp, List<String> text) {
        this.items = List.copyOf(items);
        this.xp = xp;
        this.text = List.copyOf(text);
    }

    public boolean hasLoot() {
        return !items.isEmpty() || xp > 0;
    }

    public boolean isEmpty() {
        return items.isEmpty() && xp == 0 && text.isEmpty();
    }

    /** Принимает как старую форму (список строк), так и объект. */
    public static Reward parse(JsonElement e) {
        if (e == null || e.isJsonNull()) return NONE;
        List<String> text = new ArrayList<>();
        if (e.isJsonPrimitive()) {
            text.add(e.getAsString());
            return new Reward(List.of(), 0, text);
        }
        if (e.isJsonArray()) {
            for (JsonElement x : e.getAsJsonArray()) text.add(x.getAsString());
            return new Reward(List.of(), 0, text);
        }
        JsonObject o = e.getAsJsonObject();
        List<Stack> items = new ArrayList<>();
        if (o.has("items")) {
            for (JsonElement x : o.getAsJsonArray("items")) {
                JsonObject s = x.getAsJsonObject();
                items.add(new Stack(s.get("id").getAsString(),
                        s.has("count") ? s.get("count").getAsInt() : 1));
            }
        }
        int xp = o.has("xp") ? o.get("xp").getAsInt() : 0;
        if (o.has("text")) {
            JsonElement t = o.get("text");
            if (t.isJsonPrimitive()) text.add(t.getAsString());
            else for (JsonElement x : (JsonArray) t) text.add(x.getAsString());
        }
        return new Reward(items, xp, text);
    }
}
