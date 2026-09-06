package ru.kramar.codex.book;

import com.google.gson.JsonObject;

/** Раздел — верхний уровень оглавления, объединяет главы. */
public final class Section {

    public final String id;
    public final int order;
    public final String title;
    public final String icon;
    public final int color;

    public Section(String id, int order, String title, String icon, int color) {
        this.id = id;
        this.order = order;
        this.title = title;
        this.icon = icon;
        this.color = color;
    }

    public static Section parse(String id, JsonObject o) {
        int order = o.has("order") ? o.get("order").getAsInt() : 1000;
        String title = o.has("title") ? o.get("title").getAsString() : id;
        String icon = o.has("icon") ? o.get("icon").getAsString() : "minecraft:book";
        int color = 0xFFB86B;
        if (o.has("color")) {
            String c = o.get("color").getAsString().replace("#", "");
            try {
                color = (int) Long.parseLong(c, 16);
            } catch (NumberFormatException ignored) {
                // цвет по умолчанию
            }
        }
        return new Section(id, order, title, icon, color);
    }
}
