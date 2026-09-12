package ru.kramar.codex.server;

import net.minecraft.ChatFormatting;
import net.minecraft.advancements.AdvancementHolder;
import net.minecraft.core.Holder;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.biome.Biome;
import net.minecraft.world.level.storage.LevelResource;
import net.neoforged.neoforge.items.ItemHandlerHelper;
import net.neoforged.neoforge.network.PacketDistributor;
import ru.kramar.codex.book.Book;
import ru.kramar.codex.book.Chapter;
import ru.kramar.codex.book.Quest;
import ru.kramar.codex.book.Reward;
import ru.kramar.codex.book.Task;
import ru.kramar.codex.net.Payloads;
import ru.kramar.codex.progress.Progress;
import ru.kramar.codex.progress.Rules;

import java.nio.file.Path;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.UUID;

/** Серверная сторона: хранит прогресс игроков, проверяет цели, выдаёт награды. */
public final class ServerProgress {

    private static final Map<UUID, Progress> PLAYERS = new HashMap<>();
    private static final Map<UUID, Boolean> DIRTY_SYNC = new HashMap<>();
    /** Достижения, на которые ссылается книга: только их и проверяем. */
    private static Set<String> watchedAdvancements = new HashSet<>();

    private ServerProgress() {
    }

    // ------------------------------------------------------------- жизненный цикл

    public static void onBookLoaded() {
        Set<String> adv = new HashSet<>();
        for (Chapter c : Book.SERVER.chapters()) {
            for (Quest q : c.quests) {
                for (Task t : q.tasks) if (t.kind == Task.Kind.ADVANCEMENT) adv.add(t.id);
            }
        }
        watchedAdvancements = adv;
    }

    public static void onLogin(ServerPlayer player) {
        Progress p = new Progress();
        p.bind(fileFor(player.server, player.getUUID()));
        PLAYERS.put(player.getUUID(), p);
        sendBook(player);
        sendProgress(player);
    }

    public static void onLogout(ServerPlayer player) {
        Progress p = PLAYERS.remove(player.getUUID());
        if (p != null) p.unbind();
        DIRTY_SYNC.remove(player.getUUID());
    }

    public static void onServerStopping() {
        for (Progress p : PLAYERS.values()) p.saveNow();
    }

    private static Path fileFor(MinecraftServer server, UUID id) {
        return server.getWorldPath(LevelResource.ROOT).resolve("codex").resolve(id + ".json");
    }

    public static Progress of(ServerPlayer player) {
        return PLAYERS.get(player.getUUID());
    }

    // ------------------------------------------------------------------ тик

    public static void tick(ServerPlayer player) {
        Progress p = PLAYERS.get(player.getUUID());
        if (p == null || Book.SERVER.isEmpty()) return;
        if (player.tickCount % 20 != 0) return;

        scanInventory(player, p);
        scanAdvancements(player, p);
        scanWorld(player, p);
        processCompletions(player, p);
        if (p.isDirty()) DIRTY_SYNC.put(player.getUUID(), true);
        p.tickSave(player.level().getGameTime());
        if (Boolean.TRUE.equals(DIRTY_SYNC.remove(player.getUUID()))) sendProgress(player);
    }

    private static List<ItemStack> inventoryStacks(ServerPlayer player) {
        List<ItemStack> slots = new java.util.ArrayList<>();
        var inventory = player.getInventory();
        for (int i = 0; i < inventory.getContainerSize(); i++) slots.add(inventory.getItem(i));
        slots.add(player.containerMenu.getCarried());
        return slots;
    }

    private static void scanInventory(ServerPlayer player, Progress p) {
        Map<String, Integer> counts = new HashMap<>();
        inventoryStacks(player).forEach(stack -> add(counts, stack));
        if (!p.itemsNow.equals(counts)) DIRTY_SYNC.put(player.getUUID(), true);
        p.itemsNow.clear();
        p.itemsNow.putAll(counts);
        counts.forEach(p::recordItem);
    }

    private static void add(Map<String, Integer> counts, ItemStack stack) {
        if (stack == null || stack.isEmpty()) return;
        ResourceLocation id = BuiltInRegistries.ITEM.getKey(stack.getItem());
        counts.merge(id.toString(), stack.getCount(), Integer::sum);
    }

    private static void scanAdvancements(ServerPlayer player, Progress p) {
        for (String id : watchedAdvancements) {
            if (p.advancements.contains(id)) continue;
            ResourceLocation loc = ResourceLocation.tryParse(id);
            if (loc == null) continue;
            AdvancementHolder holder = player.server.getAdvancements().get(loc);
            if (holder == null) continue;
            if (player.getAdvancements().getOrStartProgress(holder).isDone()) {
                p.advancements.add(id);
                p.markDirty();
            }
        }
    }

