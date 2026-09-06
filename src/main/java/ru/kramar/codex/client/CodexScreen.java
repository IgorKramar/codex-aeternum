package ru.kramar.codex.client;

import net.minecraft.ChatFormatting;
import net.minecraft.advancements.AdvancementHolder;
import net.minecraft.client.Minecraft;
import net.minecraft.client.resources.language.I18n;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.components.EditBox;
import net.minecraft.client.gui.components.Renderable;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.ItemStack;
import org.lwjgl.glfw.GLFW;
import ru.kramar.codex.book.Book;
import ru.kramar.codex.book.Chapter;
import ru.kramar.codex.book.Quest;
import ru.kramar.codex.book.Reward;
import ru.kramar.codex.book.Section;
import ru.kramar.codex.book.Task;
import ru.kramar.codex.compat.Jei;
import ru.kramar.codex.progress.Tracker;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;

/** Главный экран книги: оглавление слева, граф заданий по центру, описание справа. */
public final class CodexScreen extends Screen {

    private static String lastChapterId;
    private static final Map<String, float[]> VIEWS = new HashMap<>();

    private static final int SIDE_W = 168;
    private static final int DETAIL_W = 210;
    private static final int TOP_H = 26;

    private final List<Row> rows = new ArrayList<>();
    private final List<Hit> hits = new ArrayList<>();
    private Chapter chapter;
    private Quest selected;

    private EditBox search;
    private String filter = "";

    private int listScroll;
    private int listMaxScroll;
    private int detailScroll;
    private int detailMaxScroll;

    private float panX;
    private float panY;
    private float zoom = 1f;
    private boolean dragging;

    private int left;
    private int top;
    private int width0;
    private int height0;

    public CodexScreen() {
        super(Component.translatable("codex.title"));
    }

    private Book book() {
        return Tracker.book();
    }

    @Override
    protected void init() {
        left = 6;
        top = 6;
        width0 = this.width - 12;
        height0 = this.height - 12;

        search = new EditBox(this.font, left + 6, top + 6, SIDE_W - 12, 14, Component.translatable("codex.ui.search"));
        search.setHint(Component.translatable("codex.ui.search").withStyle(ChatFormatting.DARK_GRAY));
        search.setBordered(true);
        search.setMaxLength(64);
        search.setValue(filter);
        search.setResponder(v -> {
            filter = v.toLowerCase(Locale.ROOT);
            listScroll = 0;
            rebuildRows();
        });
        addRenderableWidget(search);

        rebuildRows();

        if (chapter == null) {
            Chapter want = lastChapterId == null ? null : book().chapter(lastChapterId);
            if (want == null && !book().chapters().isEmpty()) want = book().chapters().get(0);
            if (want != null) openChapter(want);
        }
    }

    // ------------------------------------------------------------------ данные

    private record Row(Section section, Chapter chapter) {
        boolean isHeader() {
            return chapter == null;
        }
    }

    /** Кликабельная область на панели описания. */
    private record Hit(int x, int y, int w, int h, Runnable left, Runnable right) {
        boolean contains(double mx, double my) {
            return mx >= x && mx <= x + w && my >= y && my <= y + h;
        }
    }

    private void rebuildRows() {
        rows.clear();
        for (Section s : book().sections()) {
            List<Chapter> in = new ArrayList<>();
            for (Chapter c : book().chapters()) {
                if (!c.sectionId.equals(s.id)) continue;
                if (!matches(c)) continue;
                in.add(c);
            }
            if (in.isEmpty()) continue;
            rows.add(new Row(s, null));
            for (Chapter c : in) rows.add(new Row(s, c));
        }
        int visible = height0 - TOP_H - 8;
        listMaxScroll = Math.max(0, rows.size() * 14 - visible);
        listScroll = Math.min(listScroll, listMaxScroll);
    }

    private boolean matches(Chapter c) {
        if (filter.isEmpty()) return true;
        if (tr(c.title).toLowerCase(Locale.ROOT).contains(filter)) return true;
        if (tr(c.subtitle).toLowerCase(Locale.ROOT).contains(filter)) return true;
        for (Quest q : c.quests) {
            if (tr(q.title).toLowerCase(Locale.ROOT).contains(filter)) return true;
            for (Task t : q.tasks) if (t.id.toLowerCase(Locale.ROOT).contains(filter)) return true;
        }
        return false;
    }

