package ru.kramar.codex.client;

import net.minecraft.ChatFormatting;
import net.minecraft.advancements.AdvancementHolder;
import net.minecraft.client.Minecraft;
import net.minecraft.client.resources.language.I18n;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.components.EditBox;
import net.minecraft.client.gui.components.Button;
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

    private static final int SIDE_W = 184;
    private static final int DETAIL_W = 300;
    private static final int TOP_H = 60;
    private static final int ROW_H = 22;
    private boolean sidebarVisible = true;
    private boolean overview;
    private Button mapsButton, fitButton, overviewButton, nextButton, coverButton;
    private final List<Quest> searchMatches = new ArrayList<>();
    private int matchIndex = -1;
    private int sideWidth() { return sidebarVisible ? SIDE_W : 0; }
    private boolean detailVisible() { return selected != null || overview; }
    private int detailWidth() { return Math.min(DETAIL_W, width0 - sideWidth()); }
    private int graphWidth() { return width0 - sideWidth() - (detailVisible() && width0 - sideWidth() >= detailWidth() + 230 ? detailWidth() : 0); }
    private int detailX() { return left + width0 - detailWidth(); }
    private void clearSelection() { selected = null; overview = false; detailScroll = 0; hits.clear(); }
    private Button control(String key, Runnable action) {
        return addRenderableWidget(Draw.button(Component.translatable(key), b -> action.run(), 0, 0, 40, 20));
    }

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

    private final GraphViewport view = new GraphViewport();
    private boolean dragging;

    private int left;
    private int top;
    private int width0;
    private int height0;

    private final String requestedMap;

    public CodexScreen() { this(null); }

    public CodexScreen(String requestedMap) {
        super(Component.translatable("codex.title"));
        this.requestedMap = requestedMap;
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
        if (width < 650) sidebarVisible = false;

        search = new EditBox(this.font, left + 10, top + 9, SIDE_W - 20, 16, Component.translatable("codex.ui.search"));
        search.setHint(Component.translatable("codex.ui.search").withColor(Theme.TEXT_FAINT));
        search.setBordered(false);
        search.setTextColor(Theme.TEXT);
        search.setMaxLength(64);
        search.setValue(filter);
        search.setResponder(v -> {
            filter = v.toLowerCase(Locale.ROOT);
            listScroll = 0;
            rebuildRows();
        });
        addRenderableWidget(search);
        mapsButton = control("codex.ui.maps", () -> { sidebarVisible = !sidebarVisible; hits.clear(); });
        fitButton = control("codex.ui.fit", () -> { clearSelection(); fitView(); });
        overviewButton = control("codex.ui.overview", () -> { clearSelection(); overview = true; });
        nextButton = control("codex.ui.next_match", this::nextMatch);
        coverButton = control("codex.ui.cover", () -> this.minecraft.setScreen(new CodexWelcomeScreen()));

        rebuildRows();

        if (chapter == null) {
            String wanted = requestedMap != null ? requestedMap : lastChapterId;
            Chapter want = wanted == null ? null : book().map(wanted);
            if (want == null && !book().maps().isEmpty()) want = book().maps().get(0);
            if (want != null) openChapter(want);
        }
        if (selected != null) focusQuest(selected);
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
        searchMatches.clear();
        matchIndex = -1;
        if (!filter.isEmpty()) for (Chapter map : book().maps()) for (Quest q : map.quests)
            if (matchesQuest(q)) searchMatches.add(q);
        for (Section s : book().sections()) {
            List<Chapter> in = new ArrayList<>();
            for (Chapter c : book().maps()) {
                if (!c.sectionId.equals(s.id)) continue;
                if (!matches(c)) continue;
                in.add(c);
            }
            if (in.isEmpty()) continue;
            if (in.size() > 1 || !in.get(0).title.equals(s.title)) rows.add(new Row(s, null));
            for (Chapter c : in) rows.add(new Row(s, c));
        }
        int visible = height0 - TOP_H - 8;
        listMaxScroll = Math.max(0, rows.size() * ROW_H - visible);
        listScroll = Math.min(listScroll, listMaxScroll);
    }

    private boolean matchesQuest(Quest q) {
        if (filter.isEmpty()) return false;
        if (tr(q.title).toLowerCase(Locale.ROOT).contains(filter)) return true;
        for (Task t : q.tasks) if (t.id.toLowerCase(Locale.ROOT).contains(filter)) return true;
        return false;
    }

    private void nextMatch() {
        if (searchMatches.isEmpty()) return;
        matchIndex = (matchIndex + 1) % searchMatches.size();
        jumpTo(searchMatches.get(matchIndex));
    }

    private void jumpTo(Quest q) {
        Chapter source = book().chapter(q.chapterId);
        if (source == null) return;
        Chapter target = book().map(source.mapId);
        if (target == null) return;
        if (chapter != target) openChapter(target);
        selected = q;
        overview = false;
        detailScroll = 0;
        hits.clear();
        if (width < 650) sidebarVisible = false;
        view.zoom = 1f;
        focusQuest(q);
    }

    private void focusQuest(Quest q) {
        int overlay = detailVisible() && width0 - sideWidth() < detailWidth() + 230 ? detailWidth() : 0;
        view.panX = -q.x * Theme.GRID - overlay / (2f * view.zoom);
        view.panY = -q.y * Theme.GRID;
    }

    private Quest dependency(Quest q, String dep) {
        return book().quest(dep.contains("/") ? dep : q.chapterId + "/" + dep);
    }

    private boolean matches(Chapter c) {
        if (filter.isEmpty()) return true;
        if (tr(c.title).toLowerCase(Locale.ROOT).contains(filter)) return true;
        if (tr(c.subtitle).toLowerCase(Locale.ROOT).contains(filter)) return true;
        for (Quest q : c.quests) {
            if (matchesQuest(q)) return true;
        }
        return false;
    }

    private void openChapter(Chapter c) {
        if (chapter != null) VIEWS.put(chapter.id, new float[]{view.panX, view.panY, view.zoom});
        chapter = c;
        lastChapterId = c.id;
        clearSelection();
        float[] v = VIEWS.get(c.id);
        if (v != null) {
            view.panX = v[0];
            view.panY = v[1];
            view.zoom = v[2];
        } else {
            fitView();
        }
    }

    private void fitView() {
        if (chapter == null || chapter.quests.isEmpty()) { view.panX = 0; view.panY = 0; return; }
        int minX = chapter.quests.stream().mapToInt(q -> q.x).min().orElse(0);
        int maxX = chapter.quests.stream().mapToInt(q -> q.x).max().orElse(0);
        int minY = chapter.quests.stream().mapToInt(q -> q.y).min().orElse(0);
        int maxY = chapter.quests.stream().mapToInt(q -> q.y).max().orElse(0);
        view.fit(minX, minY, maxX, maxY, Theme.GRID, graphWidth(), height0 - TOP_H);
    }

    // -------------------------------------------------------------- отрисовка

    /** Общая иллюстрация рисуется первой; стандартное размытие книге не требуется. */
    @Override
    public void renderBackground(GuiGraphics g, int mouseX, int mouseY, float partial) {
        // вызывается только явно из render()
    }

    @Override
    public void render(GuiGraphics g, int mouseX, int mouseY, float partial) {
        Draw.artwork(g, width, height);
        Draw.frame(g, left, top, width0, height0, Theme.BORDER_LIGHT);

        hits.clear();
        search.visible = sidebarVisible;
        search.active = sidebarVisible;
        if (!sidebarVisible) search.setFocused(false);
        if (sidebarVisible) renderSidebar(g, mouseX, mouseY);

        int graphX = left + sideWidth();
        int graphY = top + TOP_H;
        int graphW = graphWidth();
        int graphH = height0 - TOP_H;

        renderHeader(g, graphX, top, width0 - sideWidth());
        renderGraph(g, graphX, graphY, graphW, graphH);

        if (detailVisible()) {
            g.pose().pushPose();
            // Предметы карты рисуются на z=150; наложенная страница должна закрывать и их.
            g.pose().translate(0, 0, 200);
            if (selected != null) renderDetail(g, detailX(), graphY, detailWidth(), graphH, mouseX, mouseY);
            else renderOverview(g, detailX(), graphY, detailWidth(), graphH);
            g.pose().popPose();
        }
        int bx = left + 4;
        Button[] controls = {mapsButton, fitButton, overviewButton, nextButton, coverButton};
        for (Button b : controls) { b.setPosition(bx, top + 34); b.setWidth(56); bx += 58; }
        nextButton.active = !searchMatches.isEmpty();

        for (Renderable r : this.renderables) r.render(g, mouseX, mouseY, partial);
        renderHoverTooltip(g, graphX, graphY, graphW, graphH, mouseX, mouseY);
    }

    private void renderSidebar(GuiGraphics g, int mouseX, int mouseY) {
        int x = left;
        int y = top;
        Draw.panel(g, x, y, SIDE_W, height0, Theme.PANEL, Theme.BORDER);

        Draw.frame(g, x + 6, y + 5, SIDE_W - 12, 24, search.isFocused() ? Theme.TURQUOISE : Theme.BORDER);
        int listY = y + TOP_H;
        int listH = height0 - TOP_H - 2;
        g.enableScissor(x + 1, listY, x + SIDE_W - 1, listY + listH);
        int dy = listY - listScroll;
        for (Row row : rows) {
            if (dy > listY + listH) break;
            if (dy + ROW_H >= listY) {
                if (row.isHeader()) {
                    g.fill(x + 2, dy + 1, x + SIDE_W - 2, dy + ROW_H - 1, Theme.PANEL_ALT);
                    g.drawString(font, Draw.trim(font, tr(row.section.title).toUpperCase(Locale.ROOT), SIDE_W - 12),
                            x + 6, dy + 7, Theme.TURQUOISE, false);
                } else {
                    Chapter c = row.chapter;
                    boolean active = chapter != null && chapter.id.equals(c.id);
                    boolean hover = mouseX >= x + 2 && mouseX <= x + SIDE_W - 2 && mouseY >= dy && mouseY <= dy + ROW_H;
                    if (active) g.fill(x + 2, dy, x + SIDE_W - 2, dy + ROW_H, Theme.ROW_ACTIVE);
                    else if (hover) g.fill(x + 2, dy, x + SIDE_W - 2, dy + ROW_H, Theme.ROW_HOVER);

                    if (active) g.fill(x + 2, dy + 2, x + 4, dy + ROW_H - 2, Theme.ACCENT);
                    Draw.item(g, Draw.stack(c.icon), x + 7, dy + 3, 1f);

                    int done = Tracker.chapterDone(c);
                    int total = c.quests.size();
                    int color = done >= total && total > 0 ? Theme.DONE : (active ? Theme.ACCENT : Theme.TEXT);
                    g.drawString(font, Draw.trim(font, tr(c.title), SIDE_W - 76), x + 27, dy + 7, color, false);
                    String frac = done + "/" + total;
                    g.drawString(font, frac, x + SIDE_W - 6 - font.width(frac), dy + 7,
                            done >= total && total > 0 ? Theme.DONE : Theme.TEXT_FAINT, true);
                }
            }
            dy += ROW_H;
        }
        g.disableScissor();

        if (listMaxScroll > 0) {
            int trackH = listH;
            int barH = Math.max(12, (int) (trackH * (trackH / (float) (rows.size() * ROW_H))));
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
        Draw.item(g, Draw.stack(chapter.icon), x + 8, y + 8, 1f);
        g.drawString(font, Draw.trim(font, tr(chapter.title), Math.max(20, w - 125)), x + 30, y + 7, Theme.ACCENT, true);
        if (!chapter.subtitle.isEmpty()) {
            g.drawString(font, Draw.trim(font, tr(chapter.subtitle), Math.max(40, w - 150)),
                    x + 30, y + 19, Theme.TEXT_DIM, true);
        }

        if (w < 225) return;
        int done = Tracker.chapterDone(chapter);
        int total = Math.max(1, chapter.quests.size());
        int barW = 90;
        int barX = x + w - barW - 8;
        Draw.progressBar(g, barX, y + 8, barW, 5, done / (float) total, Theme.PANEL_DEEP, Theme.DONE);
        Draw.frame(g, barX - 1, y + 7, barW + 2, 7, Theme.BORDER);
        String frac = done + " / " + chapter.quests.size();
        g.drawString(font, frac, barX + barW - font.width(frac), y + 16, Theme.TEXT_DIM, true);


    }

    private void renderGraph(GuiGraphics g, int x, int y, int w, int h) {
        g.fill(x, y, x + w, y + h, Theme.ATLAS);
        Draw.frame(g, x, y, w, h, Theme.BORDER);
        Draw.corners(g, x + 4, y + 4, w - 8, h - 8, Theme.BORDER_LIGHT);
        if (chapter == null) return;

        g.enableScissor(x + 1, y + 1, x + w - 1, y + h - 1);
        int cx = x + w / 2;
        int cy = y + h / 2;
        for (int gx = x + 28; gx < x + w; gx += 48)
            for (int gy = y + 28; gy < y + h - 14; gy += 48)
                g.fill(gx, gy, gx + 1, gy + 1, Theme.ATLAS_GRID);

        if (chapter.quests.isEmpty()) {
            int ty = y + 12;
            for (String p : chapter.intro) ty += Draw.wrapped(g, font, tr(p), x + 10, ty, w - 20, Theme.TEXT_DIM) + 6;
            g.disableScissor();
            return;
        }

        for (Quest q : chapter.quests) {
            for (boolean any : new boolean[]{false, true}) for (String dep : any ? q.anyDeps : q.deps) {
                Quest p = dependency(q, dep);
                if (p == null || !chapter.quests.contains(p)) continue;
                int[] a = screenPos(cx, cy, p);
                int[] b = screenPos(cx, cy, q);
                int color = Tracker.completed(p) ? Theme.LINK_DONE : any ? Theme.LINK_ANY : Theme.LINK;
                if (any) Draw.dashedConnector(g, a[0], a[1], b[0], b[1], color);
                else Draw.connector(g, a[0], a[1], b[0], b[1], color, view.zoom >= 1f ? 2 : 1);
            }
        }

        for (Quest q : chapter.quests) {
            int[] p = screenPos(cx, cy, q);
            int size = Math.max(4, (int) (nodeSize(q) * view.zoom));
            int nx = p[0] - size / 2;
            int ny = p[1] - size / 2;
            if (nx > x + w || ny > y + h || nx + size < x || ny + size < y) continue;

            boolean done = Tracker.completed(q);
            boolean open = Tracker.unlocked(q);
            boolean claimable = Tracker.claimable(q);
            int border = done ? Theme.DONE : claimable ? Theme.CLAIM : open ? Theme.READY : Theme.LOCKED;
            int back = done ? Theme.NODE_DONE_BG : open ? Theme.NODE_READY_BG : Theme.NODE_LOCKED_BG;

            g.fill(nx - 2, ny - 2, nx + size + 2, ny + size + 2, 0x8007151F);
            g.fillGradient(nx, ny, nx + size, ny + size, back, Theme.PANEL_DEEP);
            Draw.thickFrame(g, nx, ny, size, size, border, Math.max(1, Math.min(size / 3, q.shape == Quest.Shape.BIG ? 3 : 2)));
            if (Tracker.PROGRESS.pinned.contains(q.globalId())) {
                Draw.thickFrame(g, nx - 2, ny - 2, size + 4, size + 4, Theme.PINNED, 1);
            }
            if (selected == q) Draw.corners(g, nx - 5, ny - 5, size + 10, size + 10, Theme.ACCENT);

            if (matchesQuest(q)) Draw.thickFrame(g, nx - 3, ny - 3, size + 6, size + 6, Theme.SEARCH, 2);
            float iconScale = Math.min(iconScale(q), Math.max(0.05f, (size - 4) / 16f));
            int icon = (int) (16 * iconScale);
            int pad = (size - icon) / 2;
            Draw.item(g, Draw.stack(q.icon), nx + pad, ny + pad, iconScale);
            if (!open) Draw.shade(g, nx + 1, ny + 1, size - 2, size - 2, Theme.NODE_LOCK_VEIL);
            if (q.optional && size >= 16) g.drawString(font, "◇", nx - 4, ny - 5, Theme.TEXT_DIM, false);
            if (done && size >= 14) g.drawString(font, "✔", nx + size - 8, ny + size - 9, Theme.DONE, true);
            else if (claimable && size >= 14) g.drawString(font, "!", nx + size - 6, ny + size - 10, Theme.CLAIM, true);
        }
        g.fill(x + 1, y + h - 14, x + w - 1, y + h - 1, Theme.PANEL_DEEP);
        g.drawString(font, Draw.trim(font, tr("codex.ui.legend"), w - 12), x + 6, y + h - 11, Theme.TEXT_DIM, false);
        g.disableScissor();
    }

    private void renderOverview(GuiGraphics g, int x, int y, int w, int h) {
        Draw.panel(g, x, y, w, h, Theme.PANEL, Theme.BORDER);
        if (chapter == null) return;
        g.enableScissor(x + 1, y + 1, x + w - 1, y + h - 1);
        int dy = y + 8 - detailScroll;
        dy += Draw.wrapped(g, font, tr(chapter.title), x + 8, dy, w - 16, Theme.ACCENT) + 8;
        dy += Draw.wrapped(g, font, tr("codex.ui.navigation"), x + 8, dy, w - 16, Theme.TEXT_DIM) + 10;
        dy += Draw.wrapped(g, font, tr("codex.ui.inventory_rules"), x + 8, dy, w - 16, Theme.TEXT_DIM) + 12;
        for (Chapter source : book().chapters()) {
            if (!source.mapId.equals(chapter.id)) continue;
            dy += Draw.wrapped(g, font, tr(source.title), x + 8, dy, w - 16, Theme.ACCENT_DIM) + 5;
            for (String paragraph : source.intro)
                dy += Draw.wrapped(g, font, tr(paragraph), x + 8, dy, w - 16, Theme.TEXT) + 6;
            dy += 6;
        }
        detailMaxScroll = Math.max(0, dy + detailScroll - y - h + 12);
        g.disableScissor();
        renderDetailScrollbar(g, x, y, w, h);
    }

    private void renderDetailScrollbar(GuiGraphics g, int x, int y, int w, int h) {
        if (detailMaxScroll <= 0) return;
        int track = h - 12;
        int thumb = Math.max(16, track * track / (track + detailMaxScroll));
        int at = y + 6 + (track - thumb) * detailScroll / detailMaxScroll;
        g.fill(x + w - 4, at, x + w - 2, at + thumb, Theme.TURQUOISE);
    }

    private void renderHoverTooltip(GuiGraphics g, int x, int y, int w, int h, int mouseX, int mouseY) {
        if (chapter == null || detailVisible() && mouseX >= detailX()) return;
        if (mouseX < x || mouseX > x + w || mouseY < y || mouseY > y + h) return;
        Quest q = questAt(x, y, w, h, mouseX, mouseY);
        if (q == null) return;
        List<Component> lines = new ArrayList<>();
        lines.add(Component.translatable(q.title).withStyle(
                Tracker.completed(q) ? ChatFormatting.GREEN
                        : Tracker.claimable(q) ? ChatFormatting.AQUA
                        : Tracker.unlocked(q) ? ChatFormatting.GOLD : ChatFormatting.GRAY));
        for (Task t : q.tasks) {
            lines.add(Component.literal(" • " + taskLabel(q, t))
                    .withStyle(Tracker.taskDone(q, t) ? ChatFormatting.GREEN : ChatFormatting.GRAY));
        }
        if (Tracker.claimable(q)) lines.add(Component.translatable("codex.ui.tip.claim").withStyle(ChatFormatting.AQUA));
        if (q.optional) lines.add(Component.translatable("codex.ui.optional").withStyle(ChatFormatting.GRAY));
        if (!Tracker.unlocked(q)) {
            lines.add(Component.translatable("codex.ui.tip.locked").withStyle(ChatFormatting.GRAY));
            for (String dep : q.deps) {
                Quest required = dependency(q, dep);
                if (required != null && !Tracker.completed(required)) lines.add(Component.literal(" • " + tr(required.title)).withStyle(ChatFormatting.RED));
            }
            if (!q.anyDeps.isEmpty() && q.anyDeps.stream().map(dep -> dependency(q, dep)).noneMatch(p -> p != null && Tracker.completed(p))) {
                lines.add(Component.translatable("codex.ui.requires_any").withStyle(ChatFormatting.GOLD));
                for (String dep : q.anyDeps) {
                    Quest required = dependency(q, dep);
                    if (required != null) lines.add(Component.literal(" • " + tr(required.title)).withStyle(ChatFormatting.RED));
                }
            }
        }
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

        if (q.optional) dy += Draw.wrapped(g, font, tr("codex.ui.optional"), x + 8, dy, inner, Theme.TEXT_DIM) + 5;
        dy = renderPrerequisites(g, q, x, dy, inner);
        for (String p : q.text) dy += Draw.wrapped(g, font, tr(p), x + 8, dy, inner, Theme.TEXT) + 9;

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

        List<Quest> successors = book().successors(q);
        if (!successors.isEmpty()) {
            dy += Draw.wrapped(g, font, tr("codex.ui.opens_next"), x + 8, dy + 6, inner, Theme.ACCENT_DIM) + 10;
            for (Quest next : successors) dy = questLink(g, next, x + 8, dy, inner);
        }
        if (Jei.available()) {
            dy += 6;
            dy += Draw.wrapped(g, font, tr("codex.ui.jei_hint"),
                    x + 8, dy, inner, Theme.TEXT_FAINT) + 3;
        }

        g.disableScissor();
        detailMaxScroll = Math.max(0, (dy + detailScroll) - (y + h) + 12);
        renderDetailScrollbar(g, x, y, w, h);
    }

    private int renderPrerequisites(GuiGraphics g, Quest q, int x, int dy, int inner) {
        for (boolean any : new boolean[]{false, true}) {
            List<String> deps = any ? q.anyDeps : q.deps;
            if (deps.isEmpty()) continue;
            dy += Draw.wrapped(g, font, tr(any ? "codex.ui.requires_any" : "codex.ui.requires_all"), x + 8, dy, inner, Theme.ACCENT_DIM) + 4;
            for (String dep : deps) {
                Quest target = dependency(q, dep);
                if (target != null) dy = questLink(g, target, x + 8, dy, inner);
            }
            dy += 5;
        }
        return dy;
    }

    private int questLink(GuiGraphics g, Quest target, int x, int y, int w) {
        int h = Draw.wrapped(g, font, (Tracker.completed(target) ? "✔ " : "→ ") + tr(target.title),
                x, y, w, Tracker.completed(target) ? Theme.DONE : Theme.PINNED);
        hits.add(new Hit(x, y, w, h, () -> jumpTo(target), null));
        return y + h + 4;
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
            case ADVANCEMENT -> I18n.get("codex.ui.task.advancement", advancementTitle(t.id, q));
            case DIMENSION -> I18n.get("codex.ui.task.dimension", dimensionName(t.id));
            case BIOME -> I18n.get("codex.ui.task.biome", biomeName(t.id));
            case CHECK -> tr("codex.ui.task.check");
            case PONDER -> I18n.get("codex.ui.task.ponder",
                    Draw.itemExists(t.id) ? Draw.stack(t.id).getHoverName().getString() : t.id);
        };
    }

    private static String advancementTitle(String id, Quest q) {
        ResourceLocation loc = ResourceLocation.tryParse(id);
        Minecraft mc = Minecraft.getInstance();
        if (loc != null && mc.getConnection() != null) {
            AdvancementHolder h = mc.getConnection().getAdvancements().get(loc);
            if (h != null && h.value().display().isPresent()) {
                return h.value().display().get().getTitle().getString();
            }
        }
        return tr(q.title);
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
        float s = (q.shape == Quest.Shape.BIG ? 2f : 1f) * view.zoom;
        if (s >= 3f) return 3f;
        if (s >= 2f) return 2f;
        if (s >= 1.5f) return 1.5f;
        if (s >= 1f) return 1f;
        if (s >= 0.75f) return 0.75f;
        return 0.5f;
    }

    private static float stepZoom(float current, int direction) {
        float[] steps = Theme.ZOOM_STEPS;
        if (direction > 0) {
            for (float step : steps) if (step > current + 0.001f) return step;
        } else {
            for (int i = steps.length - 1; i >= 0; i--) if (steps[i] < current - 0.001f) return steps[i];
        }
        return current;
    }

    private int nodeSize(Quest q) {
        return switch (q.shape) {
            case BIG -> Theme.NODE_BIG;
            case LORE -> Theme.NODE_LORE;
            default -> Theme.NODE;
        };
    }

    private int[] screenPos(int cx, int cy, Quest q) {
        return view.position(cx, cy, q.x, q.y, Theme.GRID);
    }

    private Quest questAt(int x, int y, int w, int h, double mx, double my) {
        if (chapter == null || mx < x + 1 || mx >= x + w - 1 || my < y + 1 || my >= y + h - 14) return null;
        int cx = x + w / 2;
        int cy = y + h / 2;
        for (int i = chapter.quests.size() - 1; i >= 0; i--) {
            Quest q = chapter.quests.get(i);
            int[] p = screenPos(cx, cy, q);
            int size = Math.max(4, (int) (nodeSize(q) * view.zoom));
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
        if (sidebarVisible && mx >= left && mx < left + sideWidth() && my >= listY && my < top + height0) {
            int index = (int) ((my - listY + listScroll) / ROW_H);
            if (index >= 0 && index < rows.size()) {
                Row row = rows.get(index);
                if (!row.isHeader()) {
                    openChapter(row.chapter);
                    if (width < 650) { sidebarVisible = false; fitView(); }
                }
            }
            return true;
        }

        int graphX = left + sideWidth();
        int graphY = top + TOP_H;
        int graphW = graphWidth();
        int graphH = height0 - TOP_H;

        if (detailVisible() && mx >= detailX() && mx < left + width0 && my >= graphY && my < top + height0) {
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
                    Quest target = selected == q ? null : q;
                    clearSelection();
                    selected = target;
                    if (target != null) focusQuest(target);
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
            view.panX += dx / view.zoom;
            view.panY += dy / view.zoom;
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
        if (mx < left || mx >= left + width0 || my < top + TOP_H || my >= top + height0) return super.mouseScrolled(mx, my, dx, dy);
        if (sidebarVisible && mx < left + sideWidth()) {
            listScroll = Math.max(0, Math.min(listMaxScroll, listScroll - (int) (dy * 18)));
            return true;
        }
        if (detailVisible() && mx >= detailX()) {
            detailScroll = Math.max(0, Math.min(detailMaxScroll, detailScroll - (int) (dy * 14)));
            hits.clear();
            return true;
        }
        float next = stepZoom(view.zoom, dy > 0 ? 1 : -1);
        if (next != view.zoom) {
            float cx = left + sideWidth() + graphWidth() / 2f;
            float cy = top + TOP_H + (height0 - TOP_H) / 2f;
            view.zoomAt(next, mx, my, cx, cy);
            return true;
        }
        return super.mouseScrolled(mx, my, dx, dy);
    }

    @Override
    public boolean keyPressed(int key, int scan, int mods) {
        if (key == GLFW.GLFW_KEY_F3 || key == GLFW.GLFW_KEY_ENTER && search.isFocused()) {
            nextMatch();
            return true;
        }
        if (search != null && search.isFocused() && key != GLFW.GLFW_KEY_ESCAPE) {
            return super.keyPressed(key, scan, mods);
        }
        if (CodexClient.OPEN_KEY.matches(key, scan)) {
            onClose();
            return true;
        }
        if (key == GLFW.GLFW_KEY_HOME) {
            clearSelection();
            fitView();
            return true;
        }
        if (key == GLFW.GLFW_KEY_ESCAPE && detailVisible()) {
            clearSelection();
            return true;
        }
        return super.keyPressed(key, scan, mods);
    }

    @Override
    public void onClose() {
        if (chapter != null) VIEWS.put(chapter.id, new float[]{view.panX, view.panY, view.zoom});
        Tracker.PROGRESS.saveNow();
        super.onClose();
    }

    @Override
    public boolean isPauseScreen() {
        return false;
    }
}
