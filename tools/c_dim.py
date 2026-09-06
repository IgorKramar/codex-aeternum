# -*- coding: utf-8 -*-
from dsl import chapter, Q, item, adv, dim, biome, check, chain

chapter(
    "dim_nether", "dim", 10, "Нижний мир", "minecraft:netherrack",
    "Что берут из Нижнего мира моды сборки",
    [
        "Нижний мир здесь ванильный. Изменилось не место — изменился спрос: ифриты нужны "
        "Create, кварц — Refined Storage, незерит — сразу троим. Каждая вылазка вниз теперь "
        "имеет список покупок.",
    ],
    chain([
        Q("portal", "Портал", "minecraft:obsidian", 0, 0,
          text=["Обсидиан, огниво, шаг. Сундук с припасами Carry On пронесёт через портал "
                "прямо в руках."],
          tasks=[dim("minecraft:the_nether", "Побывать в Нижнем мире")]),
        Q("blaze", "Ифриты", "minecraft:blaze_rod", 0, 1,
          text=["Стержни — Create, зельям и ритуалам Eternal Tales. Пустая горелка ловит "
                "самого духа: подойдите к ифриту и щёлкните. Он не против."],
          tasks=[item("minecraft:blaze_rod", 16), item("create:empty_blaze_burner")]),
        Q("quartz", "Адский кварц", "minecraft:quartz", 1, 1,
          text=["Кремний для сети, розовый кварц для Create, детали для IE. Стопка — "
                "минимум."],
          tasks=[item("minecraft:quartz", 64)]),
        Q("ancient", "Незерит", "minecraft:netherite_ingot", 0, 2,
          text=["Водолазный комплект, незеритовая сталь для пушек, верх инструментов. "
                "Копайте на пятнадцатом."],
          tasks=[item("minecraft:netherite_ingot")]),
        Q("fortress", "Крепость и бастион", "minecraft:nether_brick", 1, 2,
          text=["Крепость — ифриты и варты. Бастион — золото и лом. Между ними — постройки "
                "Eternal Tales, которых в ванили не было."],
          tasks=[item("minecraft:nether_wart", 16)]),
        Q("nether_et", "Часовая башня пиглинов", "minecraft:clock", 0, 3,
          text=["Башня с часами и четырьмя замками, которую построили не пиглины. Ключи — "
                "у надзирателей Пылающих Пустошей. Внутри — след Янтаря и Вулканеха."],
          tasks=[check("Найти часовую башню в Нижнем мире")], optional=True),
    ]),
)

chapter(
    "dim_end", "dim", 20, "Край", "minecraft:end_portal_frame",
    "Дракон, эндер-жемчуг и путь дальше",
    [],
    chain([
        Q("stronghold", "Крепость", "minecraft:ender_eye", 0, 0,
          text=["Оки эндера ведут к порталу. Жемчуг понадобится и потом: левититу "
                "и телепортам."],
          tasks=[item("minecraft:ender_eye", 12)]),
        Q("dragon", "Дракон Края", "minecraft:dragon_head", 0, 1,
          text=["После него — острова, элитры, дыхание в бутылках и яйцо, которое просят "
                "несколько рецептов."],
          tasks=[dim("minecraft:the_end", "Побывать в Крае"), item("minecraft:dragon_breath")]),
        Q("elytra", "Элитры", "minecraft:elytra", 0, 2,
          text=["Лучший транспорт до гравитационного модулятора."],
          tasks=[item("minecraft:elytra")]),
        Q("shulker", "Шалкеры", "minecraft:shulker_shell", 1, 2,
          text=["Ящики и несколько рецептов модов."],
          tasks=[item("minecraft:shulker_shell", 4)]),
        Q("end_et", "Врата Эдемских Садов", "minecraft:end_stone", 0, 3,
          text=["Где-то в Крае стоит портал в Эдем. Его откроет солнечный камень из "
                "Чистилища — но это уже история Eternal Tales."],
          tasks=[check("Прочитано")], optional=True),
    ]),
)

