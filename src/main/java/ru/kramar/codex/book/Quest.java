package ru.kramar.codex.book;

import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;

import java.util.ArrayList;
import java.util.List;

/** Узел книги: одно задание внутри главы. */
public final class Quest {

    /** Форма узла влияет только на отрисовку. */
    public enum Shape { NORMAL, BIG, LORE }

    public final String id;
    public final String chapterId;
    public final String title;
    public final String icon;
    public final int x;
    public final int y;
    public final Shape shape;
    public final List<String> deps;
    public final List<String> anyDeps;
    public final List<String> text;
    public final List<Task> tasks;
    public final Reward reward;
    public final boolean optional;

    private Quest(String id, String chapterId, String title, String icon, int x, int y, Shape shape,
                  List<String> deps, List<String> anyDeps, List<String> text, List<Task> tasks, Reward reward,
                  boolean optional) {
        this.id = id;
        this.chapterId = chapterId;
        this.title = title;
        this.icon = icon;
        this.x = x;
        this.y = y;
        this.shape = shape;
        this.deps = List.copyOf(deps);
        this.anyDeps = List.copyOf(anyDeps);
        this.text = List.copyOf(text);
        this.tasks = List.copyOf(tasks);
        this.reward = reward;
        this.optional = optional;
    }

    public String globalId() {
        return chapterId + "/" + id;
    }

    /** Информационный узел — без проверяемых целей. */
    public boolean isLore() {
        return tasks.isEmpty();
    }

    /** Есть ли цели, забирающие предметы. */
    public boolean consumes() {
        for (Task t : tasks) if (t.consume) return true;
        return false;
    }

    /** Требуется ли явное получение награды, как в GTNH. */
    public boolean needsClaim() {
        return consumes() || !reward.items.isEmpty();
    }

    public static Quest parse(String chapterId, JsonObject o) {
        String id = o.get("id").getAsString();
        String title = o.get("title").getAsString();
        String icon = o.has("icon") ? o.get("icon").getAsString() : "minecraft:paper";
        int x = o.has("x") ? o.get("x").getAsInt() : 0;
        int y = o.has("y") ? o.get("y").getAsInt() : 0;
        Shape shape = switch (o.has("shape") ? o.get("shape").getAsString() : "normal") {
            case "big" -> Shape.BIG;
            case "lore" -> Shape.LORE;
            default -> Shape.NORMAL;
        };
        List<String> deps = strings(o.get("deps"));
        List<String> text = strings(o.get("text"));
        Reward reward = Reward.parse(o.get("rewards"));
        List<Task> tasks = new ArrayList<>();
        if (o.has("tasks") && o.get("tasks").isJsonArray()) {
            for (JsonElement e : o.getAsJsonArray("tasks")) {
                tasks.add(Task.parse(e.getAsJsonObject()));
            }
        }
        boolean optional = o.has("optional") && o.get("optional").getAsBoolean();
        return new Quest(id, chapterId, title, icon, x, y, shape, deps, strings(o.get("any_deps")), text, tasks, reward, optional);
    }

    private static List<String> strings(JsonElement e) {
        List<String> out = new ArrayList<>();
        if (e == null || e.isJsonNull()) return out;
        if (e.isJsonPrimitive()) {
            out.add(e.getAsString());
            return out;
        }
        for (JsonElement x : (JsonArray) e) out.add(x.getAsString());
        return out;
    }
}
