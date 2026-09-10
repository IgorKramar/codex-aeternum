# Codex Aeternum

**RU** · Квестовая книга для модпака Minecraft 1.21.1 / NeoForge 21.1 — по образцу
GTNH: разделы, главы, связанные задания с наградами, сдача предметов, серверный прогресс.

**EN** · A GTNH-style quest book for a Minecraft 1.21.1 / NeoForge 21.1 modpack: sections,
chapters, linked quests with rewards, item turn-ins and server-side progress.

---

## Русский

### Что внутри

- 19 разделов, 106 глав, 889 заданий по всем модам сборки: Create и все его аддоны,
  Immersive Engineering, Mekanism, PneumaticCraft, Industrial Foregoing, Powah,
  Refined Storage, MineColonies, Botania, Ars Nouveau, Iron's Spellbooks,
  Mystical Agriculture, Apotheosis, Ad Astra, Cataclysm, Aether, Twilight Forest,
  Eternal Tales, кухня, мебель, мелочи.
- **Сюжетные линии** — сквозные цепочки через несколько модов с настоящими развилками.
- **Космос, магия и охота** — три больших раздела: полёты на планеты Ad Astra,
  три школы магии и десять боссов Cataclysm.
- **Испытания и эндгейм** — сдача ресурсов с наградами, от 64 брёвен до 1024 прецизионных
  механизмов и всех девяти кристаллов измерений разом.
- Прогресс считается сам: предметы, достижения, посещённые измерения и биомы, просмотренные
  сцены Ponder. Клик по предмету открывает рецепт в JEI.
- Два языка: русский и английский. Переключается языком игры.

### Как это работает

Мод ставится на клиент и на сервер (в одиночной игре сервер встроенный). Сервер ведёт
прогресс каждого игрока в `<мир>/codex/<uuid>.json`, проверяет цели и выдаёт награды.
Клиент рисует книгу и отправляет действия. Без мода на сервере книга работает
как справочник: прогресс хранится локально, награды не выдаются.

| Действие | Клавиша |
|---|---|
| Открыть или закрыть книгу | `K` (настраивается), или `/codex` |
| Панорамирование | перетаскивание ЛКМ |
| Масштаб | колесо мыши |
| Выбрать задание | ЛКМ по узлу |
| Закладка | ПКМ по узлу |
| Вернуть вид в центр | `Home` |
| Рецепт / применение предмета | ЛКМ / ПКМ по иконке цели |

### Установка

Готовый jar — на странице [релизов](https://github.com/IgorKramar/codex-aeternum/releases).
Кладётся в папку `mods` клиента и сервера.

### Сборка

Нужен только JDK 21 — остальное Gradle скачает сам:

```
./gradlew build
```

Результат — `build/libs/codex-aeternum-1.0.0.jar`. Версия мода, версия NeoForge и версия
JEI задаются в `gradle.properties`; версия оттуда же попадает в манифест мода.

### Содержимое книги

Задания описаны на Python в `tools/c_*.py`, английские тексты — в `tools/en_*.py`,
награды ключевых заданий — в `tools/rewards.py`. Сборщик выпускает JSON глав
и оба языковых файла и проверяет каждый идентификатор предмета и достижения:

```
python3 tools/build_book.py
```

Списки существующих идентификаторов лежат в `tools/valid_ids.txt`,
`tools/valid_adv.txt` и `tools/valid_biomes.txt`. После смены состава сборки их
пересобирают по папке модов и клиентскому jar:

```
python3 tools/scan_pack.py <папка mods> <клиентский jar Minecraft>
```

Списки строятся по моделям предметов, состояниям блоков, рецептам, тегам и
таблицам добычи, а не по языковым файлам: в них годами остаются ключи
предметов, которых в реестре давно нет. Переменные окружения `VALID_IDS` и
`VALID_ADV` позволяют подставить другие файлы, не трогая репозиторий.

Главы лежат в `assets/codex/book/chapters/` и продублированы в `data/codex/book/`
для сервера, поэтому их можно переопределить ресурспаком или датапаком.

---

## English

### What's inside

- 19 sections, 106 chapters, 889 quests covering every content mod in the pack: Create and
  all its add-ons, Immersive Engineering, Mekanism, PneumaticCraft, Industrial Foregoing,
  Powah, Refined Storage, MineColonies, Botania, Ars Nouveau, Iron's Spellbooks,
  Mystical Agriculture, Apotheosis, Ad Astra, Cataclysm, Aether, Twilight Forest,
  Eternal Tales, cooking, furniture and utilities.
- **Storylines** — cross-mod chains with real branching and convergence.
- **Space, magic and the hunt** — three large sections: Ad Astra planetary flight,
  three schools of magic and ten Cataclysm bosses.
- **Trials and Endgame** — resource turn-ins with rewards, from 64 logs up to 1024
  precision mechanisms and all nine dimension crystals at once.
- Progress tracks itself: items, advancements, visited dimensions and biomes, watched
  Ponder scenes. Clicking an item opens its recipe in JEI.
- Two languages, Russian and English, following the game language.

### How it works

The mod goes on both client and server (single-player uses the integrated server). The
server keeps each player's progress in `<world>/codex/<uuid>.json`, verifies objectives
and grants rewards. The client renders the book and sends actions. Without the mod on the
server the book runs as a reference: progress is stored locally and no rewards are given.

| Action | Key |
|---|---|
| Open or close the book | `K` (rebindable), or `/codex` |
| Pan | drag with LMB |
| Zoom | mouse wheel |
| Select a quest | LMB on a node |
| Pin | RMB on a node |
| Reset view | `Home` |
| Recipe / uses of an item | LMB / RMB on an objective icon |

### Installing

Grab the jar from the [releases page](https://github.com/IgorKramar/codex-aeternum/releases)
and drop it into the `mods` folder of both client and server.

### Building

JDK 21 is the only prerequisite; Gradle fetches the rest:

```
./gradlew build
```

Output: `build/libs/codex-aeternum-1.0.0.jar`. Mod, NeoForge and JEI versions live in
`gradle.properties`, and the mod version is injected into the mod manifest from there.

### Book content

Quests are described in Python in `tools/c_*.py`, English text in `tools/en_*.py`, key
rewards in `tools/rewards.py`. The builder emits chapter JSON plus both language files and
validates every item and advancement id:

```
python3 tools/build_book.py
```

The id lists live in `tools/valid_ids.txt`, `tools/valid_adv.txt` and
`tools/valid_biomes.txt`. After the pack changes, regenerate them from the mods folder
and the Minecraft client jar:

```
python3 tools/scan_pack.py <mods folder> <Minecraft client jar>
```

The lists are built from item models, blockstates, recipes, tags and loot tables rather
than language files: those keep keys for items that left the registry years ago. The
`VALID_IDS` and `VALID_ADV` environment variables point the builder at other files
without touching the repository.

Chapters live in `assets/codex/book/chapters/` and are mirrored to `data/codex/book/`
for the server, so a resource pack or data pack can override them.

## License

MIT — see `LICENSE`.