chapter(
    "dim_aether", "dim", 30, "Aether", "aether:aether_portal_frame",
    "Небесное измерение: подземелья, гравитит и валькирии",
    [],
    chain([
        Q("aether_portal", "Портал в Aether", "aether:aether_portal_frame", 0, 0,
          text=["Рамка из светящегося камня, ведро воды вместо огня. Наверху острова, "
                "внизу — бездна, которая выбрасывает обратно в обычный мир. Возьмите "
                "что-нибудь для мягкой посадки."],
          tasks=[dim("aether:the_aether", "Побывать в Aether")]),
        Q("holystone", "Первые инструменты", "aether:holystone_pickaxe", 0, 1,
          text=["Небесный корень, священный камень, янтарь. Осколок янтаря — и топливо, "
                "и лекарство."],
          tasks=[item("aether:skyroot_pickaxe"), item("aether:holystone_pickaxe"), item("aether:ambrosium_shard", 16)]),
        Q("zanite", "Занит", "aether:zanite_gemstone", 0, 2,
          text=["Местное железо, которое ускоряется по мере износа."],
          tasks=[item("aether:zanite_gemstone", 8), item("aether:zanite_pickaxe")]),
        Q("altar", "Алтарь", "aether:altar", 0, 3,
          text=["Зачаровывает на янтаре и превращает гравитит в зачарованный. Морозильник "
                "рядом делает лёд и ледяной камень."],
          tasks=[item("aether:altar"), item("aether:freezer")]),
        Q("gravitite", "Гравитит", "aether:enchanted_gravitite", 0, 4,
          text=["Броня, в которой прыгают через дом, и инструменты, поднимающие блоки "
                "в воздух. Лучший материал неба."],
          tasks=[item("aether:enchanted_gravitite", 8), item("aether:gravitite_chestplate")]),
        Q("moa", "Моа", "aether:blue_moa_egg", -1, 3,
          deps=["holystone"],
          text=["Яйцо в инкубатор, птенца — лепестками. Взрослый моа прыгает в воздухе "
                "несколько раз подряд: синий три, белый четыре, чёрный восемь."],
          tasks=[item("aether:incubator"), item("aether:blue_moa_egg"), item("aether:aechor_petal", 4)]),
        Q("bronze_dungeon", "Бронзовое подземелье", "aether:bronze_dungeon_key", 0, 5,
          text=["Слайдер: каменный куб, который разгоняется и таранит. Бейте в глаз, "
                "когда он замирает."],
          tasks=[item("aether:bronze_dungeon_key"), item("aether:victory_medal")],
          rewards=["Первые артефакты Aether"]),
        Q("silver_dungeon", "Серебряное подземелье", "aether:silver_dungeon_key", 0, 6,
          text=["Валькирии не дают копьё просто так. Возьмите его с боем — и Королева "
                "выйдет сама."],
          tasks=[item("aether:valkyrie_lance"), item("aether:silver_dungeon_key"), item("aether:valkyrie_helmet")]),
        Q("gold_dungeon", "Золотое подземелье", "aether:gold_dungeon_key", 0, 7,
          text=["Солнечный дух горит, и пока горит — неуязвим. Снежки. Много снежков. "
                "Потом — молот Кингбдогза и доспехи феникса."],
          tasks=[item("aether:gold_dungeon_key"), item("aether:hammer_of_kingbdogz")],
          rewards=["Полное прохождение Aether"]),
        Q("accessories", "Аксессуары", "aether:golden_ring", 1, 5,
          deps=["altar"],
          text=["Кольца, подвески, плащи, перчатки. Ледяная подвеска морозит воду под "
                "ногами, золотое перо замедляет падение, плащ прячет."],
          tasks=[item("aether:golden_ring"), item("aether:ice_pendant"), item("aether:golden_feather")]),
        Q("lore", "Книга преданий", "aether:book_of_lore", 2, 5,
          deps=["altar"],
          text=["Положите предмет — и книга расскажет о нём."],
          tasks=[item("aether:book_of_lore")], optional=True),
    ]),
)