    private void openChapter(Chapter c) {
        if (chapter != null) VIEWS.put(chapter.id, new float[]{panX, panY, zoom});
        chapter = c;
        lastChapterId = c.id;
        selected = null;
        detailScroll = 0;
        float[] v = VIEWS.get(c.id);
        if (v != null) {
            panX = v[0];
            panY = v[1];
            zoom = v[2];
        } else {
            zoom = 1f;
            centerView();
        }
    }

    private void centerView() {
        if (chapter == null || chapter.quests.isEmpty()) {
            panX = 0;
            panY = 0;
            return;
        }
        int minX = Integer.MAX_VALUE, minY = Integer.MAX_VALUE;
        int maxX = Integer.MIN_VALUE, maxY = Integer.MIN_VALUE;
        for (Quest q : chapter.quests) {
            minX = Math.min(minX, q.x);
            minY = Math.min(minY, q.y);
            maxX = Math.max(maxX, q.x);
            maxY = Math.max(maxY, q.y);
        }
        panX = -((minX + maxX) / 2f) * Theme.GRID;
        panY = -((minY + maxY) / 2f) * Theme.GRID + 10;
    }

    // -------------------------------------------------------------- отрисовка

    /**
     * Ваниль размывает кадр внутри renderBackground(), а Screen.render()
     * вызывает его сам. Поэтому фон рендерится явно и первым, а виджеты —
     * вручную в конце, иначе размытие ложится поверх уже нарисованной книги.
     */
    @Override
    public void renderBackground(GuiGraphics g, int mouseX, int mouseY, float partial) {
        // вызывается только явно из render()
    }

    @Override
    public void render(GuiGraphics g, int mouseX, int mouseY, float partial) {
        super.renderBackground(g, mouseX, mouseY, partial);
        g.fill(0, 0, this.width, this.height, Theme.BACKDROP);
        Draw.panel(g, left, top, width0, height0, Theme.PANEL_DEEP, Theme.BORDER);

        renderSidebar(g, mouseX, mouseY);

        int graphX = left + SIDE_W;
        int graphY = top + TOP_H;
        int graphW = width0 - SIDE_W - (selected != null ? DETAIL_W : 0);
        int graphH = height0 - TOP_H;

        renderHeader(g, graphX, top, width0 - SIDE_W);
        renderGraph(g, graphX, graphY, graphW, graphH);

        if (selected != null) {
            renderDetail(g, left + width0 - DETAIL_W, graphY, DETAIL_W, graphH, mouseX, mouseY);
        }

        for (Renderable r : this.renderables) r.render(g, mouseX, mouseY, partial);
        renderHoverTooltip(g, graphX, graphY, graphW, graphH, mouseX, mouseY);
    }

    private void renderSidebar(GuiGraphics g, int mouseX, int mouseY) {
        int x = left;
        int y = top;
        Draw.panel(g, x, y, SIDE_W, height0, Theme.PANEL, Theme.BORDER);

        int listY = y + TOP_H;
        int listH = height0 - TOP_H - 2;
        g.enableScissor(x + 1, listY, x + SIDE_W - 1, listY + listH);
        int dy = listY - listScroll;
        for (Row row : rows) {
            if (dy > listY + listH) break;
            if (dy + 14 >= listY) {
                if (row.isHeader()) {
                    g.fill(x + 2, dy + 1, x + SIDE_W - 2, dy + 13, Theme.PANEL_ALT);
                    g.drawString(font, Draw.trim(font, tr(row.section.title).toUpperCase(Locale.ROOT), SIDE_W - 12),
                            x + 6, dy + 3, row.section.color, true);
                } else {
                    Chapter c = row.chapter;
                    boolean active = chapter != null && chapter.id.equals(c.id);
                    boolean hover = mouseX >= x + 2 && mouseX <= x + SIDE_W - 2 && mouseY >= dy && mouseY <= dy + 14;
                    if (active) g.fill(x + 2, dy, x + SIDE_W - 2, dy + 14, Theme.ROW_ACTIVE);
                    else if (hover) g.fill(x + 2, dy, x + SIDE_W - 2, dy + 14, Theme.ROW_HOVER);

                    Draw.item(g, Draw.stack(c.icon), x + 5, dy - 1, 0.6f);

                    int done = Tracker.chapterDone(c);
                    int total = c.quests.size();
                    int color = done >= total && total > 0 ? Theme.DONE : (active ? Theme.ACCENT : Theme.TEXT);
                    g.drawString(font, Draw.trim(font, tr(c.title), SIDE_W - 62), x + 17, dy + 3, color, true);
                    String frac = done + "/" + total;
                    g.drawString(font, frac, x + SIDE_W - 6 - font.width(frac), dy + 3,
                            done >= total && total > 0 ? Theme.DONE : Theme.TEXT_FAINT, true);
                }
            }
            dy += 14;
        }
        g.disableScissor();

        if (listMaxScroll > 0) {
            int trackH = listH;
            int barH = Math.max(12, (int) (trackH * (trackH / (float) (rows.size() * 14))));
            int barY = listY + (int) ((trackH - barH) * (listScroll / (float) listMaxScroll));
            g.fill(x + SIDE_W - 3, listY, x + SIDE_W - 1, listY + trackH, Theme.PANEL_DEEP);
            g.fill(x + SIDE_W - 3, barY, x + SIDE_W - 1, barY + barH, Theme.BORDER_LIGHT);
        }
    }

