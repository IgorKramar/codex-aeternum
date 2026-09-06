# Codex Aeternum

**RU** · Квестовая книга для модпака Minecraft 1.21.1 / NeoForge 21.1 — по образцу
GTNH: разделы, главы, связанные задания с наградами, сдача предметов, серверный прогресс.

**EN** · A GTNH-style quest book for a Minecraft 1.21.1 / NeoForge 21.1 modpack: sections,
chapters, linked quests with rewards, item turn-ins and server-side progress.

---

## Русский

### Что внутри

- 15 разделов, 85 глав, 718 заданий по всем модам сборки: Create и все его аддоны,
  Immersive Engineering, Mekanism, Refined Storage, MineColonies, Aether, Twilight Forest,
  Eternal Tales, кухня, мебель, мелочи.
- **Сюжетные линии** — сквозные цепочки через несколько модов с настоящими развилками.
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

### Сборка

Gradle не нужен: мод компилируется напрямую против библиотек, которые уже скачал
PrismLauncher.

```
./build.sh
```

Переменные `PRISM`, `JAVA_HOME_21`, `NEO_VER`, `MC_ART`, `MODS` переопределяют пути.
Результат — `build/libs/codex-aeternum-1.0.0.jar`.

### Содержимое книги

Задания описаны на Python в `tools/c_*.py`, английские тексты — в `tools/en_*.py`,
награды ключевых заданий — в `tools/rewards.py`. Сборщик выпускает JSON глав
и оба языковых файла и проверяет каждый идентификатор предмета и достижения:

```
VALID_IDS=<файл со списком предметов> VALID_ADV=<файл с достижениями> python3 tools/build_book.py
```

Главы лежат в `assets/codex/book/chapters/` и продублированы в `data/codex/book/`
для сервера, поэтому их можно переопределить ресурспаком или датапаком.

---

## English

### What's inside

- 15 sections, 85 chapters, 718 quests covering every content mod in the pack: Create and
  all its add-ons, Immersive Engineering, Mekanism, Refined Storage, MineColonies, Aether,
  Twilight Forest, Eternal Tales, cooking, furniture and utilities.
- **Storylines** — cross-mod chains with real branching and convergence.
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

### Building

No Gradle: the mod compiles directly against the libraries PrismLauncher already
downloaded.

```
./build.sh
```

`PRISM`, `JAVA_HOME_21`, `NEO_VER`, `MC_ART` and `MODS` override the paths.
Output: `build/libs/codex-aeternum-1.0.0.jar`.

### Book content

Quests are described in Python in `tools/c_*.py`, English text in `tools/en_*.py`, key
rewards in `tools/rewards.py`. The builder emits chapter JSON plus both language files and
validates every item and advancement id:

```
VALID_IDS=<item id list> VALID_ADV=<advancement id list> python3 tools/build_book.py
```

Chapters live in `assets/codex/book/chapters/` and are mirrored to `data/codex/book/`
for the server, so a resource pack or data pack can override them.

## License

MIT — see `LICENSE`.
