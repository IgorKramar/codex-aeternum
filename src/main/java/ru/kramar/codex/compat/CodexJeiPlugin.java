package ru.kramar.codex.compat;

import mezz.jei.api.IModPlugin;
import mezz.jei.api.JeiPlugin;
import mezz.jei.api.constants.VanillaTypes;
import mezz.jei.api.recipe.RecipeIngredientRole;
import mezz.jei.api.runtime.IJeiRuntime;
import net.minecraft.client.Minecraft;

import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.ItemStack;

/** Позволяет открыть рецепт предмета прямо из книги. */
@JeiPlugin
public final class CodexJeiPlugin implements IModPlugin {

    private static IJeiRuntime runtime;

    @Override
    public ResourceLocation getPluginUid() {
        return ResourceLocation.fromNamespaceAndPath("codex", "jei");
    }

    @Override
    public void onRuntimeAvailable(IJeiRuntime jeiRuntime) {
        runtime = jeiRuntime;
    }

    @Override
    public void onRuntimeUnavailable() {
        runtime = null;
    }

    static boolean available() {
        return runtime != null;
    }

    static void show(ItemStack stack, boolean usage) {
        if (runtime == null || stack.isEmpty()) return;
        var focus = runtime.getJeiHelpers().getFocusFactory().createFocus(
                usage ? RecipeIngredientRole.INPUT : RecipeIngredientRole.OUTPUT,
                VanillaTypes.ITEM_STACK, stack);
        runtime.getRecipesGui().show(focus);
    }
}