    private void renderHeader(GuiGraphics g, int x, int y, int w) {
        Draw.panel(g, x, y, w, TOP_H, Theme.PANEL, Theme.BORDER);
        if (chapter == null) {
            g.drawString(font, tr("codex.ui.not_loaded"), x + 8, y + 9, Theme.TEXT_DIM, true);
            return;
        }
        Draw.item(g, Draw.stack(chapter.icon), x + 5, y + 5, 0.85f);
        g.drawString(font, tr(chapter.title), x + 24, y + 5, Theme.ACCENT, true);
        if (!chapter.subtitle.isEmpty()) {
            g.drawString(font, Draw.trim(font, tr(chapter.subtitle), Math.max(40, w - 150)),
                    x + 24, y + 15, Theme.TEXT_DIM, true);
        }

        int done = Tracker.chapterDone(chapter);
        int total = Math.max(1, chapter.quests.size());
        int barW = 90;
        int barX = x + w - barW - 8;
        Draw.progressBar(g, barX, y + 8, barW, 5, done / (float) total, Theme.PANEL_DEEP, Theme.DONE);
        Draw.frame(g, barX - 1, y + 7, barW + 2, 7, Theme.BORDER);
        String frac = done + " / " + chapter.quests.size();
        g.drawString(font, frac, barX + barW - font.width(frac), y + 16, Theme.TEXT_DIM, true);

        String mode = tr(Tracker.serverMode() ? "codex.ui.mode.server" : "codex.ui.mode.local");
        g.drawString(font, mode, barX - 8 - font.width(mode), y + 9, Theme.TEXT_FAINT, false);
    }

