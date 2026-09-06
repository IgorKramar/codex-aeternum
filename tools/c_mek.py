# -*- coding: utf-8 -*-
from dsl import chapter, Q, item, adv, check, chain

chapter(
    "mek_start", "mek", 10, "Осмий и первые машины", "mekanism:ingot_osmium",
    "Металлургический инфузер, сталь и стальной корпус",
    [],
    chain([
        Q("osmium", "Осмий", "mekanism:ingot_osmium", 0, 0,
          text=["Синеватый металл, который лежит везде и нужен всему. Корпуса, кабели, "
                "первые детали. Рядом с ним — олово, свинец, флюорит и уран; уран пока "
                "не трогайте."],
          tasks=[item("mekanism:ingot_osmium", 16), item("mekanism:ingot_tin", 8)]),
        Q("infuser", "Металлургический инфузер", "mekanism:metallurgic_infuser", 0, 1,
          text=["Первая машина, и уже алхимия: предмет пропитывается веществом — углеродом, "
                "красным камнем, алмазом, оловом — и становится другим предметом. Сталь, "
                "сплавы, усиленные материалы — всё отсюда."],
          tasks=[item("mekanism:metallurgic_infuser")]),
        Q("steel", "Сталь", "mekanism:ingot_steel", 0, 2,
          text=["Железо плюс обогащённый углерод — заготовка, заготовка в печь — слиток. "
                "Своя сталь, отличная от стали IE, и в этой сборке им придётся уживаться."],
          tasks=[item("mekanism:ingot_steel", 16)]),
        Q("casing", "Стальной корпус", "mekanism:steel_casing", 0, 3,
          text=["Сталь, осмий, стекло. Общая деталь каждой машины мода — от обогатителя "
                "до термоядерного реактора."],
          tasks=[item("mekanism:steel_casing", 8)],
          rewards=["Пропуск ко всем машинам мода"]),
        Q("circuit", "Управляющие схемы", "mekanism:basic_control_circuit", 0, 4,
          text=["Базовая из осмия, продвинутая из обогащённого сплава, элитная из усиленного, "
                "предельная из атомного. Уровень схемы — потолок того, что вы можете построить."],
          tasks=[item("mekanism:basic_control_circuit", 4)]),
        Q("alloys", "Сплавы", "mekanism:alloy_infused", 1, 4,
          text=["Обогащённый, усиленный, атомный. Каждый — ступень выше и химия сложнее."],
          tasks=[item("mekanism:alloy_infused", 4)]),
        Q("cables", "Передача", "mekanism:basic_universal_cable", 0, 5,
          text=["Кабель для энергии, труба для жидкости, труба под давлением для газа, "
                "транспортёр для предметов, проводник для тепла. Пять видов, пять уровней, "
                "одна логика."],
          tasks=[item("mekanism:basic_universal_cable", 8), item("mekanism:basic_mechanical_pipe", 4),
                 item("mekanism:basic_pressurized_tube", 4), item("mekanism:basic_logistical_transporter", 8)]),
        Q("sorter", "Логистическая сортировка", "mekanism:logistical_sorter", 1, 5,
          text=["По предмету, по тегу, по цвету. Диверсионный и ограничивающий транспортёры "
                "направляют поток."],
          tasks=[item("mekanism:logistical_sorter"), item("mekanism:diversion_transporter")]),
        Q("energy", "Хранение энергии", "mekanism:basic_energy_cube", 0, 6,
          text=["Куб хранит и переводит между сетями. Индукционная матрица — батарея "
                "размером с дом."],
          tasks=[item("mekanism:basic_energy_cube")]),
        Q("configurator", "Конфигуратор", "mekanism:configurator", 1, 6,
          text=["Стороны, поворот, выкачка, разбор. Карта копирует настройки одной "
                "машины на другую."],
          tasks=[item("mekanism:configurator"), item("mekanism:configuration_card")]),
        Q("box", "Картонная коробка", "mekanism:cardboard_box", 2, 6,
          text=["Машина в коробку — вместе с содержимым и настройками. Переезд за минуту."],
          tasks=[item("mekanism:cardboard_box")]),
    ]),
)

