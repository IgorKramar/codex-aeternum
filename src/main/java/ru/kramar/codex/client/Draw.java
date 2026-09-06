package ru.kramar.codex.client;

import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.Font;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.FormattedCharSequence;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;

import java.util.List;

/** Мелкие помощники отрисовки. */
public final class Draw {

    private Draw() {
    }

    public static void panel(GuiGraphics g, int x, int y, int w, int h, int fill, int border) {
        g.fill(x, y, x + w, y + h, fill);
        frame(g, x, y, w, h, border);
    }

    public static void frame(GuiGraphics g, int x, int y, int w, int h, int color) {
        g.fill(x, y, x + w, y + 1, color);
        g.fill(x, y + h - 1, x + w, y + h, color);
        g.fill(x, y, x + 1, y + h, color);
        g.fill(x + w - 1, y, x + w, y + h, color);
    }

    public static void thickFrame(GuiGraphics g, int x, int y, int w, int h, int color, int t) {
        g.fill(x, y, x + w, y + t, color);
        g.fill(x, y + h - t, x + w, y + h, color);
        g.fill(x, y, x + t, y + h, color);
        g.fill(x + w - t, y, x + w, y + h, color);
    }

    /**
     * Связь между узлами: горизонтальный сегмент до середины, затем вертикальный
     * и снова горизонтальный. Дёшево по вызовам и читается лучше диагонали.
     */
    public static void connector(GuiGraphics g, int x1, int y1, int x2, int y2, int color, int t) {
        int half = t / 2;
        if (y1 == y2) {
            hSeg(g, x1, x2, y1 - half, t, color);
            return;
        }
        if (x1 == x2) {
            vSeg(g, y1, y2, x1 - half, t, color);
            return;
        }
        int midY = (y1 + y2) / 2;
        vSeg(g, y1, midY, x1 - half, t, color);
        hSeg(g, x1, x2, midY - half, t, color);
        vSeg(g, midY, y2, x2 - half, t, color);
    }

    private static void hSeg(GuiGraphics g, int xa, int xb, int y, int t, int color) {
        int lo = Math.min(xa, xb);
        int hi = Math.max(xa, xb);
        g.fill(lo, y, hi + t, y + t, color);
    }

    private static void vSeg(GuiGraphics g, int ya, int yb, int x, int t, int color) {
        int lo = Math.min(ya, yb);
        int hi = Math.max(ya, yb);
        g.fill(x, lo, x + t, hi + t, color);
    }

    public static void progressBar(GuiGraphics g, int x, int y, int w, int h, float value,
                                   int back, int front) {
        g.fill(x, y, x + w, y + h, back);
        int filled = (int) (w * Math.max(0f, Math.min(1f, value)));
        if (filled > 0) g.fill(x, y, x + filled, y + h, front);
    }

    /** Возвращает высоту выведенного текста. */
    public static int wrapped(GuiGraphics g, Font font, String text, int x, int y, int width, int color) {
        List<FormattedCharSequence> lines = font.split(Component.literal(text), Math.max(8, width));
        int dy = y;
        for (FormattedCharSequence line : lines) {
            g.drawString(font, line, x, dy, color, false);
            dy += font.lineHeight;
        }
        return dy - y;
    }

    public static int wrappedHeight(Font font, String text, int width) {
        return font.split(Component.literal(text), Math.max(8, width)).size() * font.lineHeight;
    }

    public static ItemStack stack(String id) {
        if (id == null || id.isEmpty()) return new ItemStack(Items.PAPER);
        ResourceLocation loc = ResourceLocation.tryParse(id);
        if (loc == null) return new ItemStack(Items.PAPER);
        return BuiltInRegistries.ITEM.getOptional(loc)
                .map(ItemStack::new)
                .orElseGet(() -> new ItemStack(Items.BARRIER));
    }

    public static boolean itemExists(String id) {
        ResourceLocation loc = ResourceLocation.tryParse(id);
        return loc != null && BuiltInRegistries.ITEM.getOptional(loc).isPresent();
    }

    public static void item(GuiGraphics g, ItemStack stack, int x, int y, float scale) {
        g.pose().pushPose();
        g.pose().translate(x, y, 0);
        g.pose().scale(scale, scale, 1f);
        g.renderItem(stack, 0, 0);
        g.pose().popPose();
    }

    public static void shade(GuiGraphics g, int x, int y, int w, int h, int color) {
        g.fill(x, y, x + w, y + h, color);
    }

    public static String trim(Font font, String text, int width) {
        int w = Math.max(8, width);
        if (font.width(text) <= w) return text;
        String cut = font.plainSubstrByWidth(text, Math.max(1, w - font.width("…")));
        return cut + "…";
    }

    public static Font font() {
        return Minecraft.getInstance().font;
    }
}
