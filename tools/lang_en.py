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
    "magic": "Magic", "tech2": "Industry II", "space": "Space", "hunt": "The Hunt",
}
SECTIONS_RU = {
    "start": "Начало пути", "story": "Сюжетные линии", "world": "Мир и разведка",
    "create": "Create: механика", "createx": "Create: расширения", "ie": "Immersive Engineering",
    "mek": "Mekanism", "storage": "Хранение и логистика", "colony": "Колония", "dim": "Иные миры",
    "eternal": "Eternal Tales", "life": "Быт и уют", "trials": "Испытания", "final": "Финал",
    "endgame": "Эндгейм", "more": "За пределами пути",
    "magic": "Магия", "tech2": "Индустрия II", "space": "Космос", "hunt": "Охота",
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

UI_RU.update({
    'codex.ui.maps': 'Карты', 'codex.ui.fit': 'Вписать',
    'codex.ui.overview': 'Обзор', 'codex.ui.next_match': 'Далее',
    'codex.ui.close_detail': 'Скрыть', 'codex.ui.close': 'Закрыть',
    'codex.ui.legend': 'Зелёный: готово · Золото: доступно · Пунктир: любой путь · ◇: необязательно',
    'codex.ui.navigation': 'Перетаскивайте карту мышью. Колесо меняет масштаб под курсором; Home показывает всю карту. ПКМ закрепляет задание. Поиск: Enter или F3 переходит к следующему результату. Ссылки в задании ведут к предпосылкам и следующим шагам.',
    'codex.ui.optional': 'Необязательная ветка',
    'codex.ui.requires_all': 'Нужно выполнить всё:',
    'codex.ui.requires_any': 'Нужно выполнить хотя бы одно:',
    'codex.ui.opens_next': 'Открывает следующие шаги:',
})
UI_EN.update({
    'codex.ui.maps': 'Maps', 'codex.ui.fit': 'Fit',
    'codex.ui.overview': 'Overview', 'codex.ui.next_match': 'Next',
    'codex.ui.close_detail': 'Hide', 'codex.ui.close': 'Close',
    'codex.ui.legend': 'Green: done · Gold: available · Dashed: any path · ◇: optional',
    'codex.ui.navigation': 'Drag to pan. Scroll to zoom at the cursor; Home fits the map. Right-click pins a quest. Search: Enter or F3 jumps to the next match. Quest links lead to prerequisites and next steps.',
    'codex.ui.optional': 'Optional branch',
    'codex.ui.requires_all': 'Complete all:',
    'codex.ui.requires_any': 'Complete at least one:',
    'codex.ui.opens_next': 'Opens next steps:',
})

UI_RU.update({
    'codex.ui.cover': 'Обложка',
    'codex.welcome.title': 'Codex Aethernum',
    'codex.welcome.eyebrow': 'ПУТЕВОДИТЕЛЬ ПО ВАШЕМУ МИРУ',
    'codex.welcome.purpose': 'У каждого большого открытия есть первый шаг. Кодекс поможет пройти путь от первой мастерской до сложных производств, дальних экспедиций и магии — даже если вы впервые знакомитесь с модами.',
    'codex.welcome.promise': 'Выберите интересную ветку. Внутри — подготовка, порядок действий и объяснение результата. Связи между заданиями подскажут, какие знания и инструменты понадобятся дальше.',
    'codex.welcome.progress': '%s открытий в книге · %s уже сделано',
    'codex.welcome.how': 'КАК ЧИТАТЬ КОДЕКС',
    'codex.welcome.step1.title': 'Найдите свой путь',
    'codex.welcome.step1.body': 'Выберите карту и откройте узел. Сплошная связь требует предыдущего шага, пунктир предлагает выбор. Ромб отмечает необязательную ветку. Поиск найдёт название задания или предмет.',
    'codex.welcome.step2.title': 'Превратите знание в дело',
    'codex.welcome.step2.body': 'Прочитайте описание и выполните цели. Предметы и достижения учитываются автоматически. Ручную цель отмечайте после проверки результата. Кнопка сдачи забирает указанные ресурсы и выдаёт награду.',
    'codex.welcome.step3.title': 'Держите карту под рукой',
    'codex.welcome.step3.body': 'Перетаскивайте карту, приближайте колесом, нажмите Home для общего вида. ПКМ закрепляет задание. Клик по предмету открывает JEI; ссылки ведут к соседним шагам. Клавиша книги и Esc закрывают экран.',
    'codex.welcome.open': 'Открыть книгу',
    'codex.welcome.continue': 'Продолжить путь',
    'codex.welcome.beginning': 'К началу пути',
})
UI_EN.update({
    'codex.ui.cover': 'Cover',
    'codex.welcome.title': 'Codex Aethernum',
    'codex.welcome.eyebrow': 'A FIELD GUIDE TO YOUR WORLD',
    'codex.welcome.purpose': 'Every great discovery begins with a first step. The Codex guides you from your first workshop to complex production lines, distant expeditions and magic, even if these mods are entirely new to you.',
    'codex.welcome.promise': 'Choose a branch that interests you. Each quest explains preparation, actions and results. Connections show which knowledge and tools you will need next.',
    'codex.welcome.progress': '%s discoveries in the book · %s completed',
    'codex.welcome.how': 'HOW TO READ THE CODEX',
    'codex.welcome.step1.title': 'Find your path',
    'codex.welcome.step1.body': 'Choose a map and open a node. Solid links require previous steps; dashed links offer alternatives. Diamonds mark optional branches. Search finds quest titles or item identifiers.',
    'codex.welcome.step2.title': 'Put knowledge to work',
    'codex.welcome.step2.body': 'Read the explanation and complete its objectives. Items and advancements are tracked automatically. Tick manual goals after checking the result. Turn-in buttons consume the listed resources and give rewards.',
    'codex.welcome.step3.title': 'Keep your bearings',
    'codex.welcome.step3.body': 'Drag the map, zoom with the wheel and press Home for an overview. Right-click pins a quest. Click an item for JEI recipes; follow links to related steps. The book key and Esc close the screen.',
    'codex.welcome.open': 'Open the book',
    'codex.welcome.continue': 'Continue your journey',
    'codex.welcome.beginning': 'The first steps',
})

UI_RU['codex.ui.inventory_rules'] = 'Обычные предметные цели запоминают наибольший запас каждого предмета, замеченный в инвентаре. Разные предметы можно показать по очереди; уже учтённую машину снимать не нужно. Для количества больше одного соберите нужный запас одного предмета вместе. Цели «Сдать» требуют все указанные ресурсы при сдаче и забирают их.'
UI_EN['codex.ui.inventory_rules'] = 'Ordinary item goals remember the largest inventory quantity seen for each item. Different items can be shown separately; recorded machinery need not be dismantled. For counts above one, gather the required quantity of that item together. Turn-in goals require all listed supplies at claim time and consume them.'