chapter(
    "mek_ore", "mek", 20, "Переработка руды", "mekanism:enrichment_chamber",
    "От удвоения к пятикратному выходу",
    [
        "Ради этой главы ставят Mekanism. Каждая машина в цепочке добавляет множитель: "
        "два, три, четыре, пять. Пять слитков из одного куска руды — это не удобство, "
        "это другая экономика.",
    ],
    chain([
        Q("enrichment", "Обогатительная камера (×2)", "mekanism:enrichment_chamber", 0, 0,
          text=["Руда в два измельчённых кусочка, кусочки в два слитка. Заодно — "
                "обогащённые вещества для инфузера."],
          tasks=[item("mekanism:enrichment_chamber")],
          rewards=["Двукратная переработка руды"]),
        Q("crusher_mek", "Дробилка и комбайнер", "mekanism:crusher", 1, 0,
          text=["Дробилка — слитки обратно в пыль, комбайнер — пыль и камень в руду. "
                "Цикл замкнут."],
          tasks=[item("mekanism:crusher"), item("mekanism:combiner")]),
        Q("purification", "Камера очистки (×3)", "mekanism:purification_chamber", 0, 1,
          text=["Руда и кислород — три кусочка. Кислород даёт сепаратор, разлагающий воду; "
                "водород сохраните — он пригодится джетпаку."],
          tasks=[item("mekanism:purification_chamber"), item("mekanism:electrolytic_separator")],
          rewards=["Трёхкратная переработка руды"]),
        Q("injection", "Химическая инъекция (×4)", "mekanism:chemical_injection_chamber", 0, 2,
          text=["Руда и хлороводород — четыре осколка. Хлор из рассола, водород из воды, "
                "вместе в химическом инфузере. Это уже завод."],
          tasks=[item("mekanism:chemical_injection_chamber"), item("mekanism:chemical_infuser")],
          rewards=["Четырёхкратная переработка руды"]),
        Q("evaporation", "Термальная испарительная установка", "mekanism:thermal_evaporation_controller", 1, 2,
          text=["Башня под солнцем выпаривает воду в рассол, рассол в соль. Источник хлора, "
                "серной кислоты и тяжёлой воды. Чем выше и жарче, тем быстрее."],
          tasks=[item("mekanism:thermal_evaporation_controller"), item("mekanism:thermal_evaporation_block", 16)]),
        Q("dissolution", "Растворение и кристаллизация (×5)", "mekanism:chemical_dissolution_chamber", 0, 3,
          text=["Растворить в кислоте, промыть, кристаллизовать, раздробить, обогатить. "
                "Четыре новые машины и много энергии. Пять слитков из одной руды — "
                "потолок мода, и он окупается за вечер."],
          tasks=[item("mekanism:chemical_dissolution_chamber"), item("mekanism:chemical_washer"),
                 item("mekanism:chemical_crystallizer"), item("mekanism:chemical_oxidizer")],
          rewards=["Пятикратная переработка руды — потолок мода"]),
        Q("factory", "Фабрики", "mekanism:basic_smelting_factory", 0, 4,
          text=["Одна машина, несколько потоков: три, пять, семь, девять. Установщик уровня "
                "поднимает уже стоящую фабрику, не разбирая."],
          tasks=[item("mekanism:basic_smelting_factory"), item("mekanism:basic_tier_installer")]),
        Q("miner", "Цифровой шахтёр", "mekanism:digital_miner", 0, 5,
          text=["Радиус, высоты, фильтр — и он копает только то, что вы назвали, не трогая "
                "остального. С генератором камня оставляет за собой ровную породу; "
                "с шёлковым касанием — приносит блоки целиком."],
          tasks=[item("mekanism:digital_miner"), item("mekanism:upgrade_stone_generator")],
          rewards=["Полностью автоматическая добыча"]),
        Q("upgrades", "Улучшения машин", "mekanism:upgrade_speed", 1, 5,
          text=["Скорость, энергоэффективность, фильтр газа, тишина, якорь чанка. Скорость "
                "жрёт энергию — уравновешивайте."],
          tasks=[item("mekanism:upgrade_speed"), item("mekanism:upgrade_energy"), item("mekanism:upgrade_anchor")]),
        Q("sawmill", "Пилорама и прочее", "mekanism:precision_sawmill", 2, 5,
          text=["Пилорама разбирает предметы на части, печь плавит дёшево, формовочный "
                "сборщик крафтит по формуле."],
          tasks=[item("mekanism:precision_sawmill"), item("mekanism:energized_smelter"),
                 item("mekanism:formulaic_assemblicator")]),
    ]),
)

