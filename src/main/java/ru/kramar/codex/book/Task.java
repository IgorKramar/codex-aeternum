package ru.kramar.codex.book;

import com.google.gson.JsonObject;
import net.minecraft.resources.ResourceLocation;

/** Одна проверяемая цель внутри задания. */
public final class Task {

    public enum Kind {
        /** Иметь предмет в инвентаре; при consume — предмет забирается при получении награды. */
        ITEM,
        /** Выполнить достижение мода. */
        ADVANCEMENT,
        /** Побывать в измерении. */
        DIMENSION,
        /** Побывать в биоме. */
        BIOME,
        /** Отметить вручную. */
        CHECK,
        /** Посмотреть обучающую сцену Create (Ponder) для предмета. */
        PONDER
    }

    public final Kind kind;
    public final String id;
    public final int count;
    /** Забирать ли предметы у игрока при получении награды. */
    public final boolean consume;
    /** Пояснение к цели; если пусто — текст собирается автоматически. */
    public final String note;

    private Task(Kind kind, String id, int count, boolean consume, String note) {
        this.kind = kind;
        this.id = id;
        this.count = count;
        this.consume = consume;
        this.note = note;
    }

    public static Task parse(JsonObject o) {
        String type = o.has("type") ? o.get("type").getAsString() : "item";
        Kind kind = switch (type) {
            case "advancement" -> Kind.ADVANCEMENT;
            case "dimension" -> Kind.DIMENSION;
            case "biome" -> Kind.BIOME;
            case "check" -> Kind.CHECK;
            case "ponder" -> Kind.PONDER;
            case "item" -> Kind.ITEM;
            default -> throw new IllegalArgumentException("Неизвестный тип цели: " + type);
        };
        String id = o.has("id") ? o.get("id").getAsString()
                : o.has("item") ? o.get("item").getAsString() : "";
        int count = o.has("count") ? o.get("count").getAsInt() : 1;
        boolean consume = o.has("consume") && o.get("consume").getAsBoolean();
        String note = o.has("note") ? o.get("note").getAsString() : "";
        if (count <= 0) throw new IllegalArgumentException("Количество цели должно быть положительным");
        if (consume && kind != Kind.ITEM) throw new IllegalArgumentException("consume допустим только для предметов");
        if (kind != Kind.CHECK && ResourceLocation.tryParse(id) == null)
            throw new IllegalArgumentException("Неверный идентификатор цели: " + id);
        return new Task(kind, id, count, consume, note);
    }

    public ResourceLocation location() {
        return ResourceLocation.tryParse(id);
    }

    /** Ключ, под которым цель хранится в файле прогресса. */
    public String progressKey() {
        return kind.name().toLowerCase() + "|" + id;
    }
}
