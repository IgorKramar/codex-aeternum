# -*- coding: utf-8 -*-
from dsl import chapter, Q, item, adv, check, chain

chapter(
    "cbc_foundry", "createx", 40, "Big Cannons: литейная", "createbigcannons:cast_iron_ingot",
    "Металлы, формы и первое орудие",
    [
        "Create Big Cannons — полноценная артиллерия: стволы отливаются из расплава, "
        "рассверливаются, свариваются в секции, заряжаются пороховыми зарядами и "
        "снарядами, а прочность блоков в мире действительно учитывается при попадании.",
        "Металлы идут по возрастанию: чугун, бронза, сталь, незеритовая сталь. "
        "Чем лучше металл, тем больший заряд выдерживает ствол.",
    ],
    chain([
        Q("melting", "Плавка металла", "createbigcannons:molten_cast_iron_bucket", 0, 0,
          text=[
              "Металл плавится в чаше Create под крышкой литейной (Basin Foundry Lid) "
              "на сильном нагреве. Чугун получается из железа и угля, бронза — из меди "
              "и цинка, сталь — из железа с добавками.",
              "Расплав хранится в обычных баках Create и разливается разливщиком.",
          ],
          tasks=[item("createbigcannons:basin_foundry_lid"),
                 item("createbigcannons:molten_cast_iron_bucket")]),

        Q("sand", "Формовочный песок", "createbigcannons:casting_sand", 0, 1,
          text=["Литейный песок — расходник для форм. Делается из песка и глины."],
          tasks=[item("createbigcannons:casting_sand", 16)]),

        Q("cast", "Форма для ствола", "createbigcannons:cannon_cast", 0, 2,
          text=[
              "Форма собирается из секций разного диаметра (very small, small, medium, "
              "large, very large). Залейте расплав, дождитесь застывания — получится "
              "готовая форма (Finished Cannon Cast).",
              "Секции определяют калибр будущего орудия.",
          ],
          tasks=[item("createbigcannons:cannon_cast", 4),
                 item("createbigcannons:small_cast_mould")]),

        Q("drill", "Рассверливание", "createbigcannons:cannon_drill", 0, 3,
          text=[
              "Отлитая заготовка (unbored) непригодна к стрельбе: её нужно рассверлить "
              "сверлильным станком. Станок — это контрапция с буровой головкой, "
              "которая едет вдоль ствола.",
              "Только после рассверливания ствол становится рабочим.",
          ],
          tasks=[item("createbigcannons:cannon_drill"),
                 item("createbigcannons:cannon_drill_bit")]),

        Q("barrel", "Первый ствол", "createbigcannons:cast_iron_cannon_barrel", 0, 4,
          text=[
              "Чугунный ствол — самый дешёвый. Он выдерживает только слабые заряды, "
              "но этого достаточно, чтобы понять механику.",
              "Ствол собирается из секций: казённая часть (chamber), несколько "
              "стволовых секций (barrel) и дульная (end).",
          ],
          tasks=[item("createbigcannons:cast_iron_cannon_barrel", 3),
                 item("createbigcannons:cast_iron_cannon_chamber"),
                 item("createbigcannons:cast_iron_cannon_end")]),

        Q("welder", "Сварка секций", "createbigcannons:cannon_welder", 1, 4,
          text=["Сварщик соединяет отдельные секции в единое орудие. Без сварки "
                "выстрел разорвёт стык."],
          tasks=[item("createbigcannons:cannon_welder")]),

        Q("mount", "Лафет и станок", "createbigcannons:cannon_mount", 0, 5,
          text=[
              "Подвижный лафет (Cannon Mount) наводит орудие по горизонтали и вертикали "
              "и управляется штурвалом Create или контроллером наведения.",
              "Неподвижный станок (Fixed Cannon Mount) дешевле, но не поворачивается; "
              "полевой лафет (Cannon Carriage) на колёсах перевозится вручную.",
          ],
          tasks=[item("createbigcannons:cannon_mount"),
                 item("createbigcannons:cannon_carriage")]),

        Q("powder", "Пороховой заряд", "createbigcannons:powder_charge", 0, 6,
          text=[
              "Заряд — это спрессованный порох в оболочке. Количество зарядов "
              "определяет дальность и урон, но превышение предела прочности ствола "
              "приводит к разрыву.",
              "Хлопковый порох (Guncotton) и нитропорох мощнее обычного.",
          ],
          tasks=[item("createbigcannons:powder_charge", 4),
                 item("createbigcannons:packed_gunpowder", 4)]),

        Q("shot", "Первый выстрел", "createbigcannons:solid_shot", 0, 7,
          text=[
              "Порядок заряжания: заряд, затем снаряд, затем поджиг (кремень или "
              "красный камень на казённой части).",
              "Сплошное ядро (Solid Shot) пробивает, картечь (Bag of Grapeshot) "
              "поражает по площади, каменное ядро — самый дешёвый вариант.",
          ],
          tasks=[item("createbigcannons:solid_shot"),
                 item("createbigcannons:bag_of_grapeshot")],
          rewards=["Работающее артиллерийское орудие"]),

        Q("loader", "Автозаряжание", "createbigcannons:cannon_loader", 0, 8,
          text=[
              "Заряжающий (Cannon Loader) вместе с досылателем (Ram Rod) и "
              "прочищателем (Worm) автоматизирует цикл: извлечь гильзу, прочистить, "
              "зарядить, выстрелить.",
              "Собранная батарея с автозаряжанием стреляет непрерывно.",
          ],
          tasks=[item("createbigcannons:cannon_loader"),
                 item("createbigcannons:ram_rod"), item("createbigcannons:worm")]),
    ]),
)

