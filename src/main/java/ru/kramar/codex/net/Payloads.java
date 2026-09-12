package ru.kramar.codex.net;

import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.ResourceLocation;
import net.neoforged.neoforge.network.event.RegisterPayloadHandlersEvent;
import net.neoforged.neoforge.network.registration.PayloadRegistrar;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.zip.GZIPInputStream;
import java.util.zip.GZIPOutputStream;

/** Сетевые сообщения книги. Все помечены как необязательные: без мода на сервере клиент работает сам. */
public final class Payloads {
    public static final int MAX_UNCOMPRESSED_BYTES = 32_000_000;

    private Payloads() {
    }

    private static <T extends CustomPacketPayload> CustomPacketPayload.Type<T> makeType(String name) {
        return new CustomPacketPayload.Type<>(ResourceLocation.fromNamespaceAndPath("codex", name));
    }

    /** Сервер → клиент: полное содержимое книги (сжатый JSON). */
    public record BookSync(byte[] sections, byte[] chapters) implements CustomPacketPayload {
        public static final Type<BookSync> TYPE = makeType("book");
        public static final StreamCodec<RegistryFriendlyByteBuf, BookSync> CODEC = StreamCodec.composite(
                ByteBufCodecs.byteArray(4_000_000), BookSync::sections,
                ByteBufCodecs.byteArray(4_000_000), BookSync::chapters,
                BookSync::new);

        @Override
        public Type<BookSync> type() {
            return TYPE;
        }
    }

    /** Сервер → клиент: состояние прогресса игрока (сжатый JSON). */
    public record ProgressSync(byte[] json) implements CustomPacketPayload {
        public static final Type<ProgressSync> TYPE = makeType("progress");
        public static final StreamCodec<RegistryFriendlyByteBuf, ProgressSync> CODEC = StreamCodec.composite(
                ByteBufCodecs.byteArray(4_000_000), ProgressSync::json,
                ProgressSync::new);

        @Override
        public Type<ProgressSync> type() {
            return TYPE;
        }
    }

    /** Клиент → сервер: забрать награду за задание. */
    public record Claim(String questId) implements CustomPacketPayload {
        public static final Type<Claim> TYPE = makeType("claim");
        public static final StreamCodec<RegistryFriendlyByteBuf, Claim> CODEC = StreamCodec.composite(
                ByteBufCodecs.STRING_UTF8, Claim::questId,
                Claim::new);

        @Override
        public Type<Claim> type() {
            return TYPE;
        }
    }

    /** Клиент → сервер: ручная отметка или просмотренная сцена Ponder. */
    public record Flag(String key, boolean value) implements CustomPacketPayload {
        public static final Type<Flag> TYPE = makeType("flag");
        public static final StreamCodec<RegistryFriendlyByteBuf, Flag> CODEC = StreamCodec.composite(
                ByteBufCodecs.STRING_UTF8, Flag::key,
                ByteBufCodecs.BOOL, Flag::value,
                Flag::new);

        @Override
        public Type<Flag> type() {
            return TYPE;
        }
    }

    /** Клиент → сервер: переключить закладку. */
    public record Pin(String questId) implements CustomPacketPayload {
        public static final Type<Pin> TYPE = makeType("pin");
        public static final StreamCodec<RegistryFriendlyByteBuf, Pin> CODEC = StreamCodec.composite(
                ByteBufCodecs.STRING_UTF8, Pin::questId,
                Pin::new);

        @Override
        public Type<Pin> type() {
            return TYPE;
        }
    }

    public static void register(RegisterPayloadHandlersEvent event) {
        PayloadRegistrar r = event.registrar("codex").versioned("2").optional();
        r.playToClient(BookSync.TYPE, BookSync.CODEC, ClientHandlers::onBook);
        r.playToClient(ProgressSync.TYPE, ProgressSync.CODEC, ClientHandlers::onProgress);
        r.playToServer(Claim.TYPE, Claim.CODEC, ServerHandlers::onClaim);
        r.playToServer(Flag.TYPE, Flag.CODEC, ServerHandlers::onFlag);
        r.playToServer(Pin.TYPE, Pin.CODEC, ServerHandlers::onPin);
    }

    /** Разделитель документов внутри одного сжатого блока. */
    public static final String DOC_SEPARATOR = "\n<<<codex-doc>>>\n";

    public static byte[] gzip(String text) {
        try (ByteArrayOutputStream bos = new ByteArrayOutputStream();
             GZIPOutputStream gz = new GZIPOutputStream(bos)) {
            gz.write(text.getBytes(StandardCharsets.UTF_8));
            gz.finish();
            return bos.toByteArray();
        } catch (IOException e) {
            throw new IllegalStateException(e);
        }
    }

    public static String gunzip(byte[] data) {
        try (GZIPInputStream gz = new GZIPInputStream(new ByteArrayInputStream(data));
             ByteArrayOutputStream bos = new ByteArrayOutputStream()) {
            byte[] buf = new byte[8192];
            int n;
            while ((n = gz.read(buf)) > 0) {
                if (bos.size() > MAX_UNCOMPRESSED_BYTES - n)
                    throw new IOException("Слишком большой распакованный пакет кодекса");
                bos.write(buf, 0, n);
            }
            return bos.toString(StandardCharsets.UTF_8);
        } catch (IOException e) {
            throw new IllegalStateException(e);
        }
    }
}