    private void renderGraph(GuiGraphics g, int x, int y, int w, int h) {
        Draw.panel(g, x, y, w, h, Theme.PANEL_DEEP, Theme.BORDER);
        if (chapter == null) return;

        g.enableScissor(x + 1, y + 1, x + w - 1, y + h - 1);
        int cx = x + w / 2;
        int cy = y + h / 2;

        if (chapter.quests.isEmpty()) {
            int ty = y + 12;
            for (String p : chapter.intro) ty += Draw.wrapped(g, font, tr(p), x + 10, ty, w - 20, Theme.TEXT_DIM) + 6;
            g.disableScissor();
            return;
        }

        for (Quest q : chapter.quests) {
            for (String dep : q.deps) {
                Quest p = chapter.byId.get(dep.contains("/") ? dep.substring(dep.indexOf('/') + 1) : dep);
                if (p == null) continue;
                int[] a = screenPos(cx, cy, p);
                int[] b = screenPos(cx, cy, q);
                if (Math.max(a[0], b[0]) < x || Math.min(a[0], b[0]) > x + w) continue;
                if (Math.max(a[1], b[1]) < y || Math.min(a[1], b[1]) > y + h) continue;
                boolean lit = Tracker.completed(p);
                Draw.connector(g, a[0], a[1], b[0], b[1], lit ? Theme.LINK_DONE : Theme.LINK, zoom >= 1f ? 2 : 1);
            }
        }

        for (Quest q : chapter.quests) {
            int[] p = screenPos(cx, cy, q);
            int size = (int) (nodeSize(q) * zoom);
            int nx = p[0] - size / 2;
            int ny = p[1] - size / 2;
            if (nx > x + w || ny > y + h || nx + size < x || ny + size < y) continue;

            boolean done = Tracker.completed(q);
            boolean open = Tracker.unlocked(q);
            boolean claimable = Tracker.claimable(q);
            int border = done ? Theme.DONE : claimable ? Theme.CLAIM : open ? Theme.READY : Theme.LOCKED;
            int back = done ? Theme.NODE_DONE_BG : open ? Theme.NODE_READY_BG : Theme.NODE_LOCKED_BG;

            g.fill(nx, ny, nx + size, ny + size, back);
            Draw.thickFrame(g, nx, ny, size, size, border, q.shape == Quest.Shape.BIG ? 3 : 2);
            if (Tracker.PROGRESS.pinned.contains(q.globalId())) {
                Draw.thickFrame(g, nx - 2, ny - 2, size + 4, size + 4, Theme.PINNED, 1);
            }
            if (selected == q) Draw.thickFrame(g, nx - 3, ny - 3, size + 6, size + 6, 0xFFFFFFFF, 1);

            float iconScale = iconScale(q);
            int icon = (int) (16 * iconScale);
            int pad = (size - icon) / 2;
            Draw.item(g, Draw.stack(q.icon), nx + pad, ny + pad, iconScale);
            if (!open) Draw.shade(g, nx + 1, ny + 1, size - 2, size - 2, Theme.NODE_LOCK_VEIL);
            if (done) g.drawString(font, "✔", nx + size - 8, ny + size - 9, Theme.DONE, true);
            else if (claimable) g.drawString(font, "!", nx + size - 6, ny + size - 10, Theme.CLAIM, true);
        }
        g.disableScissor();
    }

    private void renderHoverTooltip(GuiGraphics g, int x, int y, int w, int h, int mouseX, int mouseY) {
        if (chapter == null) return;
        if (mouseX < x || mouseX > x + w || mouseY < y || mouseY > y + h) return;
        Quest q = questAt(x, y, w, h, mouseX, mouseY);
        if (q == null) return;
        List<Component> lines = new ArrayList<>();
        lines.add(Component.translatable(q.title).withStyle(
                Tracker.completed(q) ? ChatFormatting.GREEN
                        : Tracker.claimable(q) ? ChatFormatting.AQUA
                        : Tracker.unlocked(q) ? ChatFormatting.GOLD : ChatFormatting.DARK_GRAY));
        for (Task t : q.tasks) {
            lines.add(Component.literal(" • " + taskLabel(q, t))
                    .withStyle(Tracker.taskDone(q, t) ? ChatFormatting.GREEN : ChatFormatting.GRAY));
        }
        if (Tracker.claimable(q)) lines.add(Component.translatable("codex.ui.tip.claim").withStyle(ChatFormatting.AQUA));
        if (!Tracker.unlocked(q)) lines.add(Component.translatable("codex.ui.tip.locked").withStyle(ChatFormatting.DARK_RED));
        g.renderComponentTooltip(font, lines, mouseX, mouseY);
    }

