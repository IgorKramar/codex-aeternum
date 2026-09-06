# -*- coding: utf-8 -*-
from dsl import chapter, Q, item, adv, check, chain

chapter(
    "mc_found", "colony", 10, "Основание колонии", "minecolonies:blockhuttownhall",
    "Ратуша, строитель и первые жители",
    [],
    chain([
        Q("supply", "Ящик снабжения", "minecolonies:supplychestdeployer", 0, 0,
          text=["Ящик на воде, лагерь на суше. Разворачивается в стартовую площадку с ратушей, "
                "строителем и запасом. Ставится один раз — выбирайте место, где хотите "
                "прожить сотню часов."],
          tasks=[item("minecolonies:supplychestdeployer")]),
        Q("townhall", "Ратуша", "minecolonies:blockhuttownhall", 0, 1,
          text=["Ратуша объявляет границы и открывает список жителей, статистику, "
                "разрешения. Её уровень — потолок населения."],
          tasks=[item("minecolonies:blockhuttownhall")],
          rewards=["Собственная колония"]),
        Q("buildtool", "Инструмент строителя", "minecolonies:sceptergold", 0, 2,
          text=["Призрак здания ставится на землю, поворачивается, подтверждается — и "
                "строитель берётся за работу. Очки показывают границы будущих стен."],
          tasks=[item("minecolonies:sceptergold"), item("minecolonies:build_goggles")]),
        Q("builder", "Строитель", "minecolonies:blockhutbuilder", 0, 3,
          text=["Первый и главный. Он строит всё, включая собственное улучшение. Свиток "
                "ресурсов покажет из инвентаря, чего ему не хватает прямо сейчас."],
          tasks=[item("minecolonies:blockhutbuilder"), item("minecolonies:resourcescroll")]),
        Q("citizen", "Дома жителей", "minecolonies:blockhutcitizen", 0, 4,
          text=["Дом — место для жителей. Таверна — первый приют и приманка для новых."],
          tasks=[item("minecolonies:blockhutcitizen", 2), item("minecolonies:blockhuttavern")]),
        Q("warehouse", "Склад и курьер", "minecolonies:blockhutwarehouse", 0, 5,
          text=["Склад хранит, стойки — полки, курьер носит. Без курьера колония стоит: "
                "сырьё лежит, рабочие ждут, вы удивляетесь."],
          tasks=[item("minecolonies:blockhutwarehouse"), item("minecolonies:blockhutdeliveryman"),
                 item("minecolonies:blockminecoloniesrack", 8)],
          rewards=["Работающая логистика колонии"]),
        Q("food", "Еда", "minecolonies:blockhutcook", 0, 6,
          text=["Голодный житель не работает. Повар готовит из того, что принесли фермер, "
                "пастух и рыбак; кухня и пекарь расширяют меню до десятков блюд."],
          tasks=[item("minecolonies:blockhutcook"), item("minecolonies:blockhutfarmer"), item("minecolonies:blockhutfield")]),
        Q("postbox", "Почтовый ящик", "minecolonies:blockpostbox", 1, 6,
          text=["Заказ со склада без беготни за курьером."],
          tasks=[item("minecolonies:blockpostbox")]),
        Q("hospital", "Больница и кладбище", "minecolonies:blockhuthospital", 0, 7,
          text=["Больница лечит. Кладбище хоронит — и с тотемом бессмертия возвращает."],
          tasks=[item("minecolonies:blockhuthospital"), item("minecolonies:blockhutgraveyard")]),
        Q("mystical", "Мистическое место", "minecolonies:blockhutmysticalsite", 1, 7,
          text=["Счастье. Счастливые работают быстрее и реже болеют."],
          tasks=[item("minecolonies:blockhutmysticalsite")], optional=True),
    ]),
)

