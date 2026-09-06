package ru.kramar.codex.book;

import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/** Глава книги: набор связанных заданий одной темы. */
public final class Chapter {

    public final String id;
    public final String sectionId;
    public final int order;
    public final String title;
    public final String subtitle;
    public final String icon;
    public final List<String> intro;
    public final List<Quest> quests;
    public final Map<String, Quest> byId;

    private Chapter(String id, String sectionId, int order, String title, String subtitle,
                    String icon, List<String> intro, List<Quest> quests) {
        this.id = id;
        this.sectionId = sectionId;
        this.order = order;
        this.title = title;
        this.subtitle = subtitle;
        this.icon = icon;
        this.intro = List.copyOf(intro);
        this.quests = List.copyOf(quests);
        Map<String, Quest> m = new LinkedHashMap<>();
        for (Quest q : quests) m.put(q.id, q);
        this.byId = Map.copyOf(m);
    }

    public static Chapter parse(JsonObject o) {
        String id = o.get("id").getAsString();
        String sectionId = o.has("section") ? o.get("section").getAsString() : "misc";
        int order = o.has("order") ? o.get("order").getAsInt() : 1000;
        String title = o.get("title").getAsString();
        String subtitle = o.has("subtitle") ? o.get("subtitle").getAsString() : "";
        String icon = o.has("icon") ? o.get("icon").getAsString() : "minecraft:book";
        List<String> intro = new ArrayList<>();
        if (o.has("intro")) {
            JsonElement e = o.get("intro");
            if (e.isJsonPrimitive()) intro.add(e.getAsString());
            else for (JsonElement x : (JsonArray) e) intro.add(x.getAsString());
        }
        List<Quest> quests = new ArrayList<>();
        if (o.has("quests")) {
            for (JsonElement e : o.getAsJsonArray("quests")) {
                quests.add(Quest.parse(id, e.getAsJsonObject()));
            }
        }
        return new Chapter(id, sectionId, order, title, subtitle, icon, intro, quests);
    }
}
