# -*- coding: utf-8 -*-
from dsl import chapter, Q, item, adv, check, chain

chapter(
    "create_fluids", "create", 40, "Жидкости", "create:mechanical_pump",
    "Трубы, насосы, краны и промышленный разлив",
    [
        "Труба в Create ничего не хранит. Она — только путь. Считать нужно баки и насосы, "
        "а не метры магистрали; и первое, что удивляет новичка, — что вода в трубе не "
        "течёт сама.",
    ],
    chain([
        Q("pipe", "Жидкостные трубы", "create:fluid_pipe", 0, 0,
          text=["Стеклянные показывают, что внутри. Умные фильтруют. Вентиль перекрывает "
                "по сигналу. Обычные — просто соединяют концы."],
          tasks=[item("create:fluid_pipe", 8)]),
        Q("pump", "Механический насос", "create:mechanical_pump", 0, 1,
          text=["Насос даёт жидкости направление и скорость. Без него сеть — рисунок. "
                "Направление меняют ключом или сигналом."],
          tasks=[item("create:mechanical_pump")]),
        Q("tank", "Жидкостный бак", "create:fluid_tank", -1, 2,
          text=["Баки срастаются в резервуар любого размера; окошко показывает уровень. "
                "Чем выше, тем больше."],
          tasks=[item("create:fluid_tank", 4)]),
        Q("hose", "Шланговый шкив", "create:hose_pulley", 1, 2,
          deps=["pump"],
          text=["Шланг опускается в озеро и выпивает его до дна. Или наоборот — заливает. "
                "Достаточно большой водоём считается бесконечным, и тогда это вечный источник."],
          tasks=[item("create:hose_pulley")],
          rewards=["Бесконечная вода и промышленная добыча лавы"]),
        Q("spout", "Разливщик и слив", "create:spout", 0, 3,
          text=["Разливщик льёт на предмет — так делают пироги ифрита и заливают бутылки. "
                "Слив вытягивает обратно из вёдер."],
          tasks=[item("create:spout"), item("create:item_drain")]),
        Q("chocolate", "Шоколад и мёд", "create:chocolate_bucket", 1, 3,
          deps=["spout"],
          text=["Какао в горячей чаше — шоколад. Соты — мёд. Не только еда: мёд идёт "
                "в рецепты, а шоколадные ягоды сытнее, чем кажутся."],
          tasks=[item("create:chocolate_bucket"), item("create:honey_bucket")],
          optional=True),
        Q("portable_fluid", "Переносной интерфейс", "create:portable_fluid_interface", 0, 4,
          deps=["tank", "hose"],
          text=["Контрапция подъезжает, интерфейсы стыкуются — и жидкость с предметами "
                "перетекают в стационарную сеть. Так разгружают поезда и буровые."],
          tasks=[item("create:portable_fluid_interface"),
                 item("create:portable_storage_interface")]),
    ]),
)

chapter(
    "create_copper", "create", 50, "Медная эпоха", "create:copper_casing",
    "Пар, давление и погружение",
    [
        "Медь — это пар. Медный корпус открывает котлы, двигатели и снаряжение, которое "
        "позволяет спуститься туда, куда раньше было нельзя.",
    ],
    chain([
        Q("copper_casing", "Медный корпус", "create:copper_casing", 0, 0,
          text=["Медные листы и доски. Нужен трубам в кожухе, шкиву и всей паровой технике."],
          tasks=[item("create:copper_casing", 4)]),
        Q("boiler", "Паровой котёл", "create:steam_engine", 0, 1,
          text=[
              "Бак с водой, горелки снизу, двигатели сбоку. У котла есть уровень — от одного "
              "до восемнадцати, — и растёт он от объёма, числа горелок и качества огня. "
              "Каждый двигатель снимает свою долю и крутит вал. Ничто в моде не даёт "
              "столько силы с такой маленькой площадки.",
          ],
          tasks=[item("create:steam_engine", 2), item("create:fluid_tank", 8)],
          rewards=["Тысячи единиц нагрузки с небольшой площадки"]),
        Q("whistle", "Паровой свисток", "create:steam_whistle", 1, 1,
          text=["Тон настраивается удлинителями. Из свистков собирают мелодии — и гудок "
                "поезда, который слышно за холмом."],
          tasks=[item("create:steam_whistle")], optional=True),
        Q("backtank", "Медный ранец", "create:copper_backtank", 0, 2,
          text=["Ранец копит сжатый воздух, пока его крутит вал, и отдаёт его шлему под водой. "
                "Незеритовый вмещает больше и не боится лавы."],
          tasks=[item("create:copper_backtank")]),
        Q("diving", "Водолазное снаряжение", "create:copper_diving_helmet", 0, 3,
          text=["Шлем дышит из ранца, ботинки держат на дне. Океан перестаёт быть стеной."],
          tasks=[item("create:copper_diving_helmet"), item("create:copper_diving_boots")]),
        Q("netherite_diving", "Незеритовый комплект", "create:netherite_diving_helmet", 1, 3,
          text=["В нём ходят по дну лавовых озёр Нижнего мира. Медленно, но ходят."],
          tasks=[item("create:netherite_diving_helmet"), item("create:netherite_backtank")],
          optional=True),
    ]),
)