chapter(
    "cbc_advanced", "createx", 50, "Big Cannons: тяжёлое вооружение",
    "createbigcannons:steel_cannon_barrel",
    "Сталь, автопушки и специальные снаряды",
    [],
    chain([
        Q("bronze", "Бронза", "createbigcannons:bronze_ingot", 0, 0,
          text=["Бронзовые стволы держат больший заряд, чем чугунные, и не так "
                "быстро изнашиваются."],
          tasks=[item("createbigcannons:bronze_cannon_barrel", 3)]),

        Q("steel", "Сталь", "createbigcannons:steel_ingot", 0, 1,
          text=[
              "Стальные орудия — рабочая лошадка мода. Появляются составные стволы "
              "(Built-Up), собранные из нескольких слоёв: они выдерживают "
              "максимальные заряды.",
          ],
          tasks=[item("createbigcannons:steel_cannon_barrel", 3),
                 item("createbigcannons:built_up_steel_cannon_barrel")]),

        Q("nethersteel", "Незеритовая сталь", "createbigcannons:nethersteel_ingot", 0, 2,
          text=[
              "Вершина линейки. Незеритовые стволы и винтовые затворы (Screw Breech) "
              "позволяют стрелять самыми мощными зарядами без риска разрыва.",
          ],
          tasks=[item("createbigcannons:nethersteel_cannon_barrel", 3),
                 item("createbigcannons:nethersteel_screw_breech")]),

        Q("breech", "Затворы", "createbigcannons:steel_sliding_breech", 1, 1,
          deps=["steel"],
          text=[
              "Дульнозарядное орудие требует прочистки после каждого выстрела. "
              "Клиновой затвор (Sliding Breech) заряжается с казны, быстрозарядный "
              "(Quickfiring) работает с гильзами.",
          ],
          tasks=[item("createbigcannons:steel_sliding_breech"),
                 item("createbigcannons:steel_quickfiring_breech")]),

        Q("shells", "Снаряды", "createbigcannons:he_shell", 0, 3,
          text=[
              "Фугасный (HE) взрывается, бронебойный (AP) пробивает, шрапнельный "
              "накрывает пехоту, дымовой ставит завесу, жидкостный разливает "
              "содержимое бака.",
              "К каждому снаряду подбирается взрыватель: ударный, инерционный, "
              "временной, дистанционный или проводной.",
          ],
          tasks=[item("createbigcannons:he_shell"), item("createbigcannons:ap_shell"),
                 item("createbigcannons:impact_fuze"), item("createbigcannons:timed_fuze")]),

        Q("autocannon", "Автопушка", "createbigcannons:steel_autocannon_barrel", 0, 4,
          text=[
              "Автопушка стреляет очередями из унитарных патронов. Нужны ствол, "
              "затвор с экстрактором и возвратная пружина.",
              "Патроны собираются из гильз, пороха и снарядов; контейнер боепитания "
              "(Ammo Container) подаёт ленту.",
          ],
          tasks=[item("createbigcannons:steel_autocannon_barrel"),
                 item("createbigcannons:steel_autocannon_breech"),
                 item("createbigcannons:autocannon_ammo_container")],
          rewards=["Скорострельное автоматическое оружие"]),

        Q("autoammo", "Патроны автопушки", "createbigcannons:filled_autocannon_cartridge", 1, 4,
          deps=["autocannon"],
          text=[
              "Бронебойный, зажигательный и зенитный (Flak) патроны решают разные "
              "задачи. Трассирующая насадка помогает корректировать огонь.",
          ],
          tasks=[item("createbigcannons:ap_autocannon_round"),
                 item("createbigcannons:flak_autocannon_round"),
                 item("createbigcannons:tracer_tip")]),

        Q("mortar", "Мортира", "createbigcannons:drop_mortar_shell", -1, 4,
          deps=["bronze"],
          text=["Мортира стреляет навесом на короткую дистанцию. Дешёвая и "
                "эффективная против укреплений."],
          tasks=[item("createbigcannons:drop_mortar_shell")],
          optional=True),

        Q("armor", "Броня и защита", "createbigcannons:block_armor_inspection_tool", 0, 5,
          text=[
              "Инструмент осмотра брони показывает, какой блок какой заряд выдержит. "
              "Противогаз (Gas Mask) защищает от газовых снарядов.",
              "Планируя укрепление, проверяйте блоки этим инструментом — интуиция "
              "здесь обманывает.",
          ],
          tasks=[item("createbigcannons:block_armor_inspection_tool"),
                 item("createbigcannons:gas_mask")]),
    ]),
)

