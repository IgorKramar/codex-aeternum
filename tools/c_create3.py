# -*- coding: utf-8 -*-
from dsl import chapter, Q, item, adv, check, chain

chapter(
    "create_packages", "create", 80, "Посылки и фабрика", "create:packager",
    "Логистика Create 6: упаковки, склад и заказы",
    [
        "Шестая версия Create принесла почту. Предметы укладываются в картонные посылки, "
        "посылки едут по цепям и лентам, а склад отвечает на заказы, не спрашивая, кто "
        "заказал. В этом есть что-то от старой доброй почтовой станции — и что-то от "
        "завода, который сам знает, чего ему не хватает.",
    ],
    chain([
        Q("cardboard", "Картон", "create:cardboard", 0, 0,
          text=["Бумага под прессом. Из картона — посылки, фильтры посылок и доспех, "
                "в котором вас не замечают мобы. Последнее не шутка."],
          tasks=[item("create:cardboard", 8)]),
        Q("packager", "Упаковщик", "create:packager", 0, 1,
          text=["Берёт из инвентаря, складывает в коробку, надписывает адрес. По заказу "
                "или по вашей просьбе. Перепаковщик потом пересобирает содержимое."],
          tasks=[item("create:packager")]),
        Q("frogport", "Фрогпорт", "create:package_frogport", -1, 2,
          text=["Лягушка на цепи. Ловит посылки, отправляет посылки, выгружает в сундук. "
                "Квакает, если прислушаться."],
          tasks=[item("create:package_frogport", 2)]),
        Q("chain_conveyor", "Цепной конвейер", "create:chain_conveyor", 0, 2,
          text=["Цепь между узлами на любое расстояние. По ней едут коробки — и вы, если "
                "ухватитесь. Самый дешёвый способ связать далёкие постройки."],
          tasks=[item("create:chain_conveyor", 4)]),
        Q("stock_link", "Связь склада", "create:stock_link", 1, 2,
          text=["Вешается на хранилище и докладывает тикеру, что там лежит."],
          tasks=[item("create:stock_link")]),
        Q("ticker", "Тикер заказов", "create:stock_ticker", 0, 3,
          deps=["stock_link", "packager", "frogport"],
          text=["Весь ассортимент склада в одном окне. Заказали — упаковщики собрали, "
                "лягушки принесли. Список покупок запоминает то, что вы заказываете "
                "каждый раз."],
          tasks=[item("create:stock_ticker"), item("create:shopping_list")],
          rewards=["Единая точка выдачи любых материалов"]),
        Q("requester", "Запросчик", "create:redstone_requester", 1, 3,
          deps=["ticker"],
          text=["Сигнал — и склад присылает набор. Машина, которая сама заказывает себе сырьё."],
          tasks=[item("create:redstone_requester")]),
        Q("factory_gauge", "Фабричный указатель", "create:factory_gauge", 0, 4,
          deps=["ticker"],
          text=[
              "Указатель знает, что должно лежать на выходе, и сколько. Если не хватает — "
              "заказывает недостающее у соседних указателей, а те — у своих. Собранная на "
              "указателях фабрика не ждёт команд: она планирует.",
          ],
          tasks=[item("create:factory_gauge", 2)],
          rewards=["Самопланирующееся производство"]),
        Q("shop", "Лавка", "create:red_table_cloth", -1, 4,
          deps=["ticker"],
          text=["Скатерть, звонок, тикер — и это магазин. На сервере из таких вырастают рынки."],
          tasks=[item("create:red_table_cloth"), item("create:desk_bell")], optional=True),
        Q("postbox", "Почтовые ящики", "create:red_postbox", 1, 4,
          deps=["frogport"],
          text=["Адрес пишется на посылке. Ящик с этим адресом её примет — где бы ни стоял."],
          tasks=[item("create:red_postbox")], optional=True),
    ]),
)