chapter(
    "create_brass", "create", 60, "Латунная эпоха", "create:brass_casing",
    "Латунь, дробильные колёса и умная автоматика",
    [],
    chain([
        Q("brass", "Латунь", "create:brass_ingot", 0, 0,
          text=["Медь и цинк в горячей чаше. Обычного нагрева хватает. Из этого жёлтого "
                "металла сделано всё, что умеет думать."],
          tasks=[item("create:brass_ingot", 16)]),
        Q("brass_casing", "Латунный корпус", "create:brass_casing", 0, 1,
          text=["Основа воронок с фильтрами, туннелей с логикой и машин, которые решают сами."],
          tasks=[item("create:brass_casing", 8)]),
        Q("crushing", "Дробильные колёса", "create:crushing_wheel", -1, 2,
          deps=["brass"],
          text=[
              "Два колеса навстречу друг другу. Всё, что падает между ними, перемалывается — "
              "руда, камень, неосторожный игрок. В отличие от жёрнова колёса едят поток, "
              "и это основное удвоение руды на весь средний этап.",
          ],
          tasks=[item("create:crushing_wheel", 2)],
          rewards=["Промышленное удвоение руды"]),
        Q("brass_funnel", "Латунные воронки и туннели", "create:brass_funnel", 1, 2,
          deps=["brass_casing"],
          text=["Воронка выбирает по предмету, туннель делит поток поровну, по очереди или "
                "по фильтру. Фильтр атрибутов понимает слова «еда», «инструмент», "
                "«зачаровано» — и сортирует по смыслу."],
          tasks=[item("create:brass_funnel", 4), item("create:brass_tunnel", 2), item("create:filter")]),
        Q("deployer", "Деплойер", "create:deployer", 0, 3,
          deps=["brass_casing"],
          text=["Механическая рука с одним жестом: щёлкнуть, ударить, посадить, подоить. "
                "На контрапции — сердце любой фермы; на линии — сборщик, которому не "
                "надоедает."],
          tasks=[item("create:deployer", 2)]),
        Q("arm", "Механическая рука", "create:mechanical_arm", 1, 3,
          deps=["brass_casing"],
          text=["Ключом указывают, откуда брать и куда класть, — и рука переносит, "
                "фильтруя по каждой точке. Один манипулятор вместо десятка воронок."],
          tasks=[item("create:mechanical_arm")]),
        Q("precision", "Прецизионный механизм", "create:precision_mechanism", 0, 4,
          deps=["deployer", "arm"],
          text=[
              "Золотой лист, стержни, шестерни — и пять крафтеров с деплойерами по кругу. "
              "Механизм собирается только на линии, и это первая вещь в Create, которую "
              "нельзя сделать без Create. Дальше он нужен всему: расписаниям, радарам, "
              "поздней автоматике.",
          ],
          tasks=[item("create:precision_mechanism", 4)],
          rewards=["Пропуск в позднюю автоматику Create"]),
        Q("vault", "Хранилище предметов", "create:item_vault", -1, 4,
          deps=["brass_casing"],
          text=["Куб из блоков — один инвентарь на всех: для воронок, рук, упаковщиков "
                "и, позже, для сети Refined Storage."],
          tasks=[item("create:item_vault", 4)]),
        Q("chromatic", "Хроматика", "create:refined_radiance", 0, 5,
          deps=["precision"],
          text=["Хроматическое соединение под светом — Очищенное сияние; в темноте под "
                "давлением — Теневая сталь. Материалы для корпусов высшего уровня и "
                "для тех, кто любит красивое."],
          tasks=[item("create:chromatic_compound")], optional=True),
    ]),
)

