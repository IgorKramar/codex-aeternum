# -*- coding: utf-8 -*-
from dsl import chapter, Q, item, adv, check, chain

chapter(
    "ie_start", "ie", 10, "Молот и кокс", "immersiveengineering:hammer",
    "С чего начинается Immersive Engineering",
    [],
    chain([
        Q("manual", "Инженерное руководство", "immersiveengineering:manual", 0, 0,
          text=["Книга с чертежами. Каждая многоблочная машина показана в трёх измерениях, "
                "слой за слоем. Доменную печь без неё собирают со второго раза; экскаватор — "
                "никогда."],
          tasks=[item("immersiveengineering:manual")]),
        Q("hammer", "Инженерный молот", "immersiveengineering:hammer", 0, 1,
          text=["Удар по многоблоку — и груда кирпича становится машиной. Молот же делает "
                "пластины из слитков на верстаке, поворачивает блоки и разбирает лишнее. "
                "Кусачки снимают провода, отвёртка настраивает."],
          tasks=[item("immersiveengineering:hammer"), item("immersiveengineering:wirecutter"),
                 item("immersiveengineering:screwdriver")]),
        Q("coke_oven", "Коксовая печь", "immersiveengineering:coke_oven", 0, 2,
          text=[
              "Двадцать семь коксовых кирпичей кубом, удар молотом — и печь дышит. Уголь "
              "входит, кокс выходит, а снизу капает креозот — чёрное масло, на котором "
              "стоит весь мод. Первая настоящая промышленность в этой сборке пахнет именно так.",
          ],
          tasks=[item("immersiveengineering:cokebrick", 27), item("immersiveengineering:coal_coke", 16)],
          rewards=["Кокс и креозотовое масло"]),
        Q("treated", "Обработанная древесина", "immersiveengineering:treated_wood_horizontal", 0, 3,
          text=["Доски, вымоченные в креозоте, не гниют и держат вес машин. Заливайте в бочке "
                "или в чане — и делайте сразу много: попросят все."],
          tasks=[item("immersiveengineering:treated_wood_horizontal", 32)]),
        Q("blast", "Доменная печь", "immersiveengineering:blast_furnace", 0, 4,
          text=[
              "Ещё один куб, на этот раз из доменного кирпича. Железо и кокс внутрь — сталь "
              "наружу, медленно, с оранжевым светом в щелях. Подогреватель ускоряет, "
              "улучшенная печь удваивает. Сталь — материал всего, что вы построите дальше.",
          ],
          tasks=[item("immersiveengineering:blastbrick", 27), item("immersiveengineering:ingot_steel", 16)],
          rewards=["Сталь — материал всей средней и поздней игры"]),
        Q("workbench", "Инженерный верстак", "immersiveengineering:workbench", 0, 5,
          text=["Чертежи — язык этого верстака: компоненты, патроны, детали турелей, "
                "электроника. Он же улучшает дрель, пилу, револьвер и рельсотрон."],
          tasks=[item("immersiveengineering:workbench"), item("immersiveengineering:blueprint")]),
        Q("components", "Компоненты", "immersiveengineering:component_steel", 1, 5,
          text=["Железные, стальные, электронные — расходные детали любой машины. "
                "Электронным нужна медная проволока и красный камень, продвинутым — золото."],
          tasks=[item("immersiveengineering:component_iron", 8), item("immersiveengineering:component_steel", 8),
                 item("immersiveengineering:component_electronic", 4)]),
        Q("scaffold", "Каркас и лестницы", "immersiveengineering:steel_scaffolding_standard", 2, 5,
          text=["Леса, ограждения, трапы. Индустриальный стиль сборки держится на них — "
                "буквально."],
          tasks=[item("immersiveengineering:steel_scaffolding_standard", 16)], optional=True),
    ]),
)

