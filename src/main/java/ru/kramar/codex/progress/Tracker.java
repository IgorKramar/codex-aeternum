package ru.kramar.codex.progress;

import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import net.minecraft.ChatFormatting;
import net.minecraft.advancements.AdvancementHolder;
import net.minecraft.advancements.AdvancementProgress;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.components.toasts.SystemToast;
import net.minecraft.client.multiplayer.ClientAdvancements;
import net.minecraft.client.multiplayer.ServerData;
import net.minecraft.client.player.LocalPlayer;
import net.minecraft.core.Holder;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.biome.Biome;
import net.neoforged.fml.loading.FMLPaths;
import net.neoforged.neoforge.network.PacketDistributor;
import ru.kramar.codex.book.Book;
import ru.kramar.codex.book.Chapter;
import ru.kramar.codex.book.Quest;
import ru.kramar.codex.book.Task;
import ru.kramar.codex.net.Payloads;

import java.io.BufferedReader;
import java.lang.reflect.Field;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * Клиентская сторона прогресса. Два режима: локальный (сервер без мода —
 * всё считается на клиенте и хранится в файле) и серверный (клиент лишь
 * отображает присланное состояние и шлёт действия игрока).
 */
public final class Tracker {

    public static final Progress PROGRESS = new Progress();

    private static final SystemToast.SystemToastId TOAST_ID = new SystemToast.SystemToastId(5000L);

    private static boolean serverMode;
    /** Первая синхронизация после входа переносит старый прогресс и не должна сыпать уведомлениями. */
    private static boolean synced;
    private static Field advProgressField;
    private static boolean advProgressFieldMissing;
    private static int tick;
    private static long pondersStamp = -1;
    private static final Set<String> ponders = new HashSet<>();

    private Tracker() {
    }

    public static boolean serverMode() {
        return serverMode;
    }

    public static Book book() {
        return serverMode ? Book.REMOTE : Book.CLIENT;
    }

    // ---------------------------------------------------------- жизненный цикл

    public static void onJoin() {
        serverMode = false;
        PROGRESS.bind(FMLPaths.GAMEDIR.get().resolve("codex").resolve(Progress.sanitize(worldKey()) + ".json"));
        tick = 0;
        resetPonders();
    }

    public static void onLeave() {
        if (!serverMode) PROGRESS.unbind();
        else PROGRESS.clear();
        serverMode = false;
        resetPonders();
    }

    /** Сервер прислал книгу: переключаемся на серверный режим. */
    public static void enterServerMode() {
        if (!serverMode) {
            PROGRESS.saveNow();
            PROGRESS.unbind();
        }
        serverMode = true;
        synced = false;
        resetPonders();
    }

    public static void applyServerProgress(JsonObject json) {
        // Без принятой серверной книги локальное сохранение остаётся источником прогресса.
        if (!serverMode) return;
        Set<String> before = new HashSet<>(PROGRESS.completed);
        Set<String> beforeClaimed = new HashSet<>(PROGRESS.claimed);
        PROGRESS.fromJson(json);
        boolean announce = synced;
        synced = true;
        if (!announce) return;
        for (String gid : PROGRESS.completed) {
            if (!before.contains(gid) && !beforeClaimed.contains(gid)) {
                Quest q = book().quest(gid);
                if (q != null) toast(q);
            }
        }
    }

    // -------------------------------------------------------------------- тик

    public static void clientTick() {
        Minecraft mc = Minecraft.getInstance();
        LocalPlayer player = mc.player;
        if (player == null) return;
        tick++;
        if (tick % 20 != 0) return;

        scanPonders();

        if (serverMode) return;
        if (!PROGRESS.bound()) return;

        scanInventory(player);
        scanAdvancements(mc);
        scanWorld(player);
        processCompletions();
        PROGRESS.tickSave(player.level().getGameTime());
    }

    private static void processCompletions() {
        for (Quest q : Rules.recompute(book(), PROGRESS)) {
            PROGRESS.claimed.add(q.globalId());
            toast(q);
        }
    }

    private static void scanInventory(LocalPlayer player) {
        Map<String, Integer> counts = new HashMap<>();
        var inv = player.getInventory();
        for (int i = 0; i < inv.getContainerSize(); i++) add(counts, inv.getItem(i));
        add(counts, player.containerMenu.getCarried());
        PROGRESS.itemsNow.clear();
        PROGRESS.itemsNow.putAll(counts);
        counts.forEach(PROGRESS::recordItem);
    }

    private static void add(Map<String, Integer> counts, ItemStack stack) {
        if (stack == null || stack.isEmpty()) return;
        ResourceLocation id = BuiltInRegistries.ITEM.getKey(stack.getItem());
        counts.merge(id.toString(), stack.getCount(), Integer::sum);
    }

