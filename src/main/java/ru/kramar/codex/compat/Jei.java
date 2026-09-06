package ru.kramar.codex.compat;

import net.minecraft.world.item.ItemStack;
import net.neoforged.fml.ModList;

/** Мягкая обёртка: без JEI мод продолжает работать. */
public final class Jei {

    private static Boolean loaded;

    private Jei() {
    }

    public static boolean loaded() {
        if (loaded == null) loaded = ModList.get().isLoaded("jei");
        return loaded;
    }

    public static boolean available() {
        return loaded() && CodexJeiPlugin.available();
    }

    public static void showRecipe(ItemStack stack) {
        if (available()) CodexJeiPlugin.show(stack, false);
    }

    public static void showUsage(ItemStack stack) {
        if (available()) CodexJeiPlugin.show(stack, true);
    }
}
