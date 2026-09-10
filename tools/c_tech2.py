# -*- coding: utf-8 -*-
"""PneumaticCraft, Industrial Foregoing, Powah и Immersive Petroleum."""
from dsl import chapter, Q, item, give, adv, check, loot, chain

P = "pneumaticcraft:"
F = "industrialforegoing:"
W = "powah:"
O = "immersivepetroleum:"

chapter(
    "tech2_pneumatic", "tech2", 10, "PneumaticCraft", P + "air_compressor",
    "Давление, пластик и дроны, которых вы программируете",
    [
        "PneumaticCraft — единственный мод сборки, где машина может взорваться "
        "просто потому, что вы перекачали в неё воздуха. Давление здесь настоящий "
        "ресурс: его мало, оно копится медленно и уходит мгновенно.",
        "Зато в конце пути стоят дроны — маленькие роботы, которым вы рисуете "
        "программу из блоков и отправляете копать, строить, собирать урожай "
        "или воевать.",
        "Начинается всё со сжатого железа: железный слиток кладут в огонь и "
        "взрывают.",
    ],
    chain([
        Q("compressed", "Сжатое железо", P + "ingot_iron_compressed", 0, 0,
          text=[
              "Положите железные слитки на землю и взорвите. Часть уцелеет и "
              "станет сжатым железом — базовым материалом мода.",
              "Способ грубый, зато работает с первого дня и не требует ничего, "
              "кроме тротила.",
          ],
          tasks=[item(P + "ingot_iron_compressed", 16)],
          rewards=loot(("minecraft:tnt", 8), xp=100)),

        Q("compressor", "Компрессор", P + "air_compressor", 0, 1,
          text=[
              "Сжигает топливо и гонит воздух в трубы. Манометр показывает "
              "давление, и на него стоит смотреть: у каждой машины свой предел.",
              "Превысите — машина взорвётся. Предохранительный клапан спасает, "
              "но его надо не забыть поставить.",
          ],
          tasks=[item(P + "air_compressor"), item(P + "pressure_tube", 4),
                 item(P + "manometer")],
          rewards=loot((P + "pressure_tube", 8), xp=150)),

        Q("chamber", "Камера давления", P + "pressure_chamber_valve", 0, 2,
          text=[
              "Куб из стеклянных стен с клапаном и интерфейсом. Внутри под "
              "давлением происходят рецепты, которых нет больше нигде: "
              "пустые платы, детали, заготовки.",
              "Это первая многоблочная конструкция мода и самая нужная.",
          ],
          tasks=[item(P + "pressure_chamber_wall", 8), item(P + "pressure_chamber_valve"),
                 item(P + "pressure_chamber_interface")],
          rewards=loot((P + "pressure_chamber_wall", 8), xp=250)),

        Q("plastic", "Пластик", P + "plastic", 0, 3,
          text=[
              "Нефть перегоняется в дизель, керосин и жидкий пластик, а тот "
              "застывает в листы. Нефть берут из скважин Immersive Petroleum "
              "или из своей переработки.",
              "Пластик идёт во всё: платы, дроны, броню.",
          ],
          tasks=[item(P + "plastic", 16), item(P + "refinery")],
          rewards=loot((P + "plastic", 16), xp=250)),

        Q("pcb", "Печатные платы", P + "printed_circuit_board", 0, 4,
          text=[
              "Пустая плата, ультрафиолетовая засветка, травление в кислоте — "
              "и получается готовая плата. Процесс капризный и с браком.",
              "Платы — сердце всей электроники мода.",
          ],
          tasks=[item(P + "empty_pcb"), item(P + "etching_tank"),
                 item(P + "printed_circuit_board", 4)],
          rewards=loot((P + "printed_circuit_board", 4), xp=300)),

        Q("assembly", "Сборочная линия", P + "assembly_controller", 0, 5,
          text=[
              "Контроллер, платформа, дрель и лазер — конвейер, который сам "
              "изготавливает детали по программе.",
              "Первая настоящая автоматизация PneumaticCraft и обязательный "
              "шаг к дронам.",
          ],
          tasks=[item(P + "assembly_controller"), item(P + "assembly_platform"),
                 item(P + "assembly_drill"), item(P + "assembly_laser")],
          rewards=loot((P + "plastic", 32), xp=400)),

        Q("drone", "Дрон", P + "drone", 0, 6,
          text=[
              "Программатор рисует дрону задачу из блоков-инструкций: иди сюда, "
              "выкопай это, положи туда, повтори.",
              "GPS-инструмент задаёт координаты. Логистические дроны разносят "
              "предметы по базе сами, без единой трубы.",
          ],
          tasks=[item(P + "programmer"), item(P + "gps_tool"), item(P + "drone")],
          rewards=loot((P + "drone", 2), xp=500)),

        Q("armor", "Пневматическая броня", P + "pneumatic_helmet", 0, 7,
          text=[
              "Шлем показывает мобов сквозь стены и ведёт дронов, нагрудник "
              "бьёт током, поножи ускоряют, ботинки дают реактивные прыжки.",
              "Апгрейды ставятся модулями и питаются от того же сжатого воздуха.",
          ],
          tasks=[item(P + "pneumatic_helmet"), item(P + "pneumatic_chestplate"),
                 item(P + "charging_station")],
          rewards=loot((P + "air_canister", 4), xp=600)),

        Q("elevator", "Лифт", P + "elevator_base", 1, 6,
          deps=["assembly"],
          text=["Пневматический лифт поднимает на любую высоту и вызывается "
                "кнопкой на каждом этаже. Тихий, быстрый и без единого поршня."],
          tasks=[item(P + "elevator_base"), item(P + "elevator_frame", 4)],
          rewards=loot((P + "plastic", 16), xp=300), optional=True),
    ]),
)