chapter(
    "mc_production", "colony", 20, "Производство колонии", "minecolonies:blockhutsawmill",
    "От леса и шахты до кузницы и стеклодува",
    [
        "Колония умеет почти всё, если выстроить цепочки: лесоруб даёт брёвна, лесопилка — "
        "изделия, шахтёр — руду, плавильня — слитки, кузнец — инструменты. Ваша роль — "
        "решить, что делать первым.",
    ],
    chain([
        Q("lumberjack", "Лесоруб", "minecolonies:blockhutlumberjack", 0, 0,
          text=["Валит и сажает. Понимает все породы, включая BOP."],
          tasks=[item("minecolonies:blockhutlumberjack")]),
        Q("sawmill", "Лесопилка", "minecolonies:blockhutsawmill", 0, 1,
          text=["Доски, двери, лестницы, мебель — по заказам строителя."],
          tasks=[item("minecolonies:blockhutsawmill")]),
        Q("miner", "Шахтёр", "minecolonies:blockhutminer", -1, 1,
          text=["Роет шахту уровнями. Каменотёс режет камень, дробилка мелет булыжник "
                "в гравий и песок, просеиватель вытряхивает из земли редкости."],
          tasks=[item("minecolonies:blockhutminer"), item("minecolonies:blockhutstonemason"),
                 item("minecolonies:blockhutcrusher"), item("minecolonies:blockhutsifter")]),
        Q("smeltery", "Плавильни", "minecolonies:blockhutsmeltery", 0, 2,
          text=["Руда в слитки, камень и песок — в каменной. Уровень — число печей."],
          tasks=[item("minecolonies:blockhutsmeltery"), item("minecolonies:blockhutstonesmeltery")]),
        Q("blacksmith", "Кузница и механик", "minecolonies:blockhutblacksmith", 0, 3,
          text=["Кузнец — инструменты и броня, механик — механизмы, в том числе чужих модов. "
                "Стрелок, стеклодув, красильщик закрывают остальное."],
          tasks=[item("minecolonies:blockhutblacksmith"), item("minecolonies:blockhutmechanic"),
                 item("minecolonies:blockhutglassblower")]),
        Q("animals", "Животноводство", "minecolonies:blockhutshepherd", 0, 4,
          text=["Пастух, скотовод, свинопас, птичник, кролики, пчёлы, конюшня."],
          tasks=[item("minecolonies:blockhutshepherd"), item("minecolonies:blockhutcowboy"), item("minecolonies:blockhutbeekeeper")]),
        Q("plants", "Растениеводство", "minecolonies:blockhutplantation", 0, 5,
          text=["Плантация — тростник, бамбук, кактус. Флорист — цветы. Компостер — "
                "удобрение."],
          tasks=[item("minecolonies:blockhutplantation"), item("minecolonies:blockhutplantationfield"),
                 item("minecolonies:blockhutflorist"), item("minecolonies:blockhutcomposter")]),
        Q("fisherman", "Рыбак", "minecolonies:blockhutfisherman", 1, 5,
          text=["Рыба и то, что лежит на дне."],
          tasks=[item("minecolonies:blockhutfisherman")]),
        Q("nether", "Ходок в Нижний мир", "minecolonies:blockhutnetherworker", 0, 6,
          text=["Уходит в экспедицию и приносит кварц, золото, трофеи. Или не приносит."],
          tasks=[item("minecolonies:blockhutnetherworker")]),
        Q("quarry", "Карьер", "minecolonies:mediumquarry", 1, 6,
          text=["Яма до бедрока и всё, что в ней было."],
          tasks=[item("minecolonies:mediumquarry")], optional=True),
        Q("concrete", "Прочее производство", "minecolonies:blockhutconcretemixer", 2, 6,
          text=["Бетон, зелья, мистические ингредиенты."],
          tasks=[item("minecolonies:blockhutconcretemixer"), item("minecolonies:blockhutalchemist")], optional=True),
    ]),
)

chapter(
    "mc_research", "colony", 30, "Наука и развитие", "minecolonies:blockhutuniversity",
    "Университет, школа, библиотека и исследования",
    [],
    chain([
        Q("library", "Библиотека", "minecolonies:blockhutlibrary", 0, 0,
          text=["Учёные поднимают навыки остальным."],
          tasks=[item("minecolonies:blockhutlibrary")]),
        Q("school", "Школа", "minecolonies:blockhutschool", 1, 0,
          text=["Дети вырастают умнее родителей."],
          tasks=[item("minecolonies:blockhutschool")]),
        Q("university", "Университет", "minecolonies:blockhutuniversity", 0, 1,
          text=["Дерево исследований: цивилизация, технологии, война, снабжение. "
                "Пятые уровни зданий открываются только здесь."],
          tasks=[item("minecolonies:blockhutuniversity")],
          rewards=["Доступ к дереву исследований"]),
        Q("tome", "Древний том", "minecolonies:ancienttome", 1, 1,
          text=["Выпадает из налётчиков. Нужен исследованиям."],
          tasks=[item("minecolonies:ancienttome")]),
        Q("enchanter", "Зачарователь", "minecolonies:blockhutenchanter", 0, 2,
          text=["Собирает опыт с рабочих, делает книги и свитки: телепорт, усиление, "
                "вызов стражи."],
          tasks=[item("minecolonies:blockhutenchanter"), item("minecolonies:scroll_tp")]),
        Q("quests", "Задания колонии", "minecolonies:questlog", 1, 2,
          text=["Жители просят. Журнал помнит. Награды — опыт, редкости, жетоны."],
          tasks=[item("minecolonies:questlog"), item("minecolonies:adventure_token")]),
    ]),
)