chapter(
    "create_contraptions", "create", 70, "Контрапции", "create:mechanical_bearing",
    "Движущиеся конструкции: подшипники, поршни, шкивы",
    [
        "Контрапция — кусок мира, который Create отрывает и двигает как одно целое. "
        "Мост, который поворачивается. Бур, который едет. Дом, который вращается вокруг "
        "оси, если вам так захотелось. Правила везде одни: собрать, подать вращение, "
        "отпустить.",
    ],
    chain([
        Q("glue", "Суперклей и шасси", "create:super_glue", 0, 0,
          text=["Клей склеивает блоки в группу. Линейное шасси тянет вдоль оси, радиальное — "
                "по кругу; дальность настраивается ключом."],
          tasks=[item("create:super_glue"), item("create:linear_chassis", 4)]),
        Q("piston", "Механический поршень", "create:mechanical_piston", 0, 1,
          text=["Двигает по прямой на длину штанг. Липкий возвращает обратно. Ворота, "
                "мосты, выдвижные стены."],
          tasks=[item("create:mechanical_piston"), item("create:piston_extension_pole", 4)]),
        Q("pulley", "Верёвочный шкив", "create:rope_pulley", -1, 2,
          deps=["glue"],
          text=["Опускает и поднимает. Шахтный лифт, буровая, которую спускают в пропасть."],
          tasks=[item("create:rope_pulley")]),
        Q("elevator", "Лифт", "create:elevator_pulley", -2, 3,
          deps=["pulley"],
          text=["Настоящий лифт: контакт на каждом этаже, табличка с названием, кнопка. "
                "Ждёте кабину — и она приезжает."],
          tasks=[item("create:elevator_pulley"), item("create:elevator_contact", 2)]),
        Q("bearing", "Механический подшипник", "create:mechanical_bearing", 1, 2,
          deps=["glue"],
          text=["Вращает конструкцию вокруг себя. Карусель, разводной мост, ветряк, "
                "сборочная линия по кругу."],
          tasks=[item("create:mechanical_bearing")]),
        Q("clockwork", "Часовой подшипник", "create:clockwork_bearing", 2, 2,
          deps=["bearing"],
          text=["Оборот за сутки. Часы на башне, тень, ползущая по площади, — "
                "чистая декорация, и от этого не менее прекрасная."],
          tasks=[item("create:clockwork_bearing")], optional=True),
        Q("tools_contraption", "Инструменты на контрапции", "create:mechanical_drill", 0, 3,
          deps=["piston", "bearing"],
          text=["Бур ломает, пила валит, плуг пашет и собирает, жатка жнёт, каток кладёт "
                "дорогу. Всё это работает только в движении — и в движении работает "
                "без устали."],
          tasks=[item("create:mechanical_drill"), item("create:mechanical_harvester"),
                 item("create:mechanical_plough"), item("create:mechanical_roller")]),
        Q("cart", "Тележки-контрапции", "create:cart_assembler", 1, 3,
          deps=["glue"],
          text=["Сборщик превращает постройку над рельсом в едущую вагонетку. Сцепка "
                "делает из двух тележек поезд задолго до настоящих поездов."],
          tasks=[item("create:cart_assembler"), item("create:minecart_coupling")]),
        Q("gantry", "Портальная система", "create:gantry_carriage", 2, 3,
          deps=["piston"],
          text=["Каретка едет по валу-рельсу и тянет за собой что угодно. Карьеры "
                "размером с чанк начинаются здесь."],
          tasks=[item("create:gantry_carriage")]),
        Q("controls", "Управление контрапцией", "create:contraption_controls", 0, 4,
          deps=["tools_contraption", "cart"],
          text=["Пульт включает части машины изнутри. Сиденье сажает вас, штурвал даёт "
                "власть над поездом. Машина, в которой едешь, — другой уровень отношений."],
          tasks=[item("create:contraption_controls"), item("create:green_seat")]),
    ]),
)