chapter(
    "tech2_foregoing", "tech2", 20, "Industrial Foregoing", F + "machine_frame_pity",
    "Каучук, чёрные дыры и фермы, которые работают сами",
    [
        "Industrial Foregoing — это набор машин без единой цепочки: каждая "
        "делает одно дело и делает его хорошо. Сажает, собирает, доит, стрижёт, "
        "убивает, плавит, хранит.",
        "Всё начинается с каучука из деревьев и заканчивается блоками чёрной "
        "дыры, которые вмещают два миллиарда предметов одного типа.",
    ],
    chain([
        Q("latex", "Каучук", F + "latex_processing_unit", 0, 0,
          text=[
              "Экстрактор древесного сока цедит латекс из брёвен, обрабатывающий "
              "блок варит из него сухой каучук, а из каучука делают пластик.",
              "Пластик — материал всех рамок и половины машин мода.",
          ],
          tasks=[item(F + "latex_processing_unit"), item(F + "dryrubber", 8),
                 item(F + "plastic", 16)],
          rewards=loot((F + "plastic", 16), xp=150)),

        Q("frames", "Рамки машин", F + "machine_frame_pity", 0, 1,
          text=[
              "Четыре уровня: жалкая, простая, продвинутая, высшая. Каждая "
              "машина требует рамку своего уровня, и это единственная "
              "прогрессия в моде.",
          ],
          tasks=[item(F + "machine_frame_pity", 2), item(F + "machine_frame_simple")],
          rewards=loot((F + "machine_frame_pity", 4), xp=200)),

        Q("farm", "Автоферма", F + "plant_gatherer", 0, 2,
          text=[
              "Сеятель сажает по площади, сборщик собирает всё, до чего "
              "дотянется, включая деревья целиком.",
              "Удобрение из мода ускоряет рост. Ферма получается компактной "
              "и полностью автономной.",
          ],
          tasks=[item(F + "plant_sower"), item(F + "plant_gatherer"),
                 item(F + "fertilizer", 8)],
          rewards=loot((F + "fertilizer", 16), xp=250)),

        Q("animals", "Животноводство", F + "animal_rancher", 0, 3,
          text=[
              "Ранчер доит коров и стрижёт овец, не трогая самих животных. "
              "Кормушка разводит их автоматически.",
              "Бойня и дробилка мобов превращают ферму в источник мяса, "
              "опыта и розовой слизи.",
          ],
          tasks=[item(F + "animal_rancher"), item(F + "animal_feeder"),
                 item(F + "mob_crusher")],
          rewards=loot((F + "pink_slime_ingot", 4), xp=300)),

        Q("blackhole", "Чёрные дыры", F + "black_hole_unit", 0, 4,
          text=[
              "Блок чёрной дыры хранит два миллиарда предметов одного типа. "
              "Бак — столько же жидкости.",
              "Контроллер объединяет их в единый инвентарь. Проблема "
              "переполненного склада закрывается навсегда.",
          ],
          tasks=[item(F + "black_hole_unit"), item(F + "black_hole_tank"),
                 item(F + "black_hole_controller")],
          rewards=loot((F + "black_hole_unit", 2), xp=400)),

        Q("laser", "Лазерное бурение", F + "laser_drill", 0, 5,
          text=[
              "Лазерная база бьёт лучом в бедрок и вытягивает оттуда руду. "
              "Линзы задают, какую именно: чем реже руда, тем больше линз "
              "нужного цвета.",
              "Это бесконечный источник любых ресурсов и главная причина "
              "ставить мод.",
          ],
          tasks=[item(F + "laser_drill"), item(F + "fluid_laser_base"),
                 item(F + "laser_lens", 4)],
          rewards=loot((F + "machine_frame_advanced", 2), xp=600)),

        Q("stonework", "Каменный завод", F + "material_stonework_factory", 1, 5,
          deps=["blackhole"],
          text=["Одна машина, которая делает из воды и лавы булыжник, камень, "
                "кирпич, стекло и всё, что из них режется. Ставится один раз "
                "и кормит стройку до конца игры."],
          tasks=[item(F + "material_stonework_factory")],
          rewards=loot(("minecraft:stone", 64), xp=350), optional=True),
    ]),
)

