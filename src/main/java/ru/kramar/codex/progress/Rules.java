package ru.kramar.codex.progress;

import ru.kramar.codex.book.Book;
import ru.kramar.codex.book.Chapter;
import ru.kramar.codex.book.Quest;
import ru.kramar.codex.book.Task;

import java.util.ArrayList;
import java.util.List;

/** Правила прохождения, общие для сервера и клиента. */
public final class Rules {

    private Rules() {
    }

    /** Задание доступно, если выполнены все его предпосылки. */
    public static boolean unlocked(Book book, Progress p, Quest q) {
        for (String dep : q.deps) {
            String gid = dep.contains("/") ? dep : q.chapterId + "/" + dep;
            if (!p.completed.contains(gid)) return false;
        }
        return q.anyDeps.isEmpty() || q.anyDeps.stream()
                .anyMatch(dep -> p.completed.contains(dep.contains("/") ? dep : q.chapterId + "/" + dep));
    }

    public static boolean completed(Progress p, Quest q) {
        return p.completed.contains(q.globalId());
    }

    public static boolean claimed(Progress p, Quest q) {
        return p.claimed.contains(q.globalId());
    }

    /** Все цели выполнены прямо сейчас (для consume учитывается текущий инвентарь). */
    public static boolean tasksDone(Progress p, Quest q) {
        if (q.tasks.isEmpty()) return p.manual.contains(q.globalId());
        if (!completed(p, q)) {
            for (var need : consumedItems(q).entrySet())
                if (p.now(need.getKey()) < need.getValue()) return false;
        }
        for (Task t : q.tasks) {
            if (!taskDone(p, q, t)) return false;
        }
        return true;
    }

    public static java.util.Map<String, Integer> consumedItems(Quest q) {
        java.util.Map<String, Integer> result = new java.util.LinkedHashMap<>();
        for (Task t : q.tasks) if (t.kind == Task.Kind.ITEM && t.consume)
            result.merge(t.id, t.count, Math::addExact);
        return result;
    }

    public static boolean validFlag(Book book, String key) {
        for (Chapter c : book.chapters()) for (Quest q : c.quests) {
            if (q.isLore() && q.globalId().equals(key)) return true;
            for (Task t : q.tasks) {
                if (t.kind == Task.Kind.CHECK && (q.globalId() + "#" + t.progressKey()).equals(key)) return true;
                if (t.kind == Task.Kind.PONDER && ("ponder|" + t.id).equals(key)) return true;
            }
        }
        return false;
    }

    public static boolean taskDone(Progress p, Quest q, Task t) {
        return switch (t.kind) {
            case ITEM -> t.consume
                    ? (p.now(t.id) >= t.count || p.completed.contains(q.globalId()))
                    : p.seen(t.id) >= t.count;
            case ADVANCEMENT -> p.advancements.contains(t.id);
            case DIMENSION -> p.dimensions.contains(t.id);
            case BIOME -> p.biomes.contains(t.id);
            case CHECK -> p.manual.contains(q.globalId() + "#" + t.progressKey());
            case PONDER -> p.manual.contains("ponder|" + t.id);
        };
    }

    public static int taskProgress(Progress p, Task t) {
        if (t.kind != Task.Kind.ITEM) return 0;
        return Math.min(t.consume ? p.now(t.id) : p.seen(t.id), t.count);
    }

    /**
     * Пересчитывает выполненные задания. Задания, требующие явного получения
     * награды, помечаются выполненными только при получении.
     *
     * @return задания, выполненные на этом проходе
     */
    public static List<Quest> recompute(Book book, Progress p) {
        List<Quest> fresh = new ArrayList<>();
        if (book.isEmpty()) return fresh;
        boolean changed = true;
        while (changed) {
            changed = false;
            for (Chapter c : book.chapters()) {
                for (Quest q : c.quests) {
                    String gid = q.globalId();
                    if (p.completed.contains(gid)) continue;
                    if (q.needsClaim()) continue;
                    if (!unlocked(book, p, q)) continue;
                    if (!tasksDone(p, q)) continue;
                    p.completed.add(gid);
                    p.markDirty();
                    changed = true;
                    fresh.add(q);
                }
            }
        }
        return fresh;
    }

    /** Готово ли задание к получению награды. */
    public static boolean claimable(Book book, Progress p, Quest q) {
        if (p.claimed.contains(q.globalId())) return false;
        if (!unlocked(book, p, q)) return false;
        if (p.completed.contains(q.globalId())) return true;
        return q.needsClaim() && tasksDone(p, q);
    }

    public static int chapterDone(Progress p, Chapter c) {
        int n = 0;
        for (Quest q : c.quests) if (p.completed.contains(q.globalId())) n++;
        return n;
    }
}