chapter(
    "create_trains", "create", 90, "Поезда", "create:track",
    "Пути, станции, расписания и Steam 'n' Rails",
    [],
    chain([
        Q("sturdy", "Прочный лист", "create:sturdy_sheet", 0, 0,
          text=["Обсидиан через пресс и жёрнов. Материал для того, что должно выдерживать "
                "вес поезда."],
          tasks=[item("create:sturdy_sheet", 8)]),
        Q("railway_casing", "Железнодорожный корпус", "create:railway_casing", 0, 1,
          text=["Станции, сигналы, тележки, штурвал. Всё железнодорожное начинается с него."],
          tasks=[item("create:railway_casing", 4)]),
        Q("track", "Пути", "create:track", 0, 2,
          text=["Две точки — и Create сам проложит между ними кривую, подъём или петлю. "
                "Пути можно вести по воздуху; опоры вырастут сами. Тридцать два — "
                "на первую ветку до шахты."],
          tasks=[item("create:track", 32)]),
        Q("station", "Станция", "create:track_station", 0, 3,
          text=["Здесь поезд собирают и здесь он останавливается. Тележки на путь, корпус "
                "сверху, кнопка «Собрать» — и состав существует."],
          tasks=[item("create:track_station", 2)]),
        Q("bogey", "Тележки", "create:large_bogey", -1, 3,
          text=["Малая для вагонов, большая для локомотива. Steam 'n' Rails добавляет "
                "двухосные и узкоколейные."],
          tasks=[item("create:large_bogey", 2)]),
        Q("train", "Первый состав", "create:controls", 0, 4,
          deps=["station", "bogey"],
          text=[
              "Локомотиву нужна сила на борту: котёл с двигателем или, позже, электромотор. "
              "Штурвал — ваш, сиденье — машиниста. В первый раз, когда поезд тронется "
              "с вами внутри, вы поймёте, зачем всё это было.",
          ],
          tasks=[item("create:controls")],
          rewards=["Собственная железная дорога"]),
        Q("schedule", "Расписание", "create:schedule", 0, 5,
          text=["Ехать туда, ждать загрузки, ждать минуту, ехать обратно. Условия — "
                "инвентарь, сигнал, время суток. Отдайте расписание кондуктору — "
                "и поезд перестанет нуждаться в вас."],
          tasks=[item("create:schedule")]),
        Q("signals", "Сигналы", "create:track_signal", 1, 5,
          deps=["track"],
          text=["Сигнал делит путь на участки и не пускает второй состав в занятый. "
                "На однопутке со встречным движением без них будет катастрофа — красивая, "
                "но катастрофа."],
          tasks=[item("create:track_signal", 2), item("create:track_observer")]),
        Q("board", "Табло", "create:display_board", 2, 5,
          deps=["signals"],
          text=["Поезд, направление, время прибытия. Пассажирам нравится."],
          tasks=[item("create:display_board", 4)], optional=True),
        Q("snr_coupler", "Steam 'n' Rails: сцепки", "railways:track_coupler", 0, 6,
          deps=["train"],
          text=["Винтовая, кулачковая, крюк со штырём. Составы расцепляют на ходу, "
                "буферы гасят удар, головные балки делают торцы вагонов похожими на вагоны."],
          tasks=[item("railways:track_coupler"), item("railways:buffer")]),
        Q("snr_conductor", "Кондуктор", "railways:conductor_cap", 1, 6,
          deps=["schedule"],
          text=["Фуражка на жителя — и он ведёт поезд по расписанию. Свисток зовёт "
                "состав на ближайшую станцию, как такси."],
          tasks=[item("railways:conductor_cap"), item("railways:conductor_whistle")]),
        Q("snr_style", "Оформление локомотива", "railways:smokestack_coalburner", 0, 7,
          deps=["snr_coupler"],
          text=["Трубы, котлы, дымовые коробки, обшивка всех цветов, полосы опасности, "
                "краска в кувшинах. Ничего из этого не нужно. Всё из этого хочется."],
          tasks=[item("railways:smokestack_coalburner")], optional=True),
        Q("snr_handcar", "Дрезина", "railways:handcar", 1, 7,
          deps=["track"],
          text=["Качаете рычаг — едете. Ни котла, ни расписания, ни достоинства."],
          tasks=[item("railways:handcar")], optional=True),
    ]),
)

