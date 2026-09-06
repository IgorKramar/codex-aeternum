# -*- coding: utf-8 -*-
"""Английские тексты книги и строки интерфейса на обоих языках.

Переводы глав лежат в модулях en_*.py и собираются здесь в словарь EN:
EN[chapter_id] = {"title", "subtitle", "intro": [...],
                  "quests": {quest_id: {"title", "text": [...], "tasks": [...], "rewards": [...]}}}
"""
import importlib
import os

HERE = os.path.dirname(os.path.abspath(__file__))

EN = {}
for name in sorted(os.listdir(HERE)):
    if name.startswith("en_") and name.endswith(".py"):
        mod = importlib.import_module(name[:-3])
        EN.update(getattr(mod, "EN", {}))

SECTIONS_EN = {
    "start": "Getting Started", "story": "Storylines", "world": "World & Exploration",
    "create": "Create: Mechanics", "createx": "Create: Extensions", "ie": "Immersive Engineering",
    "mek": "Mekanism", "storage": "Storage & Logistics", "colony": "Colony", "dim": "Other Worlds",
    "eternal": "Eternal Tales", "life": "Home & Comfort", "trials": "Trials", "final": "Finale",
    "endgame": "Endgame", "more": "Beyond the Path",
}
SECTIONS_RU = {
    "start": "Начало пути", "story": "Сюжетные линии", "world": "Мир и разведка",
    "create": "Create: механика", "createx": "Create: расширения", "ie": "Immersive Engineering",
    "mek": "Mekanism", "storage": "Хранение и логистика", "colony": "Колония", "dim": "Иные миры",
    "eternal": "Eternal Tales", "life": "Быт и уют", "trials": "Испытания", "final": "Финал",
    "endgame": "Эндгейм", "more": "За пределами пути",
}

UI_RU = {
    "key.categories.codex": "Кодекс",
    "key.codex.open": "Открыть Кодекс",
    "codex.title": "Кодекс",
    "codex.ui.search": "Поиск…",
    "codex.ui.not_loaded": "Книга не загружена",
    "codex.ui.mode.server": "сервер",
    "codex.ui.mode.local": "локально",
    "codex.ui.state.done": "Выполнено",
    "codex.ui.state.done_claimed": "Выполнено, награда получена",
    "codex.ui.state.claimable": "Цели выполнены — заберите награду",
    "codex.ui.state.open": "Доступно",
    "codex.ui.state.locked": "Заблокировано",
    "codex.ui.tasks": "Цели",
    "codex.ui.reward": "Награда",
    "codex.ui.xp": "Опыт: %s",
    "codex.ui.claim": "Получить награду",
    "codex.ui.claim_consume": "Сдать предметы и получить награду",
    "codex.ui.local_notice": "Без мода на сервере предметы не выдаются и не забираются.",
    "codex.ui.jei_hint": "ЛКМ по предмету — рецепт, ПКМ — где применяется.",
    "codex.ui.read": "[✔] Прочитано",
    "codex.ui.mark_read": "[ ] Отметить прочитанным",
    "codex.ui.task.consume": "Сдать: %s",
    "codex.ui.task.advancement": "Достижение: %s",
    "codex.ui.task.dimension": "Побывать в измерении: %s",
    "codex.ui.task.biome": "Найти биом: %s",
    "codex.ui.task.check": "Отметить вручную",
    "codex.ui.task.ponder": "Посмотреть сцену Ponder для: %s",
    "codex.ui.tip.claim": "Награда ждёт — откройте задание",
    "codex.ui.tip.locked": "Требует предыдущие задания",
    "codex.ui.tip.lore": "Справочный узел",
    "codex.toast.done": "Кодекс: задание выполнено",
    "codex.msg.prefix": "Кодекс: ",
    "codex.msg.done": "задание выполнено — ",
    "codex.msg.claimed": "награда получена — ",
    "codex.msg.not_enough": "Кодекс: не хватает предметов для сдачи",
}
UI_EN = {
    "key.categories.codex": "Codex",
    "key.codex.open": "Open Codex",
    "codex.title": "Codex",
    "codex.ui.search": "Search…",
    "codex.ui.not_loaded": "Book not loaded",
    "codex.ui.mode.server": "server",
    "codex.ui.mode.local": "local",
    "codex.ui.state.done": "Completed",
    "codex.ui.state.done_claimed": "Completed, reward claimed",
    "codex.ui.state.claimable": "Objectives met — claim your reward",
    "codex.ui.state.open": "Available",
    "codex.ui.state.locked": "Locked",
    "codex.ui.tasks": "Objectives",
    "codex.ui.reward": "Reward",
    "codex.ui.xp": "Experience: %s",
    "codex.ui.claim": "Claim reward",
    "codex.ui.claim_consume": "Turn in items and claim reward",
    "codex.ui.local_notice": "Without the mod on the server, items are neither given nor taken.",
    "codex.ui.jei_hint": "Left-click an item for its recipe, right-click for its uses.",
    "codex.ui.read": "[✔] Read",
    "codex.ui.mark_read": "[ ] Mark as read",
    "codex.ui.task.consume": "Turn in: %s",
    "codex.ui.task.advancement": "Advancement: %s",
    "codex.ui.task.dimension": "Visit dimension: %s",
    "codex.ui.task.biome": "Find biome: %s",
    "codex.ui.task.check": "Mark manually",
    "codex.ui.task.ponder": "Watch the Ponder scene for: %s",
    "codex.ui.tip.claim": "A reward is waiting — open the quest",
    "codex.ui.tip.locked": "Requires previous quests",
    "codex.ui.tip.lore": "Reference node",
    "codex.toast.done": "Codex: quest completed",
    "codex.msg.prefix": "Codex: ",
    "codex.msg.done": "quest completed — ",
    "codex.msg.claimed": "reward claimed — ",
    "codex.msg.not_enough": "Codex: not enough items to turn in",
}