    @SuppressWarnings("unchecked")
    private static void scanAdvancements(Minecraft mc) {
        if (advProgressFieldMissing || mc.getConnection() == null) return;
        ClientAdvancements adv = mc.getConnection().getAdvancements();
        try {
            if (advProgressField == null) {
                for (Field f : ClientAdvancements.class.getDeclaredFields()) {
                    if (Map.class.isAssignableFrom(f.getType())) {
                        f.setAccessible(true);
                        advProgressField = f;
                        break;
                    }
                }
                if (advProgressField == null) {
                    advProgressFieldMissing = true;
                    return;
                }
            }
            Map<AdvancementHolder, AdvancementProgress> map =
                    (Map<AdvancementHolder, AdvancementProgress>) advProgressField.get(adv);
            if (map == null) return;
            for (Map.Entry<AdvancementHolder, AdvancementProgress> e : map.entrySet()) {
                if (e.getValue() != null && e.getValue().isDone()) {
                    if (PROGRESS.advancements.add(e.getKey().id().toString())) PROGRESS.markDirty();
                }
            }
        } catch (Throwable t) {
            advProgressFieldMissing = true;
        }
    }

    private static void scanWorld(LocalPlayer player) {
        String dim = player.level().dimension().location().toString();
        if (PROGRESS.dimensions.add(dim)) PROGRESS.markDirty();
        Holder<Biome> biome = player.level().getBiome(player.blockPosition());
        biome.unwrapKey().ifPresent(key -> {
            if (PROGRESS.biomes.add(key.location().toString())) PROGRESS.markDirty();
        });
    }

    /** Create ведёт список просмотренных сцен в ponders_watched.json. */
    private static void resetPonders() {
        pondersStamp = -1;
        ponders.clear();
    }

    private static void scanPonders() {
        Path file = FMLPaths.GAMEDIR.get().resolve("ponders_watched.json");
        try {
            if (!Files.isRegularFile(file)) return;
            long stamp = Files.getLastModifiedTime(file).toMillis();
            if (stamp == pondersStamp) return;
            try (BufferedReader r = Files.newBufferedReader(file, StandardCharsets.UTF_8)) {
                JsonElement e = JsonParser.parseReader(r);
                if (!e.isJsonArray()) return;
                for (JsonElement x : (JsonArray) e) {
                    String key = "ponder|" + x.getAsString();
                    if (Rules.validFlag(book(), key) && ponders.add(key)) setFlag(key, true);
                }
                pondersStamp = stamp;
            }
        } catch (Exception ignored) {
            // файл может писаться в этот момент — прочитаем в следующий раз
        }
    }

    // ------------------------------------------------------- действия игрока

    public static void setFlag(String key, boolean value) {
        if (!Rules.validFlag(book(), key)) return;
        if (serverMode) {
            PROGRESS.setManual(key, value);
            PacketDistributor.sendToServer(new Payloads.Flag(key, value));
        } else {
            PROGRESS.setManual(key, value);
            processCompletions();
        }
    }

    public static void toggleFlag(String key) {
        setFlag(key, !PROGRESS.manual.contains(key));
    }

    public static void togglePin(String gid) {
        if (book().quest(gid) == null) return;
        PROGRESS.togglePin(gid);
        if (serverMode) PacketDistributor.sendToServer(new Payloads.Pin(gid));
    }

    /** Получение награды. Локально награды выдать некому — задание просто засчитывается. */
    public static void claim(Quest q) {
        if (serverMode) {
            PacketDistributor.sendToServer(new Payloads.Claim(q.globalId()));
            return;
        }
        if (!Rules.claimable(book(), PROGRESS, q)) return;
        PROGRESS.completed.add(q.globalId());
        PROGRESS.claimed.add(q.globalId());
        PROGRESS.markDirty();
        processCompletions();
        toast(q);
    }

    // ------------------------------------------------------------ обёртки

    public static boolean unlocked(Quest q) {
        return Rules.unlocked(book(), PROGRESS, q);
    }

    public static boolean completed(Quest q) {
        return Rules.completed(PROGRESS, q);
    }

    public static boolean claimed(Quest q) {
        return Rules.claimed(PROGRESS, q);
    }

    public static boolean claimable(Quest q) {
        return Rules.claimable(book(), PROGRESS, q);
    }

    public static boolean taskDone(Quest q, Task t) {
        return Rules.taskDone(PROGRESS, q, t);
    }

    public static int chapterDone(Chapter c) {
        return Rules.chapterDone(PROGRESS, c);
    }

    private static void toast(Quest q) {
        if (!PROGRESS.announced.add(q.globalId()) || q.isLore()) return;
        Minecraft mc = Minecraft.getInstance();
        if (mc.getToasts() == null) return;
        Chapter c = book().chapter(q.chapterId);
        Component body = Component.translatable(q.title);
        if (c != null) body = body.copy().append(" — ").append(Component.translatable(c.title));
        SystemToast.add(mc.getToasts(), TOAST_ID,
                Component.translatable("codex.toast.done").withStyle(ChatFormatting.GOLD), body);
    }

    private static String worldKey() {
        Minecraft mc = Minecraft.getInstance();
        if (mc.hasSingleplayerServer() && mc.getSingleplayerServer() != null) {
            return "sp-" + mc.getSingleplayerServer().getWorldData().getLevelName();
        }
        ServerData sd = mc.getCurrentServer();
        if (sd != null) return "mp-" + sd.ip;
        return "default";
    }
}