chapter(
    "mek_power", "mek", 30, "Генерация энергии", "mekanismgenerators:gas_burning_generator",
    "От тепловой установки до паровой турбины",
    [],
    chain([
        Q("heat_gen", "Тепловая установка", "mekanismgenerators:heat_generator", 0, 0,
          text=["Уголь или лава. Слабо, зато с первой минуты."],
          tasks=[item("mekanismgenerators:heat_generator")]),
        Q("solar", "Солнечные панели", "mekanismgenerators:solar_generator", 1, 0,
          text=["Обычная — чуть-чуть, продвинутая три на три — заметно."],
          tasks=[item("mekanismgenerators:solar_generator"), item("mekanismgenerators:advanced_solar_generator")]),
        Q("wind", "Ветрогенератор", "mekanismgenerators:wind_generator", 2, 0,
          text=["Чем выше, тем сильнее. На вершине горы Terralith — лучший пассив старта."],
          tasks=[item("mekanismgenerators:wind_generator")]),
        Q("bio", "Биогенератор", "mekanismgenerators:bio_generator", 3, 0,
          text=["Растения через дробилку — биотопливо. Ферма кормит электростанцию."],
          tasks=[item("mekanismgenerators:bio_generator")]),
        Q("gas_gen", "Газовый генератор", "mekanismgenerators:gas_burning_generator", 0, 1,
          text=["Этилен — самый плотный по энергии газ мода. Биотопливо, вода и субстрат "
                "в камере реакции дают его; генератор сжигает. Эта связка кормит базу "
                "до самого реактора."],
          tasks=[item("mekanismgenerators:gas_burning_generator"), item("mekanism:pressurized_reaction_chamber")],
          rewards=["Основной источник энергии средней игры"]),
        Q("boiler", "Тепловой котёл", "mekanism:boiler_casing", 0, 2,
          text=["Вода в пар от нагревателей или от реактора. Пар — турбине."],
          tasks=[item("mekanism:boiler_casing", 16), item("mekanism:boiler_valve", 2)]),
        Q("turbine", "Паровая турбина", "mekanismgenerators:turbine_casing", 0, 3,
          text=["Ротор в башне, лопасти на роторе, конденсаторы наверху. Собранная правильно, "
                "она выдаёт миллионы в тик — и звучит как настоящая."],
          tasks=[item("mekanismgenerators:turbine_casing", 16), item("mekanismgenerators:turbine_rotor", 4),
                 item("mekanismgenerators:turbine_blade", 8), item("mekanismgenerators:saturating_condenser", 4)],
          rewards=["Энергия промышленного масштаба"]),
        Q("induction", "Индукционная матрица", "mekanism:induction_casing", 0, 4,
          text=["Ячейки задают объём, провайдеры — скорость. Верхние уровни хранят числа, "
                "которые не помещаются в голове."],
          tasks=[item("mekanism:induction_casing", 16), item("mekanism:basic_induction_cell"),
                 item("mekanism:basic_induction_provider")]),
    ]),
)

