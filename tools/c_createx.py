# -*- coding: utf-8 -*-
from dsl import chapter, Q, item, adv, check, chain

chapter(
    "ca_electric", "createx", 10, "Create Addition: электричество", "createaddition:electric_motor",
    "Превращение вращения в энергию и обратно",
    [
        "Три технологии сборки говорят на разных языках: Create — на вращении, "
        "Immersive Engineering и Mekanism — на энергии. Create Addition — переводчик. "
        "Без него три завода стояли бы рядом и не знали друг о друге.",
    ],
    chain([
        Q("rolling", "Прокатный стан", "createaddition:rolling_mill", 0, 0,
          text=["Слиток в стержень, стержень в проволоку. Без проволоки нет катушек, "
                "без катушек — проводов."],
          tasks=[item("createaddition:rolling_mill")]),
        Q("wire", "Проволока и катушки", "createaddition:copper_wire", 0, 1,
          text=["Медь проводит, золото лучше, электрум — лучше всех. Проволока на катушке "
                "становится проводом, который тянут между коннекторами."],
          tasks=[item("createaddition:copper_wire", 8), item("createaddition:copper_spool")]),
        Q("electrum", "Электрум", "createaddition:electrum_ingot", 1, 1,
          text=["Золото с цинком в смесителе. Лучший проводник мода и материал амулета, "
                "который хранит опыт."],
          tasks=[item("createaddition:electrum_ingot", 8)]),
        Q("alternator", "Генератор", "createaddition:alternator", 0, 2,
          text=["Вал заходит — энергия выходит. Быстрее вал — больше энергии и больше "
                "нагрузки. Водяное колесо, регулятор, генератор: первая электростанция "
                "сборки помещается на столе."],
          tasks=[item("createaddition:alternator")],
          rewards=["Первая энергия FE"]),
        Q("motor", "Электромотор", "createaddition:electric_motor", 1, 2,
          text=["Обратный перевод: энергия в вращение, с настраиваемой скоростью. Мотор "
                "в локомотиве вместо котла — и поезд заряжается на станции, как телефон."],
          tasks=[item("createaddition:electric_motor")]),
        Q("connector", "Коннекторы и провода", "createaddition:connector", 0, 3,
          text=["Коннектор на машину, провод между коннекторами. Большой держит больший ток, "
                "световой питает лампы, реле рвёт цепь по сигналу."],
          tasks=[item("createaddition:connector", 4), item("createaddition:redstone_relay")]),
        Q("accumulator", "Аккумулятор", "createaddition:accumulator", 0, 4,
          text=["Хранит. Модульный срастается в батарею любого размера."],
          tasks=[item("createaddition:accumulator")]),
        Q("burner", "Жидкостная горелка", "createaddition:liquid_blaze_burner", -1, 4,
          text=["Ифрит на пенсии: горелка на биоэтаноле или масле греет чашу не хуже. "
                "Биомасса из растений, пеллеты под прессом, перегонка — и топливо растёт "
                "на грядке."],
          tasks=[item("createaddition:liquid_blaze_burner"), item("createaddition:bioethanol_bucket")]),
        Q("tesla", "Катушка Теслы", "createaddition:tesla_coil", 1, 4,
          text=["Молния по всему живому вокруг. Заодно заряжает предметы и превращает "
                "песок в стекло на ленте. Не ставьте у входа."],
          tasks=[item("createaddition:tesla_coil")]),
        Q("digital", "Цифровой адаптер", "createaddition:digital_adapter", 0, 5,
          deps=["accumulator", "connector"],
          text=["Читает машину Create и говорит цифрами: уровень, скорость, наличие."],
          tasks=[item("createaddition:digital_adapter")]),
        Q("pei", "Переносной энергоинтерфейс", "createaddition:portable_energy_interface", 1, 5,
          deps=["accumulator"],
          text=["Энергия между контрапцией и сетью. Поезд подъехал — зарядился — уехал."],
          tasks=[item("createaddition:portable_energy_interface")]),
    ]),
)