chapter(
    "tech2_powah", "tech2", 30, "Powah", W + "energy_cell_starter",
    "Энергия без сложностей: генераторы, ячейки, реактор",
    [
        "Powah не изобретает механик — он даёт энергию просто и надёжно. "
        "Пять видов генераторов, ячейки на любой объём, кабели и беспроводная "
        "передача.",
        "Пять уровней у всего: стартовый, базовый, продвинутый, элитный, "
        "высший и созидательный. Разница только в цифрах, но цифры растут "
        "быстро.",
    ],
    chain([
        Q("dielectric", "Диэлектрик", W + "dielectric_paste", 0, 0,
          text=[
              "Паста, стержни и корпус — из них собрано всё в этом моде. "
              "Плюс энергетическая сталь, которая делается в энергетическом "
              "шаре.",
          ],
          tasks=[item(W + "dielectric_paste", 8), item(W + "dielectric_casing", 4)],
          rewards=loot((W + "dielectric_paste", 16), xp=120)),

        Q("generators", "Генераторы", W + "thermo_generator_starter", 0, 1,
          text=[
              "Термогенератор на разнице температур, фурнатор на угле, "
              "магматор на лаве, солнечная панель на солнце.",
              "Все стартовые версии дешёвы и ставятся в первый же вечер.",
          ],
          tasks=[item(W + "thermo_generator_starter"), item(W + "furnator_starter"),
                 item(W + "magmator_starter")],
          rewards=loot((W + "energy_cable_starter", 8), xp=200)),

        Q("cells", "Ячейки и кабели", W + "energy_cell_starter", 0, 2,
          text=[
              "Ячейка хранит, кабель передаёт. Эндер-ячейка связывает две "
              "точки без провода, передатчик игрока заряжает всё, что у вас "
              "в карманах, на расстоянии.",
          ],
          tasks=[item(W + "energy_cell_starter"), item(W + "energy_cable_starter", 8),
                 item(W + "ender_cell_starter")],
          rewards=loot((W + "energy_cell_basic", 1), xp=250)),

        Q("energizing", "Энергетический шар", W + "energizing_orb", 0, 3,
          text=[
              "Шар и стержни вокруг него превращают энергию в материалы: "
              "энергетическую сталь, кристаллы, компоненты высших уровней.",
              "Чем больше стержней, тем быстрее. Это узловая машина мода.",
          ],
          tasks=[item(W + "energizing_orb"), item(W + "energizing_rod_starter", 4),
                 item(W + "steel_energized", 8)],
          rewards=loot((W + "steel_energized", 8), xp=300)),

        Q("crystals", "Кристаллы", W + "blazing_crystal", 0, 4,
          text=[
              "Пылающий, ниотический, одухотворённый, нитро — четыре кристалла, "
              "которые задают уровень всей техники.",
              "Делаются в шаре из соответствующих материалов и стоят дорого.",
          ],
          tasks=[item(W + "blazing_crystal", 4), item(W + "niotic_crystal", 2)],
          rewards=loot((W + "blazing_crystal", 8), xp=400)),

        Q("reactor", "Реактор", W + "reactor_starter", 0, 5,
          text=[
              "Уранинит добывается в шахтах и питает реактор. Многоблочный, "
              "тихий и очень мощный — но требует охлаждения.",
              "Топливо расходуется медленно, а отдача не зависит ни от "
              "солнца, ни от угля.",
          ],
          tasks=[item(W + "uraninite_raw", 8), item(W + "uraninite", 4),
                 item(W + "reactor_starter")],
          rewards=loot((W + "uraninite", 8), xp=600)),
    ]),
)

