package ru.kramar.codex.net;

import com.google.gson.JsonParser;
import net.neoforged.neoforge.network.handling.IPayloadContext;
import ru.kramar.codex.book.Book;
import ru.kramar.codex.progress.Tracker;

import java.util.ArrayList;
import java.util.List;

/** Обработчики сообщений от сервера. Выполняются в потоке клиента. */
final class ClientHandlers {

    private ClientHandlers() {
    }

    static void onBook(Payloads.BookSync msg, IPayloadContext ctx) {
        ctx.enqueueWork(() -> {
            String sections = Payloads.gunzip(msg.sections());
            String joined = Payloads.gunzip(msg.chapters());
            List<String> docs = new ArrayList<>();
            for (String d : joined.split(java.util.regex.Pattern.quote(Payloads.DOC_SEPARATOR))) {
                if (!d.isBlank()) docs.add(d);
            }
            Book.REMOTE.loadFromDocuments(sections, docs);
            Tracker.enterServerMode();
        });
    }

    static void onProgress(Payloads.ProgressSync msg, IPayloadContext ctx) {
        ctx.enqueueWork(() -> {
            String json = Payloads.gunzip(msg.json());
            Tracker.applyServerProgress(JsonParser.parseString(json).getAsJsonObject());
        });
    }
}
