package ru.kramar.codex.client;

import com.mojang.blaze3d.platform.InputConstants;
import com.mojang.brigadier.builder.LiteralArgumentBuilder;
import net.minecraft.client.KeyMapping;
import net.minecraft.client.Minecraft;
import net.minecraft.commands.CommandSourceStack;
import net.minecraft.commands.Commands;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.client.event.ClientPlayerNetworkEvent;
import net.neoforged.neoforge.client.event.ClientTickEvent;
import net.neoforged.neoforge.client.event.RegisterClientCommandsEvent;
import net.neoforged.neoforge.client.event.RegisterClientReloadListenersEvent;
import net.neoforged.neoforge.client.event.RegisterKeyMappingsEvent;
import net.neoforged.neoforge.client.event.RenderTooltipEvent;
import org.lwjgl.glfw.GLFW;
import ru.kramar.codex.Codex;
import ru.kramar.codex.book.Book;
import ru.kramar.codex.progress.Tracker;

/** Клиентская часть: клавиша, экран, локальный режим. */
@Mod(value = Codex.ID, dist = Dist.CLIENT)
public final class CodexClient {

    public static final KeyMapping OPEN_KEY = new KeyMapping(
            "key.codex.open", InputConstants.Type.KEYSYM, GLFW.GLFW_KEY_K, "key.categories.codex");

    public CodexClient(IEventBus modBus) {
        modBus.addListener(this::registerKeys);
        modBus.addListener(this::registerReloadListeners);
    }

    private void registerKeys(RegisterKeyMappingsEvent event) {
        event.register(OPEN_KEY);
    }

    private void registerReloadListeners(RegisterClientReloadListenersEvent event) {
        event.registerReloadListener(Book.CLIENT.listener());
        event.registerReloadListener(Hints.listener());
    }

    @EventBusSubscriber(modid = Codex.ID, value = Dist.CLIENT)
    public static final class GameEvents {

        private GameEvents() {
        }

        @SubscribeEvent
        public static void onTooltipColor(RenderTooltipEvent.Color event) {
            var screen = Minecraft.getInstance().screen;
            if (!(screen instanceof CodexScreen) && !(screen instanceof CodexWelcomeScreen)) return;
            event.setBackgroundStart(Theme.PANEL);
            event.setBackgroundEnd(Theme.PANEL_DEEP);
            event.setBorderStart(Theme.BORDER_LIGHT);
            event.setBorderEnd(Theme.TURQUOISE);
        }

        @SubscribeEvent
        public static void onClientTick(ClientTickEvent.Post event) {
            Minecraft mc = Minecraft.getInstance();
            while (OPEN_KEY.consumeClick()) {
                if (mc.screen == null && mc.player != null) mc.setScreen(ClientOptions.opening());
            }
            Tracker.clientTick();
        }

        @SubscribeEvent
        public static void onRegisterCommands(RegisterClientCommandsEvent event) {
            LiteralArgumentBuilder<CommandSourceStack> root = Commands.literal("codex")
                    .executes(ctx -> {
                        Minecraft.getInstance().tell(() ->
                                Minecraft.getInstance().setScreen(ClientOptions.opening()));
                        return 1;
                    });
            event.getDispatcher().register(root);
        }

        @SubscribeEvent
        public static void onLogin(ClientPlayerNetworkEvent.LoggingIn event) {
            Tracker.onJoin();
        }

        @SubscribeEvent
        public static void onLogout(ClientPlayerNetworkEvent.LoggingOut event) {
            Tracker.onLeave();
        }
    }
}