chapter(
    "ie_power", "ie", 20, "Электросеть", "immersiveengineering:wirecoil_copper",
    "Провода, напряжения, генераторы и трансформаторы",
    [],
    chain([
        Q("wire_lv", "Низкое напряжение", "immersiveengineering:wirecoil_copper", 0, 0,
          text=["Медь, 2048 в тик. Коннектор на машину, провод от коннектора к коннектору "
                "правым щелчком. Изолированный — можно трогать. Голый — нельзя."],
          tasks=[item("immersiveengineering:wirecoil_copper"), item("immersiveengineering:connector_lv", 2)]),
        Q("dynamo", "Динамо и водяное колесо", "immersiveengineering:dynamo", 0, 1,
          text=["Динамо крутит что угодно: водяное колесо в потоке, ветряк на высоте. "
                "Колесу нужна текущая вода по всей высоте, ветряку — небо."],
          tasks=[item("immersiveengineering:dynamo"), item("immersiveengineering:watermill")]),
        Q("windmill_ie", "Ветряк", "immersiveengineering:windmill", 1, 1,
          text=["Лопасти и паруса. Выше — сильнее, в дождь — слабее."],
          tasks=[item("immersiveengineering:windmill"), item("immersiveengineering:windmill_blade", 8)]),
        Q("capacitor", "Конденсаторы", "immersiveengineering:capacitor_lv", 0, 2,
          text=["Сто тысяч, миллион, четыре миллиона. Стороны задаются отвёрткой: вход, "
                "выход, ничего."],
          tasks=[item("immersiveengineering:capacitor_lv")]),
        Q("wire_mv", "Среднее напряжение", "immersiveengineering:wirecoil_electrum", 0, 3,
          text=["Электрум, 8192 в тик. Золото и серебро в доменной печи или смесителе."],
          tasks=[item("immersiveengineering:wirecoil_electrum"), item("immersiveengineering:connector_mv", 2)]),
        Q("wire_hv", "Высокое напряжение", "immersiveengineering:wirecoil_steel", 0, 4,
          text=["Сталь, 32768 в тик, через опоры на километры. Реле — промежуточная опора, "
                "которая ничего не ест. ЛЭП над лесом — самое красивое, что есть в IE."],
          tasks=[item("immersiveengineering:wirecoil_steel"), item("immersiveengineering:connector_hv", 2)]),
        Q("transformer", "Трансформаторы", "immersiveengineering:transformer", 0, 5,
          text=["LV к MV, MV к HV. Направление — по тому, с какой стороны подключён провод."],
          tasks=[item("immersiveengineering:transformer"), item("immersiveengineering:transformer_hv")]),
        Q("safety", "Техника безопасности", "immersiveengineering:armor_faraday_chestplate", 1, 5,
          text=["Костюм Фарадея против тока, наушники против рёва дизеля, автомат защиты "
                "против всего сразу. Вольтметр покажет, что вы сделали не так."],
          tasks=[item("immersiveengineering:armor_faraday_chestplate"), item("immersiveengineering:voltmeter"),
                 item("immersiveengineering:breaker_switch")]),
        Q("thermo", "Термоэлектрический генератор", "immersiveengineering:thermoelectric_generator", -1, 4,
          deps=["capacitor"],
          text=["Лёд с одной стороны, лава с другой — и ток течёт из разницы. Мало, "
                "но вечно."],
          tasks=[item("immersiveengineering:thermoelectric_generator")], optional=True),
        Q("lightning", "Громоотвод", "immersiveengineering:lightning_rod", -1, 5,
          deps=["wire_hv"],
          text=["Башня, которая ждёт грозы. Удар — и конденсаторы полны на неделю."],
          tasks=[item("immersiveengineering:lightning_rod")], optional=True),
    ]),
)