chapter(
    "dim_twilight", "dim", 40, "Сумеречный лес", "twilightforest:twilight_portal_miniature_structure",
    "Строгая цепочка боссов от Наги до Йети",
    [],
    chain([
        Q("tf_portal", "Портал в Сумеречный лес", "twilightforest:twilight_portal_miniature_structure", 0, 0,
          text=["Яма два на два, вода, цветы по краю, алмаз в воду. Молния — и вечный "
                "вечер."],
          tasks=[dim("twilightforest:twilight_forest", "Побывать в Сумеречном лесу")]),
        Q("tf_start", "Первые шаги", "twilightforest:ironwood_ingot", 0, 1,
          text=["Живой корень и железное дерево — первые материалы. Факельные ягоды светят, "
                "личинка ставит светильники, магическая карта показывает, куда идти."],
          tasks=[item("twilightforest:liveroot", 4), item("twilightforest:ironwood_ingot", 4), item("twilightforest:magic_map_focus")]),
        Q("naga", "Нага", "twilightforest:naga_trophy", 0, 2,
          text=["Двор с колоннами. Она бросается и крушит их; прячьтесь и бейте."],
          tasks=[item("twilightforest:naga_trophy"), item("twilightforest:naga_scale", 4)],
          rewards=["Открывает башню Лича"]),
        Q("lich", "Лич", "twilightforest:lich_trophy", 0, 3,
          text=["Три фазы: щит и шары, прислужники, ближний бой. Шары отражайте обратно — "
                "иначе щит не снять."],
          tasks=[item("twilightforest:lich_trophy"), item("twilightforest:zombie_scepter")],
          rewards=["Открывает лабиринт, болото и тёмный лес"]),
        Q("minoshroom", "Миношрум", "twilightforest:minoshroom_trophy", -1, 4,
          text=["В глубине лабиринта. Кирка-разрушитель ломает его стены."],
          tasks=[item("twilightforest:minoshroom_trophy"), item("twilightforest:mazebreaker_pickaxe")]),
        Q("hydra", "Гидра", "twilightforest:hydra_trophy", 0, 4,
          text=["Три головы. Отрубленная отрастает, если не добить. Кровь и слёзы — "
                "в огненный слиток и меч."],
          tasks=[item("twilightforest:hydra_trophy"), item("twilightforest:fiery_blood", 4), item("twilightforest:fiery_sword")]),
        Q("knight_phantom", "Призрачный рыцарь", "twilightforest:knight_phantom_trophy", 1, 4,
          text=["Четыре призрака волнами в крепости тёмного леса. Найтметалл — оттуда."],
          tasks=[item("twilightforest:knight_phantom_trophy"), item("twilightforest:knightmetal_ingot", 4)]),
        Q("ur_ghast", "Ур-Гаст", "twilightforest:ur_ghast_trophy", 0, 5,
          deps=["knight_phantom"],
          text=["Тёмная башня, ловушки для гастов, кармаинт. Эксперимент 115 — еда, "
                "которая не кончается."],
          tasks=[item("twilightforest:ur_ghast_trophy"), item("twilightforest:carminite", 4), item("twilightforest:experiment_115")]),
        Q("snow_queen", "Снежная королева", "twilightforest:snow_queen_trophy", 0, 6,
          deps=["ur_ghast", "hydra"],
          text=["Сначала Альфа-йети и его шкура. Потом ледяная башня. Стеклянный меч "
                "бьёт один раз — но как."],
          tasks=[item("twilightforest:alpha_yeti_fur", 4), item("twilightforest:snow_queen_trophy"), item("twilightforest:arctic_chestplate")]),
        Q("giants", "Облачный замок", "twilightforest:giant_pickaxe", 0, 7,
          text=["Плодородная почва, волшебные бобы, стебель до облаков. Наверху — великаны "
                "и кирка, которая ломает четыре на четыре."],
          tasks=[item("twilightforest:uberous_soil"), item("twilightforest:magic_beans"), item("twilightforest:giant_pickaxe")]),
        Q("cinders", "Светоч углей", "twilightforest:lamp_of_cinders", 0, 8,
          text=["Выжигает шипы, закрывающие последние земли. Дальше — только лес."],
          tasks=[item("twilightforest:lamp_of_cinders")],
          rewards=["Полное прохождение Сумеречного леса"]),
        Q("uncrafting", "Стол разбора", "twilightforest:uncrafting_table", 1, 2,
          deps=["tf_start"],
          text=["Разбирает предметы обратно. В этой сборке — оружие; пользуйтесь осознанно."],
          tasks=[item("twilightforest:uncrafting_table")], optional=True),
        Q("charms", "Обереги", "twilightforest:charm_of_life_1", 2, 2,
          deps=["tf_start"],
          text=["Жизни — воскрешает. Сохранения — оставляет инвентарь. Оба одноразовые."],
          tasks=[item("twilightforest:charm_of_life_1"), item("twilightforest:charm_of_keeping_1")], optional=True),
        Q("trophy", "Пьедестал трофеев", "twilightforest:trophy_pedestal", 1, 8,
          deps=["ur_ghast"],
          text=["Трофей на пьедестал — усиление и открытые области."],
          tasks=[item("twilightforest:trophy_pedestal")]),
    ]),
)