chapter(
    "radar", "createx", 60, "Create Radar: наведение", "create_radar:plane_radar",
    "Обнаружение целей, ПВО и автоматическая наводка",
    [
        "Create Radar связывает артиллерию с электроникой: радары находят цели, "
        "контроллеры наводят орудия, система опознавания отличает своих от чужих.",
    ],
    chain([
        Q("plate", "Радарные пластины", "create_radar:radar_plate_block", 0, 0,
          text=[
              "Антенна радара собирается из пластин; чем больше площадь, тем дальше "
              "дальность обнаружения. Тарелка (Radar Dish) — компактный вариант.",
          ],
          tasks=[item("create_radar:radar_plate_block", 8)]),

        Q("radar", "Радар", "create_radar:plane_radar", 0, 1,
          text=[
              "Радар обнаруживает движущиеся физические объекты и существа в секторе "
              "обзора и передаёт координаты по линии данных.",
          ],
          tasks=[item("create_radar:plane_radar"), item("create_radar:radar_bearing")]),

        Q("datalink", "Линия данных", "create_radar:data_link", 0, 2,
          text=["Линия данных соединяет радар, монитор и контроллеры. Фильтры "
                "(целевой, идентификационный, сетевой) отсеивают лишние отметки."],
          tasks=[item("create_radar:data_link"), item("create_radar:monitor")]),

        Q("iff", "Свой — чужой", "create_radar:identification_transponder", 1, 2,
          text=[
              "Транспондер помечает ваш объект как дружественный, зона безопасности "
              "(Safe Zone Designator) исключает участок из обстрела, приёмник "
              "предупреждения (RWR) сообщает, что вас облучают чужим радаром.",
          ],
          tasks=[item("create_radar:identification_transponder"),
                 item("create_radar:radar_warning_receiver")]),

        Q("controllers", "Контроллеры наведения", "create_radar:auto_yaw_controller", 0, 3,
          text=[
              "Автоматические контроллеры курса и тангажа наводят лафет на цель, "
              "полученную от радара. Контроллер огня (Fire Controller) даёт "
              "команду на выстрел с учётом упреждения.",
          ],
          tasks=[item("create_radar:auto_yaw_controller"),
                 item("create_radar:auto_pitch_controller"),
                 item("create_radar:fire_controller")],
          rewards=["Автоматическая турель"]),

        Q("guidance", "Наведение снарядов", "create_radar:guided_fuze", 0, 4,
          text=[
              "Управляемый взрыватель и модуль ARAD наводят снаряд на цель или на "
              "источник радиоизлучения. Глушилка (Jammer) срывает чужое наведение.",
          ],
          tasks=[item("create_radar:guided_fuze"), item("create_radar:arad_guidance"),
                 item("create_radar:jammer")]),

        Q("misc_radar", "Прочее", "create_radar:binoculars", 1, 4,
          text=["Бинокль приближает изображение и подсвечивает цели, радио "
                "передаёт голос и сигналы на расстояние."],
          tasks=[item("create_radar:binoculars"), item("create_radar:radio")],
          optional=True),
    ]),
)