chapter(
    "ie_machines", "ie", 30, "Многоблочные машины", "immersiveengineering:crusher",
    "Дробилка, пресс, дуговая печь и экскаватор",
    [],
    chain([
        Q("crusher_ie", "Дробилка", "immersiveengineering:crusher", 0, 0,
          text=["Пять на три на три, валы с зубьями, рёв. Удваивает руду и мелет всё, "
                "что бросили сверху, — включая мобов, если они неудачно ходят."],
          tasks=[item("immersiveengineering:crusher")],
          rewards=["Промышленное удвоение руды"]),
        Q("press", "Металлический пресс", "immersiveengineering:metal_press", 0, 1,
          text=["Формы не расходуются: пластины, стержни, шестерни, проволока, гильзы, "
                "упаковка. Сделали форму раз — и навсегда."],
          tasks=[item("immersiveengineering:metal_press"), item("immersiveengineering:mold_plate"),
                 item("immersiveengineering:mold_rod"), item("immersiveengineering:mold_wire")]),
        Q("arc", "Дуговая печь", "immersiveengineering:arc_furnace", 0, 2,
          text=["Электроды опускаются, металл вспыхивает. Сталь быстрее домны, лом — "
                "обратно в слитки. Графитовые электроды сгорают и требуют замены."],
          tasks=[item("immersiveengineering:arc_furnace"), item("immersiveengineering:graphite_electrode")]),
        Q("assembler", "Сборщик", "immersiveengineering:assembler", 1, 2,
          text=["Три рецепта верстака одновременно из общего буфера. Автоверстак делает "
                "то же по чертежу."],
          tasks=[item("immersiveengineering:assembler"), item("immersiveengineering:auto_workbench")]),
        Q("sample", "Разведка руды", "immersiveengineering:sample_drill", 0, 3,
          text=["Под каждым чанком лежит жила. Инструменты геолога берут пробу на глаз, "
                "буровая — точно. Керн покажет, что там и сколько осталось."],
          tasks=[item("immersiveengineering:survey_tools"), item("immersiveengineering:sample_drill"),
                 item("immersiveengineering:coresample")]),
        Q("excavator", "Экскаватор", "immersiveengineering:excavator", 0, 4,
          text=[
              "Ковшовое колесо размером с дом медленно поворачивается над жилой, и руда "
              "сыплется на конвейер. Жила беднеет, но не кончается никогда. Это машина, "
              "ради которой строят всё остальное.",
          ],
          tasks=[item("immersiveengineering:excavator"), item("immersiveengineering:bucket_wheel")],
          rewards=["Бесконечная добыча руды"]),
        Q("storage", "Хранилища", "immersiveengineering:silo", 1, 4,
          text=["Силос — гора одного предмета. Цистерна — озеро одной жидкости."],
          tasks=[item("immersiveengineering:silo"), item("immersiveengineering:tank")]),
        Q("conveyor", "Конвейеры", "immersiveengineering:conveyor_basic", 0, 5,
          text=["Обычные, с выгрузкой, с извлечением, вертикальные, разделители, "
                "с крышкой. Сортировщик разводит поток, пакетировщик считает."],
          tasks=[item("immersiveengineering:conveyor_basic", 8), item("immersiveengineering:sorter"),
                 item("immersiveengineering:item_batcher")]),
    ]),
)

chapter(
    "ie_chemistry", "ie", 40, "Химия и топливо", "immersiveengineering:refinery",
    "Растительное масло, этанол, биодизель и полимеры",
    [],
    chain([
        Q("squeezer", "Пресс-выжималка", "immersiveengineering:squeezer", 0, 0,
          text=["Семена в масло, растения в сок, жмых на топливо."],
          tasks=[item("immersiveengineering:squeezer")]),
        Q("fermenter", "Ферментёр", "immersiveengineering:fermenter", 0, 1,
          text=["Всё, что растёт, бродит в этанол. Тростник — лучше всего."],
          tasks=[item("immersiveengineering:fermenter")]),
        Q("refinery_ie", "Нефтеперегонный завод", "immersiveengineering:refinery", 0, 2,
          text=["Этанол с маслом — биодизель. Форсированный — злее."],
          tasks=[item("immersiveengineering:refinery"), item("immersiveengineering:biodiesel_bucket")]),
        Q("diesel", "Дизель-генератор", "immersiveengineering:diesel_generator", 0, 3,
          text=["Самый мощный генератор мода. Ревёт так, что нужны наушники, жрёт топливо "
                "и не спрашивает, готовы ли вы к такому количеству энергии."],
          tasks=[item("immersiveengineering:diesel_generator")],
          rewards=["Основной источник энергии поздней игры IE"]),
        Q("mixer", "Промышленный смеситель", "immersiveengineering:mixer", 1, 2,
          deps=["fermenter"],
          text=["Бетон, зелья ведрами, растворы для переработки."],
          tasks=[item("immersiveengineering:mixer")]),
        Q("bottling", "Разливочная машина", "immersiveengineering:bottling_machine", 2, 2,
          deps=["fermenter"],
          text=["Бутылки, вёдра, канистры — на конвейере, без рук."],
          tasks=[item("immersiveengineering:bottling_machine")]),
        Q("duroplast", "Дуропласт", "immersiveengineering:plate_duroplast", 0, 4,
          text=["Полимер из химических отходов. Продвинутые детали и броня."],
          tasks=[item("immersiveengineering:plate_duroplast", 4)]),
        Q("cloche", "Садовая клош", "immersiveengineering:cloche", 1, 4,
          deps=["squeezer"],
          text=["Стеклянный колпак, под которым растёт что угодно: семена, почва, вода, "
                "энергия — и урожай без грядок. Работает с коноплёй IE и культурами "
                "Farmer's Delight."],
          tasks=[item("immersiveengineering:cloche")],
          rewards=["Автоматическое земледелие"]),
    ]),
)