    private void renderDetail(GuiGraphics g, int x, int y, int w, int h, int mouseX, int mouseY) {
        Quest q = selected;
        hits.clear();
        Draw.panel(g, x, y, w, h, Theme.PANEL, Theme.BORDER);
        g.enableScissor(x + 1, y + 1, x + w - 1, y + h - 1);

        int inner = w - 16;
        int dy = y + 8 - detailScroll;

        Draw.item(g, Draw.stack(q.icon), x + 8, dy, 1f);
        int titleH = Draw.wrapped(g, font, tr(q.title), x + 28, dy + 2, inner - 20, Theme.ACCENT);
        dy += Math.max(18, titleH) + 6;

        boolean done = Tracker.completed(q);
        boolean claimable = Tracker.claimable(q);
        String state = tr(done ? (Tracker.claimed(q) ? "codex.ui.state.done_claimed" : "codex.ui.state.done")
                : claimable ? "codex.ui.state.claimable"
                : Tracker.unlocked(q) ? "codex.ui.state.open" : "codex.ui.state.locked");
        int stateColor = done ? Theme.DONE : claimable ? Theme.CLAIM
                : Tracker.unlocked(q) ? Theme.READY : Theme.TEXT_FAINT;
        dy += Draw.wrapped(g, font, state, x + 8, dy, inner, stateColor) + 3;

        g.fill(x + 8, dy, x + w - 8, dy + 1, Theme.BORDER);
        dy += 6;

        for (String p : q.text) dy += Draw.wrapped(g, font, tr(p), x + 8, dy, inner, Theme.TEXT) + 5;

        if (!q.tasks.isEmpty()) {
            dy += 2;
            g.drawString(font, tr("codex.ui.tasks"), x + 8, dy, Theme.ACCENT_DIM, true);
            dy += 11;
            for (Task t : q.tasks) {
                boolean tdone = Tracker.taskDone(q, t);
                int rowTop = dy;
                int tx = x + 14;
                if (t.kind == Task.Kind.ITEM) {
                    ItemStack stack = Draw.stack(t.id);
                    Draw.item(g, stack, x + 8, dy - 1, 0.7f);
                    tx = x + 22;
                    hits.add(new Hit(x + 8, dy - 1, 12, 12,
                            () -> Jei.showRecipe(stack), () -> Jei.showUsage(stack)));
                } else if (t.kind == Task.Kind.CHECK) {
                    String key = q.globalId() + "#" + t.progressKey();
                    boolean on = Tracker.PROGRESS.manual.contains(key);
                    g.drawString(font, on ? "[✔]" : "[ ]", x + 8, dy, on ? Theme.DONE : Theme.TEXT_DIM, true);
                    tx = x + 28;
                    hits.add(new Hit(x + 8, dy - 1, 18, 12, () -> Tracker.toggleFlag(key), null));
                }
                g.drawString(font, tdone ? "✔" : "✖", x + w - 16, dy, tdone ? Theme.DONE : Theme.TEXT_FAINT, true);
                int used = Draw.wrapped(g, font, taskLabel(q, t), tx, dy, w - (tx - x) - 22,
                        tdone ? Theme.DONE : Theme.TEXT);
                dy = rowTop + Math.max(12, used) + 3;
            }
        } else {
            dy += 2;
            boolean read = Tracker.PROGRESS.manual.contains(q.globalId());
            String label = tr(read ? "codex.ui.read" : "codex.ui.mark_read");
            g.drawString(font, label, x + 8, dy, read ? Theme.DONE : Theme.TEXT_DIM, true);
            hits.add(new Hit(x + 8, dy - 1, font.width(label), 12,
                    () -> Tracker.toggleFlag(q.globalId()), null));
            dy += 14;
        }

        Reward r = q.reward;
        if (!r.isEmpty()) {
            dy += 4;
            g.drawString(font, tr("codex.ui.reward"), x + 8, dy, Theme.ACCENT_DIM, true);
            dy += 11;
            for (Reward.Stack s : r.items) {
                ItemStack stack = Draw.stack(s.id());
                Draw.item(g, stack, x + 8, dy - 1, 0.7f);
                hits.add(new Hit(x + 8, dy - 1, 12, 12, () -> Jei.showRecipe(stack), () -> Jei.showUsage(stack)));
                String name = Draw.itemExists(s.id()) ? stack.getHoverName().getString() : s.id();
                dy += Draw.wrapped(g, font, name + " ×" + s.count(), x + 22, dy, w - 36, Theme.TEXT) + 3;
            }
            if (r.xp > 0) dy += Draw.wrapped(g, font, I18n.get("codex.ui.xp", r.xp), x + 8, dy, inner, Theme.TEXT) + 3;
            for (String t : r.text) dy += Draw.wrapped(g, font, "• " + tr(t), x + 8, dy, inner, Theme.TEXT_DIM) + 3;
        }

        if (claimable) {
            dy += 6;
            String label = tr(q.consumes() ? "codex.ui.claim_consume" : "codex.ui.claim");
            int bw = w - 16;
            int bh = 16;
            boolean hover = mouseX >= x + 8 && mouseX <= x + 8 + bw && mouseY >= dy && mouseY <= dy + bh;
            g.fill(x + 8, dy, x + 8 + bw, dy + bh, hover ? Theme.CLAIM_BTN_HOVER : Theme.CLAIM_BTN);
            Draw.frame(g, x + 8, dy, bw, bh, Theme.CLAIM);
            List<net.minecraft.util.FormattedCharSequence> ls = font.split(Component.literal(label), bw - 6);
            int ty = dy + (bh - ls.size() * font.lineHeight) / 2 + 1;
            for (var line : ls) {
                g.drawString(font, line, x + 8 + (bw - font.width(line)) / 2, ty, Theme.TEXT, true);
                ty += font.lineHeight;
            }
            hits.add(new Hit(x + 8, dy, bw, bh, () -> Tracker.claim(q), null));
            dy += bh + 4;
            if (!Tracker.serverMode()) {
                dy += Draw.wrapped(g, font, tr("codex.ui.local_notice"),
                        x + 8, dy, inner, Theme.TEXT_FAINT) + 3;
            }
        }

        if (Jei.available()) {
            dy += 6;
            dy += Draw.wrapped(g, font, tr("codex.ui.jei_hint"),
                    x + 8, dy, inner, Theme.TEXT_FAINT) + 3;
        }

        g.disableScissor();
        detailMaxScroll = Math.max(0, (dy + detailScroll) - (y + h) + 12);
    }