chapter(
    "mc_military", "colony", 40, "Оборона", "minecolonies:blockhutbarracks",
    "Стража, казармы и отражение набегов",
    [
        "Варвары, пираты, мумии, норманны, амазонки — кто придёт, зависит от биома. "
        "Сколько и как часто — от размера колонии. Поздняя колония без гарнизона "
        "не доживает до утра.",
    ],
    chain([
        Q("guardtower", "Сторожевая башня", "minecolonies:blockhutguardtower", 0, 0,
          text=["Башня — стражник. Лучник или мечник, снаряжение со склада."],
          tasks=[item("minecolonies:blockhutguardtower", 2)]),
        Q("barracks", "Казармы", "minecolonies:blockhutbarracks", 0, 1,
          text=["До четырёх башен в одном здании. Гарнизон."],
          tasks=[item("minecolonies:blockhutbarracks"), item("minecolonies:blockhutbarrackstower")]),
        Q("training", "Обучение", "minecolonies:blockhutcombatacademy", 0, 2,
          text=["Академия — мечникам, стрельбище — лучникам."],
          tasks=[item("minecolonies:blockhutcombatacademy"), item("minecolonies:blockhutarchery")]),
        Q("walls", "Стены и ворота", "minecolonies:gate_wood", 0, 3,
          text=["Ворота открываются своим. Караулка держит участок стены."],
          tasks=[item("minecolonies:gate_wood"), item("minecolonies:blockhutgatehouse")]),
        Q("banner", "Знамя сбора", "minecolonies:banner_rally_guards", 1, 3,
          text=["Все стражи — в одну точку. Когда стену прорвали."],
          tasks=[item("minecolonies:banner_rally_guards")]),
        Q("raid", "Отражённый набег", "minecolonies:chiefsword", 0, 4,
          text=["Вождь падает — падает и его меч. Набеги объявляются в чате заранее; "
                "ночь потом длинная."],
          tasks=[item("minecolonies:chiefsword")],
          rewards=["Трофеи и уверенность в обороне"]),
    ]),
)

chapter(
    "mc_build", "colony", 50, "Строительство и стили", "structurize:sceptersteel",
    "Structurize, Domum Ornamentum и Multi-Piston",
    [],
    chain([
        Q("scepter", "Инструменты Structurize", "structurize:sceptersteel", 0, 0,
          text=["Скипетр выделяет, инструмент форм строит сферы и купола, кронциркуль мерит."],
          tasks=[item("structurize:sceptersteel"), item("structurize:shapetool"), item("structurize:caliper")]),
        Q("substitution", "Блоки-заменители", "structurize:blocksubstitution", 0, 1,
          text=["Воздух, твёрдое, жидкость, тег — схема сама подстраивается под рельеф."],
          tasks=[item("structurize:blocksubstitution"), item("structurize:blocksolidsubstitution")]),
        Q("cutter", "Резак архитектора", "domum_ornamentum:architectscutter", 0, 2,
          text=["Кирпич, черепица, фахверк, панели, светильники, двери, ковры — из любых "
                "материалов в сотнях сочетаний. На этом стоят все стили колонии."],
          tasks=[item("domum_ornamentum:architectscutter")],
          rewards=["Огромная палитра строительных материалов"]),
        Q("timberframe", "Фахверк", "domum_ornamentum:dynamic_timberframe", 1, 2,
          text=["Дерево и заполнение. Средневековье узнаётся по нему."],
          tasks=[item("domum_ornamentum:dynamic_timberframe")]),
        Q("multipiston", "Мультипоршень", "multipiston:multipistonblock", 0, 3,
          text=["Десятки блоков за раз на заданное расстояние. Подъёмные мосты, ворота, крыши."],
          tasks=[item("multipiston:multipistonblock")], optional=True),
        Q("decoration", "Контроллер декораций", "minecolonies:decorationcontroller", 1, 3,
          text=["Декор, который строитель возводит наравне со зданиями."],
          tasks=[item("minecolonies:decorationcontroller")], optional=True),
    ]),
)
