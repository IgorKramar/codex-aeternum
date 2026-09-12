package ru.kramar.codex.client;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import net.minecraft.client.gui.screens.Screen;
import net.neoforged.fml.loading.FMLPaths;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;

/** Настройки этого клиента: `config/codex-client.json`. Порядок прохождения хранится не здесь, а в прогрессе игрока. */
public final class ClientOptions {
    private static final Logger LOG = LoggerFactory.getLogger("codex");
    private static final Gson GSON = new GsonBuilder().setPrettyPrinting().create();
    private static final Path FILE = FMLPaths.CONFIGDIR.get().resolve("codex-client.json");
    private static ClientOptions instance;

    public boolean itemTooltips = true;
    public boolean toasts = true;
    public boolean coverFirst = true;

    public static ClientOptions get() {
        if (instance == null) instance = load();
        return instance;
    }

    /** Экран, который открывают клавиша книги и команда /codex. */
    public static Screen opening() {
        return get().coverFirst ? new CodexWelcomeScreen() : new CodexScreen();
    }

    private static ClientOptions load() {
        try {
            if (Files.isRegularFile(FILE)) {
                ClientOptions loaded = GSON.fromJson(Files.readString(FILE, StandardCharsets.UTF_8), ClientOptions.class);
                if (loaded != null) return loaded;
            }
        } catch (Exception ex) {
            LOG.warn("Кодекс: настройки клиента {} не читаются, используются значения по умолчанию", FILE, ex);
        }
        return new ClientOptions();
    }

    public void save() {
        try {
            Files.createDirectories(FILE.getParent());
            Files.writeString(FILE, GSON.toJson(this), StandardCharsets.UTF_8);
        } catch (Exception ex) {
            LOG.warn("Кодекс: не удалось сохранить настройки клиента {}", FILE, ex);
        }
    }
}
