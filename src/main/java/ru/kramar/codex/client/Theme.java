package ru.kramar.codex.client;

/**
 * Цвета и размеры интерфейса книги.
 *
 * <p>Палитра намеренно контрастная. Тёмно-коричневые рамки на почти чёрном фоне
 * читаются как размытая муть: при разнице яркости меньше сотни любое
 * пересжатие картинки, невысокая гамма монитора или масштаб интерфейса
 * съедают границы. Каждый элемент здесь отличается от своей подложки
 * минимум на 90 единиц яркости.
 */
public final class Theme {

    /** Подложка чуть прозрачна: размытый мир за книгой виден как лёгкий фон. */
    public static final int BACKDROP = 0xD8080706;
    public static final int PANEL = 0xFF262119;
    public static final int PANEL_ALT = 0xFF3A3125;
    public static final int PANEL_DEEP = 0xFF151210;
    public static final int BORDER = 0xFF8A7048;
    public static final int BORDER_LIGHT = 0xFFB89464;

    public static final int TEXT = 0xFFFFF7E8;
    public static final int TEXT_DIM = 0xFFD6C8AC;
    public static final int TEXT_FAINT = 0xFFB0A288;
    public static final int ACCENT = 0xFFFFC24E;
    public static final int ACCENT_DIM = 0xFFD9A03A;

    public static final int DONE = 0xFF8CE668;
    public static final int DONE_DIM = 0xFF4E9A38;

    /** Линии связей: должны читаться на тёмном фоне, но не спорить с узлами. */
    public static final int LINK = 0xFF7A6748;
    public static final int LINK_DONE = 0xFF5FB043;

    public static final int READY = 0xFFFFC24E;
    public static final int LOCKED = 0xFF6B6355;
    public static final int PINNED = 0xFF7FCCFF;
    /** Задание с невостребованной наградой. */
    public static final int CLAIM = 0xFF5FD7E6;
    public static final int CLAIM_BTN = 0xFF1E3A40;
    public static final int CLAIM_BTN_HOVER = 0xFF2A5058;

    /** Выделение строки в оглавлении. */
    public static final int ROW_ACTIVE = 0xFF4A3D24;
    public static final int ROW_HOVER = 0xFF332B20;

    /** Фон узла по состоянию. */
    public static final int NODE_DONE_BG = 0xFF24361B;
    public static final int NODE_READY_BG = 0xFF352913;
    public static final int NODE_LOCKED_BG = 0xFF1C1A17;
    /** Затемнение поверх заблокированного узла. */
    public static final int NODE_LOCK_VEIL = 0x90121110;

    /**
     * Размеры узлов подобраны так, чтобы предмет 16x16 рисовался с целым
     * масштабом: 24 = 16 при 1.0, 34 = 32 при 2.0, 20 = 16 при 1.0.
     * Дробный масштаб текстуры даёт заметное мыло, особенно при guiScale 3-4.
     */
    public static final int GRID = 34;
    public static final int NODE = 24;
    public static final int NODE_BIG = 34;
    public static final int NODE_LORE = 20;

    /** Дискретные ступени масштаба: только те, что не мылят иконки. */
    public static final float[] ZOOM_STEPS = {0.5f, 0.75f, 1.0f, 1.5f, 2.0f};

    private Theme() {
    }
}
