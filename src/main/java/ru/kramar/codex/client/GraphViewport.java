package ru.kramar.codex.client;

/** Геометрия карты в GUI-пикселях; не зависит от Minecraft и доступна для точечных проверок. */
final class GraphViewport {
    float panX;
    float panY;
    float zoom = 1f;

    void center(int minX, int minY, int maxX, int maxY, int grid) {
        panX = -(minX + maxX) * grid / 2f;
        panY = -(minY + maxY) * grid / 2f;
    }

    void fit(int minX, int minY, int maxX, int maxY, int grid, int width, int height) {
        center(minX, minY, maxX, maxY, grid);
        zoom = Math.max(0.02f, Math.min(1f, Math.min(
                Math.max(1, width - 30f) / ((maxX - minX) * grid + 64),
                Math.max(1, height - 44f) / ((maxY - minY) * grid + 64))));
    }

    int[] position(int cx, int cy, int x, int y, int grid) {
        return new int[]{Math.round(cx + (x * grid + panX) * zoom),
                Math.round(cy + (y * grid + panY) * zoom)};
    }

    void zoomAt(float next, double mx, double my, float cx, float cy) {
        panX += (float)(mx - cx) * (1 / next - 1 / zoom);
        panY += (float)(my - cy) * (1 / next - 1 / zoom);
        zoom = next;
    }
}