chapter(
    "ie_gear", "ie", 50, "Снаряжение инженера", "immersiveengineering:revolver",
    "Оружие, инструменты и броня",
    [],
    chain([
        Q("drill_ie", "Дрель", "immersiveengineering:drill", 0, 0,
          text=["Три на три за проход, от энергии. Стальная головка — надолго. Улучшения "
                "в верстаке: водостойкость, бак, зона."],
          tasks=[item("immersiveengineering:drill"), item("immersiveengineering:drillhead_steel")]),
        Q("buzzsaw", "Бензопила", "immersiveengineering:buzzsaw", 1, 0,
          text=["Валит деревья. С нужным диском — не только деревья."],
          tasks=[item("immersiveengineering:buzzsaw")]),
        Q("revolver", "Револьвер", "immersiveengineering:revolver", 0, 1,
          text=["Собирается из деталей по чертежу. Бронебойные, разрывные, зажигательные, "
                "картечь, «волчья стая», зельевые. Улучшения — электромагнит, барабан, пара."],
          tasks=[item("immersiveengineering:revolver"), item("immersiveengineering:gunpart_hammer")]),
        Q("railgun", "Рельсотрон", "immersiveengineering:railgun", 0, 2,
          text=["Стержни любого металла на энергии. Держите кнопку — заряд растёт."],
          tasks=[item("immersiveengineering:railgun")]),
        Q("chemthrower", "Химомёт", "immersiveengineering:chemthrower", 1, 2,
          text=["Креозот горит, кислота ест, вода тушит. Против толпы."],
          tasks=[item("immersiveengineering:chemthrower")]),
        Q("powerpack", "Энергоранец", "immersiveengineering:powerpack", 0, 3,
          text=["Питает всё ручное. Зарядная станция — дома."],
          tasks=[item("immersiveengineering:powerpack"), item("immersiveengineering:charging_station")]),
        Q("skyhook", "Небесный крюк", "immersiveengineering:skyhook", 1, 3,
          text=["Цепляетесь за натянутый трос и летите вдоль него. Канатная дорога между "
                "базами — и минута пути вместо десяти."],
          tasks=[item("immersiveengineering:skyhook"), item("immersiveengineering:wirecoil_structure_steel")]),
        Q("steel_armor", "Стальная броня", "immersiveengineering:armor_steel_chestplate", 0, 4,
          text=["Между железом и алмазом, из того, чего у вас тонны."],
          tasks=[item("immersiveengineering:armor_steel_chestplate")]),
        Q("turret", "Турели", "immersiveengineering:turret_gun", 1, 4,
          deps=["revolver"],
          text=["Пулемётная ест патроны, химическая — жидкость. Список целей, энергия, "
                "и база защищает себя сама."],
          tasks=[item("immersiveengineering:turret_gun"), item("immersiveengineering:turret_chem")]),
        Q("misc_ie", "Мелочи", "immersiveengineering:floodlight", 2, 4,
          text=["Прожектор, электрофонарь, загрузчик чанков, ремонтный набор."],
          tasks=[item("immersiveengineering:floodlight"), item("immersiveengineering:electric_lantern"),
                 item("immersiveengineering:maintenance_kit")], optional=True),
        Q("shaders", "Шейдеры", "immersiveengineering:shader_bag_common", 3, 4,
          text=["Раскраски оружия и машин. Из мешков и с побеждённых."],
          tasks=[item("immersiveengineering:shader_bag_common")], optional=True),
    ]),
)