    private String taskLabel(Quest q, Task t) {
        if (!t.note.isEmpty() && t.kind != Task.Kind.ITEM) return tr(t.note);
        return switch (t.kind) {
            case ITEM -> {
                String name = Draw.itemExists(t.id) ? Draw.stack(t.id).getHoverName().getString() : t.id;
                int have = ru.kramar.codex.progress.Rules.taskProgress(Tracker.PROGRESS, t);
                String base = t.count > 1 ? name + " — " + have + "/" + t.count : name;
                String note = t.note.isEmpty() ? "" : " (" + tr(t.note) + ")";
                yield (t.consume ? I18n.get("codex.ui.task.consume", base) : base) + note;
            }
            case ADVANCEMENT -> I18n.get("codex.ui.task.advancement", advancementTitle(t.id));
            case DIMENSION -> I18n.get("codex.ui.task.dimension", dimensionName(t.id));
            case BIOME -> I18n.get("codex.ui.task.biome", biomeName(t.id));
            case CHECK -> tr("codex.ui.task.check");
            case PONDER -> I18n.get("codex.ui.task.ponder",
                    Draw.itemExists(t.id) ? Draw.stack(t.id).getHoverName().getString() : t.id);
        };
    }

    private static String advancementTitle(String id) {
        ResourceLocation loc = ResourceLocation.tryParse(id);
        Minecraft mc = Minecraft.getInstance();
        if (loc != null && mc.getConnection() != null) {
            AdvancementHolder h = mc.getConnection().getAdvancements().get(loc);
            if (h != null && h.value().display().isPresent()) {
                return h.value().display().get().getTitle().getString();
            }
        }
        return id;
    }

    /** Перевод ключа; отсутствующий ключ показывается как есть. */
    static String tr(String key) {
        return key == null || key.isEmpty() ? "" : I18n.get(key);
    }

    private static String biomeName(String id) {
        ResourceLocation loc = ResourceLocation.tryParse(id);
        if (loc == null) return id;
        String key = "biome." + loc.getNamespace() + "." + loc.getPath();
        return I18n.exists(key) ? I18n.get(key) : dimensionName(id);
    }

    private static String dimensionName(String id) {
        ResourceLocation loc = ResourceLocation.tryParse(id);
        if (loc == null) return id;
        String path = loc.getPath().replace('_', ' ');
        return Character.toUpperCase(path.charAt(0)) + path.substring(1);
    }

    // ------------------------------------------------------------------ ввод

    private float iconScale(Quest q) {
        float s = (q.shape == Quest.Shape.BIG ? 2f : 1f) * zoom;
        if (s >= 3f) return 3f;
        if (s >= 2f) return 2f;
        if (s >= 1.5f) return 1.5f;
        if (s >= 1f) return 1f;
        if (s >= 0.75f) return 0.75f;
        return 0.5f;
    }

    private static float stepZoom(float current, int direction) {
        float[] steps = Theme.ZOOM_STEPS;
        int index = 0;
        float best = Float.MAX_VALUE;
        for (int i = 0; i < steps.length; i++) {
            float d = Math.abs(steps[i] - current);
            if (d < best) {
                best = d;
                index = i;
            }
        }
        index = Math.max(0, Math.min(steps.length - 1, index + direction));
        return steps[index];
    }

    private int nodeSize(Quest q) {
        return switch (q.shape) {
            case BIG -> Theme.NODE_BIG;
            case LORE -> Theme.NODE_LORE;
            default -> Theme.NODE;
        };
    }