chapter(
    "mek_nuclear", "mek", 40, "Ядерная энергетика", "mekanismgenerators:fission_reactor_casing",
    "Уран, реактор деления, отходы и радиация",
    [],
    chain([
        Q("uranium", "Уран", "mekanism:ingot_uranium", 0, 0,
          text=["Глубоко и редко. Слиток — в жёлтый кек, кек — в топливо. Без защиты "
                "он греет руки в самом плохом смысле."],
          tasks=[item("mekanism:ingot_uranium", 8), item("mekanism:yellow_cake_uranium", 4)]),
        Q("hazmat", "Защитный костюм", "mekanism:hazmat_gown", 1, 0,
          text=["Костюм снижает дозу, счётчик Гейгера показывает фон, дозиметр — сколько "
                "вы уже набрали. К реактору без всех трёх не подходят."],
          tasks=[item("mekanism:hazmat_gown"), item("mekanism:geiger_counter"), item("mekanism:dosimeter")]),
        Q("fuel", "Топливные сборки", "mekanismgenerators:fission_fuel_assembly", 0, 1,
          text=["Кек, центрифуга, нейтронный активатор на солнце — гексафторид, потом "
                "делящееся топливо. Сборка вставляется в реактор и тихо сгорает."],
          tasks=[item("mekanismgenerators:fission_fuel_assembly"), item("mekanism:isotopic_centrifuge"),
                 item("mekanism:solar_neutron_activator")]),
        Q("reactor", "Реактор деления", "mekanismgenerators:fission_reactor_casing", 0, 2,
          text=[
              "Корпус, порты, сборки, стержни, теплоноситель. Скорость горения задаёте вы — "
              "и вы же отвечаете, если температура уйдёт за предел. Логический адаптер "
              "свяжите с аварийным остановом до того, как загрузите первую сборку. "
              "Это не совет. Это единственное правило.",
          ],
          tasks=[item("mekanismgenerators:fission_reactor_casing", 32), item("mekanismgenerators:fission_reactor_port", 4),
                 item("mekanismgenerators:control_rod_assembly"), item("mekanismgenerators:fission_reactor_logic_adapter")],
          rewards=["Гигаваттные мощности — и постоянный риск"]),
        Q("waste", "Отходы", "mekanism:radioactive_waste_barrel", 0, 3,
          text=["Бочка медленно распадает отходы; полная бочка — выброс. Отходы же "
                "перерабатываются в полоний и плутоний, и вот тогда начинается интересное."],
          tasks=[item("mekanism:radioactive_waste_barrel"), item("mekanism:pellet_polonium"), item("mekanism:pellet_plutonium")]),
        Q("fusion", "Термоядерный реактор", "mekanismgenerators:fusion_reactor_controller", 0, 4,
          text=["Дейтерий и тритий из тяжёлой воды, хольраум с топливом, лазер, который "
                "зажигает звезду. Дальше она горит сама, без отходов и без страха."],
          tasks=[item("mekanismgenerators:fusion_reactor_controller"), item("mekanismgenerators:fusion_reactor_frame", 32),
                 item("mekanismgenerators:hohlraum"), item("mekanismgenerators:laser_focus_matrix"),
                 item("mekanism:laser_amplifier")],
          rewards=["Чистая энергия высшего уровня"]),
        Q("sps", "Сверхкритический сдвиг фаз", "mekanism:sps_casing", 0, 5,
          text=["Полоний в антивещество ценой чудовищной энергии. Антивещество — "
                "нуклеосинтезатору, который делает то, чего не бывает."],
          tasks=[item("mekanism:sps_casing", 16), item("mekanism:sps_port"), item("mekanism:pellet_antimatter"),
                 item("mekanism:antiprotonic_nucleosynthesizer")],
          rewards=["Вершина технологического дерева Mekanism"]),
    ]),
)

chapter(
    "mek_qio", "mek", 50, "QIO и телепортация", "mekanism:qio_dashboard",
    "Квантовое хранилище и мгновенные перемещения",
    [],
    chain([
        Q("teleport_core", "Телепортационное ядро", "mekanism:teleportation_core", 0, 0,
          text=["Общая деталь всего, что нарушает расстояние."],
          tasks=[item("mekanism:teleportation_core", 4)]),
        Q("teleporter", "Телепорт", "mekanism:teleporter", 0, 1,
          text=["Два телепорта на одной частоте — и между ними нет пути, только шаг. "
                "Через измерения тоже. Портативный уносит к любому стационарному."],
          tasks=[item("mekanism:teleporter"), item("mekanism:portable_teleporter")]),
        Q("entangloporter", "Квантовый связыватель", "mekanism:quantum_entangloporter", 1, 1,
          text=["Энергия, жидкость, газ, предметы — между двумя точками без трубы. "
                "Реактор на краю мира, турбина дома."],
          tasks=[item("mekanism:quantum_entangloporter")]),
        Q("qio_array", "Массив дисков QIO", "mekanism:qio_drive_array", 0, 2,
          text=["Базовый, гиперплотный, замедляющий время, сверхмассивный. Названия "
                "честные."],
          tasks=[item("mekanism:qio_drive_array"), item("mekanism:qio_drive_base")]),
        Q("qio_dash", "Панель QIO", "mekanism:qio_dashboard", 0, 3,
          text=["Окно в хранилище без единого кабеля. Портативная — в кармане."],
          tasks=[item("mekanism:qio_dashboard"), item("mekanism:portable_qio_dashboard")],
          rewards=["Беспроводное хранилище любой ёмкости"]),
        Q("qio_io", "Импорт и экспорт", "mekanism:qio_importer", 0, 4,
          text=["Импортёр кладёт, экспортёр достаёт по фильтру, адаптер даёт сигнал."],
          tasks=[item("mekanism:qio_importer"), item("mekanism:qio_exporter"), item("mekanism:qio_redstone_adapter")]),
        Q("stabilizer", "Стабилизатор измерения", "mekanism:dimensional_stabilizer", 1, 4,
          text=["Держит чанки. Предельная схема — и ваша база не засыпает никогда."],
          tasks=[item("mekanism:dimensional_stabilizer")]),
    ]),
)

