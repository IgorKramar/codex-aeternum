package ru.kramar.codex.client;

import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.components.Button;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.network.chat.Component;
import ru.kramar.codex.progress.Progress;
import ru.kramar.codex.progress.Tracker;

import java.util.ArrayList;
import java.util.List;
import java.util.function.Supplier;

/** Настройки книги: порядок прохождения (в прогрессе игрока) и удобства этого клиента. */
public final class CodexSettingsScreen extends Screen {
    private final Screen parent;
    private final List<Row> rows = new ArrayList<>();
    private int margin;
    private int bodyWidth;
    private int buttonWidth;

    /** Строка настройки: заголовок, описание текущего значения и кнопка, переключающая значение. */
    private record Row(String key, Supplier<String> value, Supplier<String> description, Button button) {
    }

    public CodexSettingsScreen(Screen parent) {
        super(Component.translatable("codex.settings.title"));
        this.parent = parent;
    }

    @Override
    protected void init() {
        rows.clear();
        margin = Math.max(16, Math.min(48, width / 20));
        bodyWidth = width - margin * 2;
        buttonWidth = Math.min(150, bodyWidth / 3);
        ClientOptions o = ClientOptions.get();
        row("codex.settings.order",
                () -> CodexScreen.tr("codex.settings.order." + orderKey()),
                () -> CodexScreen.tr("codex.settings.order." + orderKey() + ".desc"),
                b -> Tracker.setOrder(next(Tracker.PROGRESS.order)));
        row("codex.settings.tooltips", () -> onOff(o.itemTooltips), () -> CodexScreen.tr("codex.settings.tooltips.desc"),
                b -> { o.itemTooltips = !o.itemTooltips; o.save(); });
        row("codex.settings.toasts", () -> onOff(o.toasts), () -> CodexScreen.tr("codex.settings.toasts.desc"),
                b -> { o.toasts = !o.toasts; o.save(); });
        row("codex.settings.cover", () -> CodexScreen.tr(o.coverFirst ? "codex.settings.cover.on" : "codex.settings.cover.off"),
                () -> CodexScreen.tr("codex.settings.cover.desc"), b -> { o.coverFirst = !o.coverFirst; o.save(); });
        addRenderableWidget(Draw.button(Component.translatable("codex.ui.back"), b -> onClose(), width - 68, 8, 60, 20));
    }

    private void row(String key, Supplier<String> value, Supplier<String> description, Button.OnPress action) {
        Button button = Draw.button(Component.empty(), action, 0, 0, buttonWidth, 20);
        rows.add(new Row(key, value, description, button));
        addRenderableWidget(button);
    }

    private static String orderKey() {
        return Tracker.PROGRESS.order.name().toLowerCase();
    }

    private static Progress.Order next(Progress.Order current) {
        Progress.Order[] all = Progress.Order.values();
        return all[(current.ordinal() + 1) % all.length];
    }

    private static String onOff(boolean value) {
        return CodexScreen.tr(value ? "codex.ui.on" : "codex.ui.off");
    }

    @Override
    public void renderBackground(GuiGraphics g, int mx, int my, float partial) {
        // Иллюстрация обложки вместо стандартного размытия.
    }

    @Override
    public void render(GuiGraphics g, int mx, int my, float partial) {
        g.fill(0, 0, width, height, 0xFF071219);
        Draw.artwork(g, width, height);
        g.fill(0, 0, width, height, 0xB8071219);
        Draw.frame(g, 6, 6, width - 12, height - 12, 0xFF78633F);
        g.fill(margin, 24, margin + 24, 25, Theme.BORDER_LIGHT);
        g.drawString(font, Component.translatable("codex.settings.title"), margin + 32, 20, Theme.TEXT_DIM, false);

        int y = 44;
        y += Draw.wrapped(g, font, CodexScreen.tr("codex.settings.intro"), margin, y, bodyWidth, Theme.TEXT_DIM) + 14;
        int textWidth = bodyWidth - buttonWidth - 16;
        for (Row row : rows) {
            row.button().setMessage(Component.literal(row.value().get()));
            row.button().setPosition(width - margin - buttonWidth, y - 2);
            g.drawString(font, CodexScreen.tr(row.key()), margin, y, Theme.TEXT, false);
            int used = Draw.wrapped(g, font, row.description().get(), margin, y + 12, textWidth, Theme.TEXT_DIM);
            y += Math.max(24, 12 + used) + 12;
            g.fill(margin, y - 6, width - margin, y - 5, 0x5578633F);
        }
        super.render(g, mx, my, partial);
    }

    @Override
    public void onClose() {
        minecraft.setScreen(parent);
    }

    @Override
    public boolean keyPressed(int key, int scan, int mods) {
        if (CodexClient.OPEN_KEY.matches(key, scan)) { minecraft.setScreen(null); return true; }
        return super.keyPressed(key, scan, mods);
    }

    @Override
    public boolean isPauseScreen() { return false; }
}