    private static void scanWorld(ServerPlayer player, Progress p) {
        String dim = player.level().dimension().location().toString();
        if (p.dimensions.add(dim)) p.markDirty();
        Holder<Biome> biome = player.level().getBiome(player.blockPosition());
        biome.unwrapKey().ifPresent(key -> {
            if (p.biomes.add(key.location().toString())) p.markDirty();
        });
    }

    // -------------------------------------------------------- действия игрока

    public static void claim(ServerPlayer player, String gid) {
        Progress p = PLAYERS.get(player.getUUID());
        Quest q = Book.SERVER.quest(gid);
        if (p == null || q == null) return;
        scanInventory(player, p);
        if (!Rules.claimable(Book.SERVER, p, q)) return;

        if (!takeItems(player, Rules.consumedItems(q))) {
            player.sendSystemMessage(Component.translatable("codex.msg.not_enough").withStyle(ChatFormatting.RED));
            sendProgress(player);
            return;
        }
        p.completed.add(gid);
        p.claimed.add(gid);
        p.markDirty();
        grantLoot(player, q.reward, true);
        announce(player, q, true);
        scanInventory(player, p);
        processCompletions(player, p);
        sendProgress(player);
    }

    public static void flag(ServerPlayer player, String key, boolean value) {
        Progress p = PLAYERS.get(player.getUUID());
        if (p == null || !Rules.validFlag(Book.SERVER, key)) return;
        p.setManual(key, value);
        DIRTY_SYNC.put(player.getUUID(), true);
    }

    public static void pin(ServerPlayer player, String gid) {
        Progress p = PLAYERS.get(player.getUUID());
        if (p == null || Book.SERVER.quest(gid) == null) return;
        p.togglePin(gid);
        DIRTY_SYNC.put(player.getUUID(), true);
    }

    private static void processCompletions(ServerPlayer player, Progress p) {
        for (Quest q : Rules.recompute(Book.SERVER, p)) {
            if (p.claimed.add(q.globalId())) grantLoot(player, q.reward, false);
            announce(player, q, false);
        }
    }

    /** Проверка всех требований до изменения стэков; те же слоты, что и у scanInventory. */
    private static boolean takeItems(ServerPlayer player, Map<String, Integer> required) {
        List<ItemStack> slots = inventoryStacks(player);
        var inventory = player.getInventory();
        Map<String, Integer> available = new HashMap<>();
        slots.forEach(stack -> add(available, stack));
        for (var need : required.entrySet())
            if (available.getOrDefault(need.getKey(), 0) < need.getValue()) return false;
        for (var need : required.entrySet()) {
            int left = need.getValue();
            for (ItemStack stack : slots) {
                if (stack.isEmpty() || !BuiltInRegistries.ITEM.getKey(stack.getItem()).toString().equals(need.getKey())) continue;
                int take = Math.min(left, stack.getCount());
                stack.shrink(take);
                left -= take;
                if (left == 0) break;
            }
        }
        inventory.setChanged();
        player.containerMenu.broadcastChanges();
        return true;
    }

    private static void grantLoot(ServerPlayer player, Reward reward, boolean explicit) {
        if (reward == null || !reward.hasLoot()) return;
        for (Reward.Stack s : reward.items) {
            ResourceLocation loc = ResourceLocation.tryParse(s.id());
            if (loc == null) continue;
            BuiltInRegistries.ITEM.getOptional(loc).ifPresent(item -> {
                int left = s.count();
                while (left > 0) {
                    int n = Math.min(left, item.getDefaultMaxStackSize());
                    ItemHandlerHelper.giveItemToPlayer(player, new ItemStack(item, n));
                    left -= n;
                }
            });
        }
        if (reward.xp > 0) player.giveExperiencePoints(reward.xp);
    }

    private static void announce(ServerPlayer player, Quest q, boolean claimed) {
        Component text = Component.translatable("codex.msg.prefix")
                .withStyle(ChatFormatting.GOLD)
                .append(Component.translatable(claimed ? "codex.msg.claimed" : "codex.msg.done")
                        .withStyle(ChatFormatting.GRAY))
                .append(Component.translatable(q.title).withStyle(ChatFormatting.YELLOW));
        player.displayClientMessage(text, true);
    }

    // ------------------------------------------------------------- рассылка

    public static void sendBook(ServerPlayer player) {
        if (Book.SERVER.isEmpty()) return;
        byte[] sections = Payloads.gzip(Book.SERVER.rawSections());
        byte[] chapters = Payloads.gzip(String.join(Payloads.DOC_SEPARATOR, Book.SERVER.rawDocuments()));
        PacketDistributor.sendToPlayer(player, new Payloads.BookSync(sections, chapters));
    }

    public static void sendProgress(ServerPlayer player) {
        Progress p = PLAYERS.get(player.getUUID());
        if (p == null) return;
        PacketDistributor.sendToPlayer(player, new Payloads.ProgressSync(Payloads.gzip(p.snapshot().toString())));
    }

    public static void broadcastBook(MinecraftServer server) {
        for (ServerPlayer sp : server.getPlayerList().getPlayers()) sendBook(sp);
    }
}
