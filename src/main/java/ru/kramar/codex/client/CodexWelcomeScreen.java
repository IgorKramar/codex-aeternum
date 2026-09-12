package ru.kramar.codex.client;

import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.network.chat.Component;
import ru.kramar.codex.progress.Tracker;

/** Обложка и краткое руководство; весь текст остаётся переводимым и доступным виджетам. */
public final class CodexWelcomeScreen extends Screen {
    private static final int GOLD = Theme.BORDER_LIGHT;
    private static final int WHITE = Theme.TEXT;
    private static final int MUTED = Theme.TEXT_DIM;
    private int scroll;
    private int maxScroll;
    private int margin;
    private int bodyWidth;
    private int footerY;

    public CodexWelcomeScreen() {
        super(Component.translatable("codex.welcome.title"));
    }

    @Override
    protected void init() {
        margin = Math.max(16, Math.min(48, width / 20));
        bodyWidth = width - margin * 2;
        footerY = height - 43;
        int gap = 8;
        int buttonWidth = Math.min(170, (bodyWidth - gap) / 2);
        String primary = Tracker.PROGRESS.completed.isEmpty() ? "codex.welcome.open" : "codex.welcome.continue";
        addRenderableWidget(Draw.button(Component.translatable(primary), b -> minecraft.setScreen(new CodexScreen()), margin, footerY, buttonWidth, 22));
        addRenderableWidget(Draw.button(Component.translatable("codex.welcome.beginning"), b -> minecraft.setScreen(new CodexScreen("start")), margin + buttonWidth + gap, footerY, buttonWidth, 22));
        addRenderableWidget(Draw.button(Component.translatable("codex.ui.close"), b -> onClose(), width - 68, 8, 60, 20));
        scroll = 0;
    }

    @Override
    public void renderBackground(GuiGraphics g, int mx, int my, float partial) {
        // Обложка заменяет стандартное размытие, иначе оно размывает и саму иллюстрацию.
    }

    @Override
    public void render(GuiGraphics g, int mx, int my, float partial) {
        g.fill(0, 0, width, height, 0xFF071219);
        Draw.artwork(g, width, height);
        if (width < 650) g.fill(0, 0, width, height, 0xA5071219);
        Draw.frame(g, 6, 6, width - 12, height - 12, 0xFF78633F);
        g.fill(margin, 24, margin + 24, 25, GOLD);
        g.drawString(font, Component.translatable("codex.welcome.eyebrow"), margin + 32, 20, MUTED, false);

        g.enableScissor(margin - 2, 40, width - margin + 2, footerY - 12);
        int y = 52 - scroll;
        float logoScale = width >= 650 ? 4.5f : 3f;
        g.pose().pushPose();
        g.pose().translate(margin, y, 0);
        g.pose().scale(logoScale, logoScale, 1);
        g.drawString(font, "CODEX", 0, 0, GOLD, false);
        g.pose().popPose();
        y += (int)(10 * logoScale) + 7;
        g.pose().pushPose();
        g.pose().translate(margin + 1, y, 0);
        g.pose().scale(1.6f, 1.6f, 1);
        g.drawString(font, "A E T H E R N U M", 0, 0, WHITE, false);
        g.pose().popPose();
        y += 32;

        int textWidth = width >= 650 ? Math.min(360, bodyWidth * 46 / 100) : bodyWidth;
        y += Draw.wrapped(g, font, CodexScreen.tr("codex.welcome.purpose"), margin, y, textWidth, WHITE) + 12;
        y += Draw.wrapped(g, font, CodexScreen.tr("codex.welcome.promise"), margin, y, textWidth, MUTED) + 20;
        String progress = net.minecraft.client.resources.language.I18n.get("codex.welcome.progress",
                Tracker.book().totalQuests(), Math.min(Tracker.book().totalQuests(), Tracker.PROGRESS.completed.size()));
        y += Draw.wrapped(g, font, progress, margin, y, textWidth, GOLD) + 20;
        y = Math.max(y, 274 - scroll);
        g.fill(margin, y, width - margin, y + 1, 0x8878633F);
        y += 15;
        y += Draw.wrapped(g, font, CodexScreen.tr("codex.welcome.how"), margin, y, bodyWidth, GOLD) + 13;

        boolean columns = width >= 650;
        int cardWidth = columns ? (bodyWidth - 24) / 3 : bodyWidth;
        int bottom = y;
        for (int i = 0; i < 3; i++) {
            int x = margin + (columns ? i * (cardWidth + 12) : 0);
            int top = columns ? y : bottom;
            String prefix = "codex.welcome.step" + (i + 1);
            int titleHeight = font.split(Component.translatable(prefix + ".title"), cardWidth - 40).size() * font.lineHeight;
            int bodyHeight = font.split(Component.translatable(prefix + ".body"), cardWidth - 20).size() * font.lineHeight;
            int cardHeight = 30 + titleHeight + bodyHeight;
            g.fill(x, top, x + cardWidth, top + cardHeight, 0xDD091B23);
            g.fill(x, top, x + 2, top + cardHeight, 0xFFA28A59);
            g.drawString(font, "0" + (i + 1), x + 10, top + 10, GOLD, false);
            Draw.wrapped(g, font, CodexScreen.tr(prefix + ".title"), x + 30, top + 10, cardWidth - 40, WHITE);
            Draw.wrapped(g, font, CodexScreen.tr(prefix + ".body"), x + 10, top + 20 + titleHeight, cardWidth - 20, MUTED);
            bottom = Math.max(bottom, top + cardHeight + 10);
        }
        maxScroll = Math.max(0, bottom + scroll - (footerY - 14));
        scroll = Math.min(scroll, maxScroll);
        g.disableScissor();
        g.fill(7, footerY - 10, width - 7, height - 7, 0xEE071219);
        if (maxScroll > 0) {
            int trackHeight = Math.max(1, footerY - 57);
            int thumbHeight = Math.max(16, trackHeight * trackHeight / (trackHeight + maxScroll));
            int thumbY = 40 + (trackHeight - thumbHeight) * scroll / Math.max(1, maxScroll);
            g.fill(width - 12, thumbY, width - 10, thumbY + thumbHeight, GOLD);
        }
        super.render(g, mx, my, partial);
    }

    @Override
    public boolean mouseScrolled(double mx, double my, double dx, double dy) {
        scroll = Math.max(0, Math.min(maxScroll, scroll - (int)(dy * 24)));
        return true;
    }

    @Override
    public boolean keyPressed(int key, int scan, int mods) {
        if (CodexClient.OPEN_KEY.matches(key, scan)) { onClose(); return true; }
        if (key == org.lwjgl.glfw.GLFW.GLFW_KEY_PAGE_DOWN) { scroll = Math.min(maxScroll, scroll + 100); return true; }
        if (key == org.lwjgl.glfw.GLFW.GLFW_KEY_PAGE_UP) { scroll = Math.max(0, scroll - 100); return true; }
        return super.keyPressed(key, scan, mods);
    }

    @Override
    public boolean isPauseScreen() { return false; }
}