chapter(
    "mek_gear", "mek", 60, "MekaSuit", "mekanism:mekasuit_bodyarmor",
    "Силовая броня, модули и Meka-Tool",
    [
        "MekaSuit сама по себе — алмаз с батарейкой. Всё решают модули: больше тридцати, "
        "и каждый превращает костюм во что-то новое — в водолаза, в лётчика, в шахтёра, "
        "которому не нужна кирка.",
    ],
    chain([
        Q("scuba", "Дыхание и полёт", "mekanism:scuba_mask", 0, 0,
          text=["Маска с баллоном — вода. Джетпак на водороде — небо; в сборке его носят "
                "в слоте аксессуара, не снимая нагрудник. Скороходы гасят падение "
                "и взбегают по склону."],
          tasks=[item("mekanism:scuba_mask"), item("mekanism:jetpack"), item("mekanism:free_runners")]),
        Q("atomic_disassembler", "Атомный дизассемблер", "mekanism:atomic_disassembler", 1, 0,
          text=["Копает всё, режет всё, вынимает жилу целиком. Первый инструмент, после "
                "которого кирка кажется палкой."],
          tasks=[item("mekanism:atomic_disassembler")]),
        Q("robit", "Робит", "mekanism:robit", 2, 0,
          text=["Подбирает, плавит, крафтит, ходит следом. Зарядная станция — дом."],
          tasks=[item("mekanism:robit")], optional=True),
        Q("mekasuit", "Комплект MekaSuit", "mekanism:mekasuit_bodyarmor", 0, 1,
          text=["Атомный сплав, предельные схемы, алмазы — четыре части. Пока пустые."],
          tasks=[item("mekanism:mekasuit_helmet"), item("mekanism:mekasuit_bodyarmor"),
                 item("mekanism:mekasuit_pants"), item("mekanism:mekasuit_boots")]),
        Q("modification", "Станция модификации", "mekanism:modification_station", 0, 2,
          text=["Модули входят и выходят. Уровни складываются."],
          tasks=[item("mekanism:modification_station"), item("mekanism:module_base", 4)]),
        Q("modules_core", "Базовые модули", "mekanism:module_energy_unit", 0, 3,
          text=["Ёмкость, солнечная зарядка, распределение заряда. Без них костюм пуст "
                "через минуту. Электролитическое дыхание — бесконечный воздух под водой."],
          tasks=[item("mekanism:module_energy_unit"), item("mekanism:module_electrolytic_breathing_unit"),
                 item("mekanism:module_inhalation_purification_unit")]),
        Q("modules_move", "Движение", "mekanism:module_gravitational_modulating_unit", 1, 3,
          text=["Гравитационный модулятор — полёт творческого режима в выживании. "
                "Гидравлика — прыжок, ускорение — бег, и ещё лава и лёд под ногами."],
          tasks=[item("mekanism:module_gravitational_modulating_unit"), item("mekanism:module_hydraulic_propulsion_unit"),
                 item("mekanism:module_locomotive_boosting_unit")]),
        Q("modules_util", "Полезное", "mekanism:module_vision_enhancement_unit", 2, 3,
          text=["Ночное зрение, магнит, стабилизация, защита от лазеров и радиации, "
                "счётчик и питание — в шлем и нагрудник."],
          tasks=[item("mekanism:module_vision_enhancement_unit"), item("mekanism:module_magnetic_attraction_unit"),
                 item("mekanism:module_radiation_shielding_unit")]),
        Q("mekatool", "Meka-Tool", "mekanism:meka_tool", 0, 4,
          text=["Жила целиком, удача или шёлк, вспашка, стрижка, телепорт, удар. "
                "Последний инструмент, который вы сделаете."],
          tasks=[item("mekanism:meka_tool"), item("mekanism:module_excavation_escalation_unit"),
                 item("mekanism:module_vein_mining_unit")],
          rewards=["Финальный инструмент технологической ветки"]),
        Q("laser", "Лазеры", "mekanism:laser", -1, 3,
          deps=["modification"],
          text=["Режет на расстоянии. Усилитель копит, тяговый луч собирает дроп."],
          tasks=[item("mekanism:laser"), item("mekanism:laser_amplifier"), item("mekanism:laser_tractor_beam")],
          optional=True),
        Q("security", "Безопасность", "mekanism:security_desk", -1, 4,
          deps=["modification"],
          text=["Машины — только своим."],
          tasks=[item("mekanism:security_desk")], optional=True),
    ]),
)