chapter(
    "missiles", "createx", 70, "Ракеты", "cbcaeronauticsmissiles:rocket_motor",
    "CBC Aeronautics Missiles: управляемое ракетное оружие",
    [
        "Небольшой мод, который сшивает Big Cannons, Aeronautics и Radar: ракета — "
        "это физический объект с двигателем, рулями и системой наведения.",
    ],
    chain([
        Q("motor_rocket", "Ракетный двигатель", "cbcaeronauticsmissiles:rocket_motor", 0, 0,
          text=["Двигатель даёт тягу физическому объекту. Чем больше двигателей, "
                "тем выше скорость и меньше время работы."],
          tasks=[item("cbcaeronauticsmissiles:rocket_motor")]),

        Q("fins", "Рули", "cbcaeronauticsmissiles:actuator_fins", 0, 1,
          text=["Подвижные рули поворачивают ракету в полёте по командам "
                "вычислителя наведения."],
          tasks=[item("cbcaeronauticsmissiles:actuator_fins", 4)]),

        Q("computer", "Вычислитель наведения", "cbcaeronauticsmissiles:guidance_computer", 0, 2,
          text=[
              "Вычислитель принимает цель от интерфейса наведения или радара и "
              "ведёт ракету, управляя рулями.",
          ],
          tasks=[item("cbcaeronauticsmissiles:guidance_computer"),
                 item("cbcaeronauticsmissiles:targeting_interface")]),

        Q("fuze_prox", "Неконтактный взрыватель", "cbcaeronauticsmissiles:aircraft_proximity_fuze",
          1, 2,
          text=["Подрывает боевую часть при сближении с воздушной целью — "
                "основа зенитных ракет."],
          tasks=[item("cbcaeronauticsmissiles:aircraft_proximity_fuze")]),

        Q("mount_missile", "Пусковая установка", "cbcaeronauticsmissiles:missile_mount", 0, 3,
          text=[
              "Крепление удерживает ракету до пуска и отпускает её по сигналу. "
              "Вместе с радаром и контроллером огня получается полноценный "
              "зенитно-ракетный комплекс.",
          ],
          tasks=[item("cbcaeronauticsmissiles:missile_mount")],
          rewards=["Управляемое ракетное вооружение"]),
    ]),
)