chapter(
    "tech2_petroleum", "tech2", 40, "Immersive Petroleum", O + "pumpjack",
    "Нефть, скважины и то, что из них гонят",
    [
        "Аддон к Immersive Engineering, который добавляет к нему нефтяную "
        "промышленность: разведку, бурение, добычу и переработку.",
        "Нефть залегает резервуарами под целыми регионами. Найти — половина "
        "дела; вторая половина — построить над ней качалку.",
    ],
    chain([
        Q("survey", "Разведка", O + "seismic_survey", 0, 0,
          text=[
              "Сейсморазведка показывает, есть ли под этим участком "
              "резервуар и какой. Керн из Immersive Engineering делает то же "
              "для руды.",
              "Бурить наугад бессмысленно: под большинством чанков пусто.",
          ],
          tasks=[item(O + "seismic_survey"), item("immersiveengineering:coresample")],
          rewards=loot((O + "seismic_survey", 2), xp=200)),

        Q("derrick", "Вышка", O + "derrick", 0, 1,
          text=[
              "Буровая вышка вскрывает резервуар. Ставится один раз на "
              "месторождение и работает до его исчерпания.",
          ],
          tasks=[item(O + "derrick")],
          rewards=loot(("immersiveengineering:ingot_steel", 16), xp=300)),

        Q("pumpjack", "Качалка", O + "pumpjack", 0, 2,
          text=[
              "Знаменитый кивающий насос. Тянет нефть из вскрытого резервуара "
              "и кормит ею весь завод.",
              "Резервуары не бесконечны, но остаточный приток остаётся навсегда.",
          ],
          tasks=[item(O + "pumpjack")],
          rewards=loot((O + "gasoline_bucket", 4), xp=400)),

        Q("tower", "Дистилляционная башня", O + "distillation_tower", 0, 3,
          text=[
              "Нефть разгоняется на фракции: бензин, дизель, смазка, "
              "битум. Каждая идёт своим путём.",
              "Факельная труба сжигает лишний газ, чтобы башня не встала.",
          ],
          tasks=[item(O + "distillation_tower"), item(O + "flarestack"),
                 item(O + "diesel_bucket", 4)],
          rewards=loot((O + "lubricant_bucket", 4), xp=500)),

        Q("products", "Продукты", O + "asphalt", 0, 4,
          text=[
              "Асфальт кладут дорогой — по нему бегается быстрее. Смазка "
              "ускоряет машины Immersive Engineering через автосмазчик.",
              "Напалм — на случай, если дипломатия не сработала.",
          ],
          tasks=[item(O + "asphalt", 16), item(O + "auto_lubricator")],
          rewards=loot((O + "asphalt", 32), xp=400)),
    ]),
)