chapter(
    "aero_basics", "createx", 20, "Create Aeronautics: полёт", "aeronautics:white_envelope",
    "Настоящая физика, дирижабли и левитит",
    [
        "Create Aeronautics не притворяется. Конструкция здесь не телепортируется по "
        "точкам — она летит: кренится под весом, теряет высоту, когда гаснет горелка, "
        "и разбивается, если пилот забыл, что земля твёрдая.",
        "В комплекте ещё два мода: Create Simulated — сенсоры, верёвки, физические "
        "механизмы — и Create Offroad, который ставит всё это на колёса.",
    ],
    chain([
        Q("assembler", "Физический сборщик", "simulated:physics_assembler", 0, 0,
          text=["Щелчок — и постройка перестаёт быть частью мира. У неё появляется масса, "
                "инерция и способность упасть. Разбирается тем же блоком."],
          tasks=[item("simulated:physics_assembler")],
          rewards=["Доступ ко всей физической технике"]),
        Q("levitite", "Левитит", "aeronautics:levitite", 0, 1,
          text=["Материал с отрицательной массой. Смесь варится в чаше из порошка эндера, "
                "разливается и застывает в блоки, которые тянут вверх. Перламутровый — "
                "для тяжёлых судов."],
          tasks=[item("aeronautics:levitite_blend_bucket"), item("aeronautics:levitite", 8)]),
        Q("envelope", "Оболочка дирижабля", "aeronautics:white_envelope", 0, 2,
          text=["Баллон. Его объём — подъёмная сила. Оболочка с валом внутри пропускает "
                "вращение сквозь себя. Шестнадцать цветов."],
          tasks=[item("aeronautics:white_envelope", 16)]),
        Q("burner_aero", "Регулируемая горелка", "aeronautics:adjustable_burner", 1, 2,
          text=["Греет воздух в оболочке. Сильнее огонь — выше. Сигнал — регулятор."],
          tasks=[item("aeronautics:adjustable_burner")]),
        Q("airship", "Первый дирижабль", "aeronautics:steam_vent", 0, 3,
          deps=["assembler", "envelope", "burner_aero"],
          text=[
              "Гондола, оболочка сверху, горелка, паровой клапан для сброса, сборщик. "
              "Первый подъём — всегда криво; первый полёт над своей базой — всегда молча.",
          ],
          tasks=[item("aeronautics:steam_vent")],
          rewards=["Собственный летающий корабль"]),
        Q("propeller", "Пропеллеры", "aeronautics:wooden_propeller", 0, 4,
          text=["Деревянный лёгкий, андезитовый прочный, умный меняет шаг на лету. "
                "На подшипник пропеллера, на вал, вперёд."],
          tasks=[item("aeronautics:wooden_propeller"), item("aeronautics:propeller_bearing")]),
        Q("gyro", "Гироскопы", "aeronautics:gyroscopic_propeller_bearing", 1, 4,
          text=["Без гироскопа корабль кренится и однажды переворачивается. С гироскопом — "
                "стоит в воздухе, как на столе."],
          tasks=[item("aeronautics:gyroscopic_propeller_bearing"), item("simulated:gyroscopic_mechanism")]),
        Q("goggles_aero", "Очки авиатора", "aeronautics:aviators_goggles", 2, 4,
          text=["Высота, скорость, крен, тангаж — на стекле."],
          tasks=[item("aeronautics:aviators_goggles")]),
        Q("sensors", "Сенсоры", "simulated:altitude_sensor", 0, 5,
          deps=["airship"],
          text=["Высотомер, гиросенсор, оптика, лазер. Автопилот собирается из них: "
                "высотомер держит эшелон, гиросенсор ровняет крылья."],
          tasks=[item("simulated:altitude_sensor"), item("simulated:gimbal_sensor"), item("simulated:laser_sensor")]),
        Q("engine", "Портативный двигатель", "simulated:black_portable_engine", 0, 6,
          deps=["sensors"],
          text=["Вращение на борту, без котла и валов с земли."],
          tasks=[item("simulated:engine_assembly"), item("simulated:black_portable_engine")]),
        Q("docking", "Стыковка и швартовка", "simulated:docking_connector", 1, 6,
          deps=["sensors"],
          text=["Разъём соединяет два судна, парный — шарнир. Верёвки буксируют "
                "и швартуют. Порт для дирижаблей — реальность."],
          tasks=[item("simulated:docking_connector"), item("simulated:rope_connector")]),
        Q("navigation", "Навигационный стол", "simulated:navigation_table", 0, 7,
          deps=["engine", "docking"],
          text=["Карта, маршрут, печатная машинка с программой и приёмник. Корабль, "
                "который летит сам, пока вы спите в его трюме."],
          tasks=[item("simulated:navigation_table")],
          rewards=["Автономные полёты по маршруту"]),
    ]),
)

chapter(
    "offroad", "createx", 30, "Create Offroad: наземная техника", "offroad:tire",
    "Колёса, подвеска и вездеходы",
    [],
    chain([
        Q("wheel_mount", "Ступица", "offroad:wheel_mount", 0, 0,
          text=["Колесо на ось, вращение на колесо. Четыре — машина."],
          tasks=[item("offroad:wheel_mount", 4)]),
        Q("tires", "Шины", "offroad:tire", 0, 1,
          text=["Маленькие, обычные, большие, чудовищные. Липкие версии — Sticky Wheels — "
                "держат склон и лёд."],
          tasks=[item("offroad:tire", 4), item("offroad:sticky_tire", 4)]),
        Q("borehead", "Буровая головка", "offroad:borehead_bearing", 0, 2,
          text=["Породорежущее колесо на физическом шасси. Тоннель за вами закрывается "
                "темнотой."],
          tasks=[item("offroad:borehead_bearing"), item("offroad:rockcutting_wheel")], optional=True),
        Q("vehicle", "Первая машина", "offroad:large_tire", 0, 3,
          deps=["tires"],
          text=["Рама, четыре ступицы с шинами, двигатель, штурвал, направленный "
                "переключатель для руля — и сборщик. По холмам Terralith на колёсах."],
          tasks=[item("simulated:directional_gearshift")],
          rewards=["Наземный транспорт с настоящей физикой"]),
    ]),
)
