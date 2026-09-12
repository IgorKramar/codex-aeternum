package ru.kramar.codex.client;

/** Общая палитра обложки, ночного атласа и страниц руководства. */
public final class Theme {
    public static final int PANEL = 0xFF102B38;
    public static final int PANEL_ALT = 0xFF183D49;
    public static final int PANEL_DEEP = 0xFF07151F;
    public static final int BORDER = 0xFF796840;
    public static final int BORDER_LIGHT = 0xFFE4C180;
    public static final int TEXT = 0xFFF3EEE1;
    public static final int TEXT_DIM = 0xFFB8CCCF;
    public static final int TEXT_FAINT = 0xFF8FAAAF;
    public static final int ACCENT = 0xFFFFD578;
    public static final int ACCENT_DIM = 0xFFE4C180;
    public static final int TURQUOISE = 0xFF74DCD8;
    public static final int DONE = 0xFF81E3BF;
    public static final int ATLAS = 0xD9091926;
    public static final int ATLAS_GRID = 0xFF263F49;
    public static final int SEARCH = 0xFFFFEC9F;
    public static final int LINK_ANY = 0xFF698FA0;
    public static final int LINK = 0xFFA28A59;
    public static final int LINK_DONE = 0xFF4FBAAA;
    public static final int READY = 0xFFFFD578;
    public static final int LOCKED = 0xFF6C8490;
    public static final int PINNED = 0xFF82DDEB;
    public static final int CLAIM = 0xFF74DCD8;
    public static final int CLAIM_BTN = 0xFF174750;
    public static final int CLAIM_BTN_HOVER = 0xFF246371;
    public static final int ROW_ACTIVE = 0xFF214B55;
    public static final int ROW_HOVER = 0xFF183947;
    public static final int NODE_DONE_BG = 0xFF16443F;
    public static final int NODE_READY_BG = 0xFF3B3524;
    public static final int NODE_LOCKED_BG = 0xFF102736;
    public static final int NODE_LOCK_VEIL = 0x4507151F;

    public static final int GRID = 34;
    public static final int NODE = 24;
    public static final int NODE_BIG = 34;
    public static final int NODE_LORE = 20;
    /** Ступени сохраняют чёткость пиксельных иконок. */
    public static final float[] ZOOM_STEPS = {0.125f, 0.25f, 0.5f, 0.75f, 1.0f, 1.5f, 2.0f};
    private Theme() {}
}
