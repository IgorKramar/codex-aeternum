package ru.kramar.codex.net;

import net.minecraft.server.level.ServerPlayer;
import net.neoforged.neoforge.network.handling.IPayloadContext;
import ru.kramar.codex.server.ServerProgress;

/** Обработчики сообщений от клиента. Выполняются в потоке сервера. */
final class ServerHandlers {

    private ServerHandlers() {
    }

    static void onClaim(Payloads.Claim msg, IPayloadContext ctx) {
        ctx.enqueueWork(() -> {
            if (ctx.player() instanceof ServerPlayer sp) ServerProgress.claim(sp, msg.questId());
        });
    }

    static void onFlag(Payloads.Flag msg, IPayloadContext ctx) {
        ctx.enqueueWork(() -> {
            if (ctx.player() instanceof ServerPlayer sp) ServerProgress.flag(sp, msg.key(), msg.value());
        });
    }

    static void onPin(Payloads.Pin msg, IPayloadContext ctx) {
        ctx.enqueueWork(() -> {
            if (ctx.player() instanceof ServerPlayer sp) ServerProgress.pin(sp, msg.questId());
        });
    }
}