    private int[] screenPos(int cx, int cy, Quest q) {
        return new int[]{
                (int) (cx + (q.x * Theme.GRID + panX) * zoom),
                (int) (cy + (q.y * Theme.GRID + panY) * zoom)
        };
    }

    private Quest questAt(int x, int y, int w, int h, double mx, double my) {
        if (chapter == null) return null;
        int cx = x + w / 2;
        int cy = y + h / 2;
        for (int i = chapter.quests.size() - 1; i >= 0; i--) {
            Quest q = chapter.quests.get(i);
            int[] p = screenPos(cx, cy, q);
            int size = (int) (nodeSize(q) * zoom);
            if (mx >= p[0] - size / 2f && mx <= p[0] + size / 2f
                    && my >= p[1] - size / 2f && my <= p[1] + size / 2f) {
                return q;
            }
        }
        return null;
    }

    @Override
    public boolean mouseClicked(double mx, double my, int button) {
        if (super.mouseClicked(mx, my, button)) return true;

        int listY = top + TOP_H;
        if (mx >= left && mx <= left + SIDE_W && my >= listY) {
            int index = (int) ((my - listY + listScroll) / 14);
            if (index >= 0 && index < rows.size()) {
                Row row = rows.get(index);
                if (!row.isHeader()) openChapter(row.chapter);
            }
            return true;
        }

        int graphX = left + SIDE_W;
        int graphY = top + TOP_H;
        int graphW = width0 - SIDE_W - (selected != null ? DETAIL_W : 0);
        int graphH = height0 - TOP_H;

        if (selected != null && mx >= left + width0 - DETAIL_W && my >= graphY) {
            for (Hit hit : hits) {
                if (!hit.contains(mx, my)) continue;
                if (button == 1 && hit.right() != null) hit.right().run();
                else if (button == 0 && hit.left() != null) hit.left().run();
                return true;
            }
            return true;
        }

        if (mx >= graphX && mx <= graphX + graphW && my >= graphY && my <= graphY + graphH) {
            Quest q = questAt(graphX, graphY, graphW, graphH, mx, my);
            if (q != null) {
                if (button == 1) Tracker.togglePin(q.globalId());
                else {
                    selected = selected == q ? null : q;
                    detailScroll = 0;
                }
                return true;
            }
            if (button == 0) {
                dragging = true;
                return true;
            }
        }
        return true;
    }

    @Override
    public boolean mouseDragged(double mx, double my, int button, double dx, double dy) {
        if (dragging && button == 0) {
            panX += dx / zoom;
            panY += dy / zoom;
            return true;
        }
        return super.mouseDragged(mx, my, button, dx, dy);
    }

    @Override
    public boolean mouseReleased(double mx, double my, int button) {
        dragging = false;
        return super.mouseReleased(mx, my, button);
    }

    @Override
    public boolean mouseScrolled(double mx, double my, double dx, double dy) {
        if (mx <= left + SIDE_W) {
            listScroll = Math.max(0, Math.min(listMaxScroll, listScroll - (int) (dy * 18)));
            return true;
        }
        if (selected != null && mx >= left + width0 - DETAIL_W) {
            detailScroll = Math.max(0, Math.min(detailMaxScroll, detailScroll - (int) (dy * 14)));
            return true;
        }
        float old = zoom;
        zoom = stepZoom(zoom, dy > 0 ? 1 : -1);
        if (zoom != old) return true;
        return super.mouseScrolled(mx, my, dx, dy);
    }

    @Override
    public boolean keyPressed(int key, int scan, int mods) {
        if (search != null && search.isFocused() && key != GLFW.GLFW_KEY_ESCAPE) {
            return super.keyPressed(key, scan, mods);
        }
        if (CodexClient.OPEN_KEY.matches(key, scan)) {
            onClose();
            return true;
        }
        if (key == GLFW.GLFW_KEY_HOME) {
            centerView();
            zoom = 1f;
            return true;
        }
        if (key == GLFW.GLFW_KEY_ESCAPE && selected != null) {
            selected = null;
            return true;
        }
        return super.keyPressed(key, scan, mods);
    }

    @Override
    public void onClose() {
        if (chapter != null) VIEWS.put(chapter.id, new float[]{panX, panY, zoom});
        Tracker.PROGRESS.saveNow();
        super.onClose();
    }

    @Override
    public boolean isPauseScreen() {
        return false;
    }
}
