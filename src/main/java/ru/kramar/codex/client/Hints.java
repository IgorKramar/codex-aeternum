package ru.kramar.codex.client;

import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import net.minecraft.ChatFormatting;
import net.minecraft.client.resources.language.I18n;
import net.minecraft.core.Holder;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.packs.resources.ResourceManager;
import net.minecraft.server.packs.resources.ResourceManagerReloadListener;
import net.minecraft.tags.TagKey;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.material.Fluid;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Optional;
import java.util.Set;

/** Источники предметов из `hints.json`: как скрафтить, с кого выпадает, где лежит. Имена подставляются на языке игры. */
public final class Hints {
    private static final Logger LOG = LoggerFactory.getLogger("codex");
    private static final ResourceLocation FILE = ResourceLocation.fromNamespaceAndPath("codex", "book/hints.json");
    private static JsonObject index = new JsonObject();

    private Hints() {
    }

    public static ResourceManagerReloadListener listener() {
        return Hints::load;
    }

    private static void load(ResourceManager rm) {
        JsonObject loaded = new JsonObject();
        try {
            var resource = rm.getResource(FILE);
            if (resource.isPresent()) {
                try (var reader = new InputStreamReader(resource.get().open(), StandardCharsets.UTF_8)) {
                    loaded = JsonParser.parseReader(reader).getAsJsonObject();
                }
            }
        } catch (Exception ex) {
            LOG.warn("Кодекс: индекс источников предметов не прочитан", ex);
        }
        index = loaded;
        JsonObject items = index.getAsJsonObject("items");
        LOG.info("Кодекс: источники предметов — {}", items == null ? 0 : items.size());
    }

    /** Строки подсказки о получении предмета; пусто, если в сборке ничего не найдено. */
    public static List<Component> lines(Item item) {
        JsonObject items = index.getAsJsonObject("items");
        JsonObject entry = items == null ? null : items.getAsJsonObject(BuiltInRegistries.ITEM.getKey(item).toString());
        List<Component> lines = new ArrayList<>();
        if (entry == null) return lines;
        if (entry.has("recipes")) {
            for (JsonElement e : entry.getAsJsonArray("recipes")) {
                JsonObject recipe = e.getAsJsonObject();
                String type = recipe.get("type").getAsString();
                lines.add(Component.literal(" ▸ " + recipeLabel(type) + ": " + names(recipe.getAsJsonArray("in")))
                        .withStyle(ChatFormatting.GRAY));
            }
        }
        list(lines, entry, "drops", "codex.hint.drop", Hints::entityWithHabitat);
        list(lines, entry, "chests", "codex.hint.chest", Hints::chestName);
        list(lines, entry, "blocks", "codex.hint.block", Hints::blockName);
        list(lines, entry, "world", "codex.hint.world", Hints::biomeName);
        return lines;
    }

    private static void list(List<Component> lines, JsonObject entry, String key, String label,
                             java.util.function.Function<String, String> namer) {
        if (!entry.has(key)) return;
        Set<String> names = new LinkedHashSet<>();
        for (JsonElement e : entry.getAsJsonArray(key)) names.add(namer.apply(e.getAsString()));
        lines.add(Component.literal(" ▸ " + I18n.get(label, String.join(", ", names))).withStyle(ChatFormatting.GRAY));
    }

    /** Название типа рецепта: перевод, если он есть, иначе «мод: тип». */
    private static String recipeLabel(String type) {
        String key = "codex.recipe." + type.replace(':', '.');
        if (I18n.exists(key)) return I18n.get(key);
        int colon = type.indexOf(':');
        String path = colon < 0 ? type : type.substring(colon + 1);
        return (colon < 0 ? "" : type.substring(0, colon) + ": ") + path.replace('_', ' ');
    }

    private static String names(JsonArray ingredients) {
        Set<String> names = new LinkedHashSet<>();
        for (JsonElement e : ingredients) {
            String id = e.getAsString();
            if (id.startsWith("~")) names.add(fluidName(id.substring(1)));
            else if (id.startsWith("#")) names.add(tagName(id.substring(1)));
            else names.add(itemName(id));
            if (names.size() >= 6) break;
        }
        return String.join(", ", names);
    }

    private static String itemName(String id) {
        return BuiltInRegistries.ITEM.getOptional(ResourceLocation.tryParse(id))
                .map(i -> i.getDescription().getString()).orElse(id);
    }

    private static String tagName(String id) {
        String path = id.startsWith("#") ? id.substring(1) : id;
        ResourceLocation location = ResourceLocation.tryParse(path);
        if (location != null) {
            Optional<Holder<Item>> first = BuiltInRegistries.ITEM.getTag(TagKey.create(Registries.ITEM, location))
                    .flatMap(named -> named.stream().findFirst());
            if (first.isPresent()) return I18n.get("codex.hint.tag", first.get().value().getDescription().getString());
        }
        return path.substring(path.indexOf(':') + 1).replace('_', ' ').replace('/', ' ');
    }

    private static String fluidName(String id) {
        String path = id.startsWith("#") ? id.substring(1) : id;
        ResourceLocation location = ResourceLocation.tryParse(path);
        Optional<Fluid> fluid = location == null ? Optional.empty() : BuiltInRegistries.FLUID.getOptional(location);
        if (fluid.isEmpty() && location != null) {
            fluid = BuiltInRegistries.FLUID.getTag(TagKey.create(Registries.FLUID, location))
                    .flatMap(named -> named.stream().findFirst()).map(Holder::value);
        }
        return fluid.map(f -> f.getFluidType().getDescription().getString())
                .orElse(path.substring(path.indexOf(':') + 1).replace('_', ' '));
    }

    private static String entityName(String id) {
        return EntityType.byString(id).map(t -> t.getDescription().getString()).orElse(id);
    }

    /** Существо и, если известно, где оно обитает: биомы из его правил появления или структура. */
    private static String entityWithHabitat(String id) {
        JsonObject entities = index.getAsJsonObject("entities");
        JsonArray habitat = entities == null ? null : entities.getAsJsonArray(id);
        if (habitat == null || habitat.isEmpty()) return entityName(id);
        Set<String> places = new LinkedHashSet<>();
        for (JsonElement e : habitat) {
            places.add(biomeName(e.getAsString()));
            if (places.size() >= 3) break;
        }
        return I18n.get("codex.hint.habitat", entityName(id), String.join(", ", places));
    }

    /** Биом или структура по идентификатору: перевод биома, если он есть, иначе читаемый путь. */
    private static String biomeName(String id) {
        ResourceLocation location = ResourceLocation.tryParse(id);
        if (location != null) {
            String key = "biome." + location.getNamespace() + "." + location.getPath();
            if (I18n.exists(key)) return I18n.get(key);
        }
        return id.substring(id.indexOf(':') + 1).replace('_', ' ').replace("/", " › ");
    }

    private static String blockName(String id) {
        return BuiltInRegistries.BLOCK.getOptional(ResourceLocation.tryParse(id))
                .map(Block::getName).map(Component::getString).orElse(id);
    }

    private static String chestName(String id) {
        String path = id.substring(id.indexOf(':') + 1);
        return path.replace('_', ' ').replace("/", " › ");
    }
}
