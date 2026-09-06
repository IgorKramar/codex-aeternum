package ru.kramar.codex;

import net.minecraft.server.level.ServerPlayer;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.event.AddReloadListenerEvent;
import net.neoforged.neoforge.event.OnDatapackSyncEvent;
import net.neoforged.neoforge.event.entity.player.PlayerEvent;
import net.neoforged.neoforge.event.server.ServerStoppingEvent;
import net.neoforged.neoforge.event.tick.PlayerTickEvent;
import net.neoforged.neoforge.network.event.RegisterPayloadHandlersEvent;
import ru.kramar.codex.book.Book;
import ru.kramar.codex.net.Payloads;
import ru.kramar.codex.server.ServerProgress;

/** Точка входа. Общая часть: книга на сервере, сеть, прогресс игроков. */
@Mod(Codex.ID)
public final class Codex {

    public static final String ID = "codex";

    public Codex(IEventBus modBus) {
        modBus.addListener(Payloads::register);
    }

    /** Серверные обработчики; на встроенном сервере одиночной игры работают так же. */
    @EventBusSubscriber(modid = ID)
    public static final class ServerEvents {

        private ServerEvents() {
        }

        @SubscribeEvent
        public static void onReload(AddReloadListenerEvent event) {
            event.addListener(Book.SERVER.listener());
        }

        @SubscribeEvent
        public static void onDatapackSync(OnDatapackSyncEvent event) {
            ServerProgress.onBookLoaded();
            if (event.getPlayer() == null) {
                ServerProgress.broadcastBook(event.getPlayerList().getServer());
            }
        }

        @SubscribeEvent
        public static void onLogin(PlayerEvent.PlayerLoggedInEvent event) {
            if (event.getEntity() instanceof ServerPlayer sp) ServerProgress.onLogin(sp);
        }

        @SubscribeEvent
        public static void onLogout(PlayerEvent.PlayerLoggedOutEvent event) {
            if (event.getEntity() instanceof ServerPlayer sp) ServerProgress.onLogout(sp);
        }

        @SubscribeEvent
        public static void onPlayerTick(PlayerTickEvent.Post event) {
            if (event.getEntity() instanceof ServerPlayer sp) ServerProgress.tick(sp);
        }

        @SubscribeEvent
        public static void onStopping(ServerStoppingEvent event) {
            ServerProgress.onServerStopping();
        }
    }
}