chapter(
    "create_tools", "create", 100, "Снаряжение и схемы", "create:extendo_grip",
    "Инструменты Create и строительство по чертежам",
    [],
    chain([
        Q("extendo", "Удлинённый захват", "create:extendo_grip", 0, 0,
          text=["Руки становятся длиннее. Два захвата — ещё длиннее."],
          tasks=[item("create:extendo_grip")]),
        Q("potato", "Картофельная пушка", "create:potato_cannon", 1, 0,
          text=["Стреляет тем, что растёт. Картошка бьёт, свёкла красит, огненная лапша "
                "жжёт. С ранцем за спиной — очередями."],
          tasks=[item("create:potato_cannon")], optional=True),
        Q("symmetry", "Жезл симметрии", "create:wand_of_symmetry", 2, 0,
          text=["Ставите блок слева — появляется справа. Симметричные здания за половину "
                "времени."],
          tasks=[item("create:wand_of_symmetry")], optional=True),
        Q("schematic", "Схематика", "create:schematic_and_quill", 0, 1,
          text=["Перо обводит область и сохраняет её в файл. Стол загружает файл в пустую "
                "схематику. Здание становится предметом."],
          tasks=[item("create:schematic_and_quill"), item("create:schematic_table")]),
        Q("cannon", "Схематическая пушка", "create:schematicannon", 0, 2,
          text=["Пушка стреляет блоками из сундука по чертежу — и на пустыре вырастает "
                "здание, которое вы построили однажды где-то ещё. Порох в качестве топлива "
                "добавляет происходящему серьёзности."],
          tasks=[item("create:schematicannon")],
          rewards=["Автоматическое строительство любых сохранённых построек"]),
        Q("blueprint", "Чертёж крафта", "create:crafting_blueprint", 1, 2,
          text=["Рецепт на стене. Щёлкнули — собралось из вашего инвентаря."],
          tasks=[item("create:crafting_blueprint")], optional=True),
        Q("toolbox", "Ящик с инструментами", "create:brown_toolbox", 2, 2,
          text=["Восемь наборов предметов, раздаваемых в хотбар по клавише всем, кто рядом."],
          tasks=[item("create:brown_toolbox")], optional=True),
        Q("worldshaper", "Формирователь мира", "create:handheld_worldshaper", 0, 3,
          deps=["cannon"],
          text=["Творческий инструмент рельефа. В выживании его нет; знать о нём стоит."],
          tasks=[check("Прочитано")], optional=True),
    ]),
)

chapter(
    "create_world", "create", 110, "Create в мире", "create:andesite_casing",
    "Структуры, декор и мелкие дополнения",
    [],
    [
        Q("arise", "Create: Structures Arise", "create:andesite_casing", 0, 0,
          text=["Заброшенные фабрики, мастерские, шахты с работающими механизмами. Кто-то "
                "строил здесь до вас — и ушёл, оставив чертежи в сундуках."],
          tasks=[check("Найти постройку Create в мире")]),
        Q("rustic", "Create: Rustic Structures", "minecraft:oak_planks", 1, 0,
          text=["Мельницы, лесопилки, фермерские дворы. Деревенский Create, вписанный "
                "в холмы Terralith."],
          tasks=[check("Найти деревенскую постройку Create")]),
        Q("stickywheels", "Sticky Wheels", "offroad:sticky_tire", 0, 1,
          text=["Липкие шины для Offroad: держат склон, не скользят по льду."],
          tasks=[item("offroad:sticky_tire")], optional=True),
        Q("deco", "Декоративные блоки", "create:copper_shingles", 1, 1,
          text=["Медная черепица во всех стадиях зелени, стекло в рамах, балки, кронштейны, "
                "copycat-блоки, принимающие любой облик. Create умеет быть красивым."],
          tasks=[item("create:copper_shingles"), item("create:metal_girder")], optional=True),
    ],
)
