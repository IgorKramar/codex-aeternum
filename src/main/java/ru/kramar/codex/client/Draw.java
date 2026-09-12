package ru.kramar.codex.client;

import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.Font;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.components.Button;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.FormattedCharSequence;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;

import java.util.List;

/** Мелкие помощники отрисовки. */
public final class Draw {
    private static final ResourceLocation ART = ResourceLocation.fromNamespaceAndPath("codex", "textures/gui/welcome.png");

    private Draw() {
    }

    public static void panel(GuiGraphics g, int x, int y, int w, int h, int fill, int border) {
        g.fillGradient(x, y, x + w, y + h, fill, Theme.PANEL_DEEP);
        frame(g, x, y, w, h, border);
        corners(g, x + 2, y + 2, w - 4, h - 4, Theme.BORDER_LIGHT);
    }

    public static void artwork(GuiGraphics g, int width, int height) {
        float scale = Math.max(width / 1536f, height / 1024f);
        int w = Math.round(1536 * scale), h = Math.round(1024 * scale);
        g.blit(ART, (width - w) / 2, (height - h) / 2, w, h, 0f, 0f, 1536, 1024, 1536, 1024);
    }

    public static void corners(GuiGraphics g, int x, int y, int w, int h, int color) {
        int length = Math.min(8, Math.min(w, h) / 3);
        for (int dx : new int[]{0, w - 1}) for (int dy : new int[]{0, h - 1}) {
            int sx = x + dx, sy = y + dy;
            g.fill(dx == 0 ? sx : sx - length + 1, sy, dx == 0 ? sx + length : sx + 1, sy + 1, color);
            g.fill(sx, dy == 0 ? sy : sy - length + 1, sx + 1, dy == 0 ? sy + length : sy + 1, color);
        }
    }

    /** Меняется только рисунок: клавиатура, озвучивание и нажатия остаются ванильными. */
    public static Button button(Component label, Button.OnPress action, int x, int y, int w, int h) {
        return Button.builder(label, action).bounds(x, y, w, h).build(builder -> new Button(builder) {
            @Override
            protected void renderWidget(GuiGraphics g, int mx, int my, float partial) {
                boolean highlight = active && isHoveredOrFocused();
                int border = !active ? Theme.LOCKED : highlight ? Theme.TURQUOISE : Theme.BORDER_LIGHT;
                g.fillGradient(getX(), getY(), getX() + getWidth(), getY() + getHeight(),
                        highlight ? Theme.CLAIM_BTN_HOVER : Theme.PANEL_ALT, Theme.PANEL_DEEP);
                frame(g, getX(), getY(), getWidth(), getHeight(), border);
                if (isFocused()) frame(g, getX() + 2, getY() + 2, getWidth() - 4, getHeight() - 4, Theme.TURQUOISE);
                renderString(g, font(), active ? Theme.TEXT : Theme.TEXT_FAINT);
            }
        });
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
        int midX = (x1 + x2) / 2;
        hSeg(g, x1, midX, y1 - half, t, color);
        vSeg(g, y1, y2, midX - half, t, color);
        hSeg(g, midX, x2, y2 - half, t, color);
    }

    /** Пунктир выделяет альтернативные предпосылки даже без различения цветов. */
    public static void dashedConnector(GuiGraphics g, int x1, int y1, int x2, int y2, int color) {
        int midX = (x1 + x2) / 2;
        dashedSegment(g, x1, y1, midX, y1, color);
        dashedSegment(g, midX, y1, midX, y2, color);
        dashedSegment(g, midX, y2, x2, y2, color);
    }

    private static void dashedSegment(GuiGraphics g, int x1, int y1, int x2, int y2, int color) {
        int distance = Math.max(Math.abs(x2 - x1), Math.abs(y2 - y1));
        if (distance == 0) return;
        for (int i = 0; i < distance; i += 7) {
            int end = Math.min(distance, i + 4);
            int ax = x1 + (x2 - x1) * i / distance, ay = y1 + (y2 - y1) * i / distance;
            int bx = x1 + (x2 - x1) * end / distance, by = y1 + (y2 - y1) * end / distance;
            g.fill(Math.min(ax, bx), Math.min(ay, by), Math.max(ax, bx) + 1, Math.max(ay, by) + 1, color);
        }
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
