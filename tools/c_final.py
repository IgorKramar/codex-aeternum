# -*- coding: utf-8 -*-
from dsl import chapter, Q, item, adv, dim, check, chain

chapter(
    "final_bridges", "final", 10, "Мосты между модами", "createaddition:electric_motor",
    "Как три технологические линии соединяются в одну",
    [
        "Отдельные ветки сборки самодостаточны, но по-настоящему она "
        "раскрывается на стыках. Эта глава — карта переходов.",
        "Каждое задание здесь требует предметов из разных модов сразу: "
        "это и есть проверка того, что вы связали производство воедино.",
    ],
    [
        Q("rot_to_fe", "Вращение → FE", "createaddition:alternator", 0, 0,
          text=[
              "Генератор Create Addition превращает вращение в FE. "
              "Отсюда энергия идёт в конденсаторы Immersive Engineering "
              "и энергокубы Mekanism.",
              "Обратный переход — электромотор: FE снова становится "
              "вращением, что позволяет питать машины Create от "
              "реактора Mekanism.",
          ],
          tasks=[item("createaddition:alternator"),
                 item("createaddition:electric_motor"),
                 item("immersiveengineering:capacitor_lv"),
                 item("mekanism:basic_energy_cube")],
          rewards=["Единая энергосистема всей базы"]),

        Q("ore_chain", "Единая цепочка руды", "mekanism:chemical_dissolution_chamber", 1, 0,
          text=[
              "Три мода дают три ступени переработки: жёрнов и "
              "дробильные колёса Create (×2), дробилка Immersive "
              "Engineering (×2 с побочными продуктами), цепочка "
              "Mekanism (×5).",
              "Оптимально: добыча экскаватором IE или цифровым "
              "шахтёром Mekanism, переработка в Mekanism, "
              "распределение через Refined Storage.",
          ],
          tasks=[item("create:crushing_wheel"), item("immersiveengineering:crusher"),
                 item("mekanism:chemical_dissolution_chamber")]),

        Q("fuel_chain", "Топливная цепочка", "immersiveengineering:refinery", 2, 0,
          text=[
              "Растительное масло и этанол IE, биоэтанол Create "
              "Addition и биотопливо Mekanism делаются из одного и "
              "того же — урожая.",
              "Клош IE и автоматическая ферма Create закрывают "
              "потребность в сырье полностью.",
          ],
          tasks=[item("immersiveengineering:cloche"),
                 item("immersiveengineering:biodiesel_bucket"),
                 item("createaddition:bioethanol_bucket")]),

        Q("storage_bridge", "Хранилище как хаб", "refinedstorage:external_storage", 0, 1,
          text=[
              "Внешнее хранилище Refined Storage подключает к сети "
              "хранилище Create, бины Mekanism, силосы IE и стойки "
              "MineColonies.",
              "В результате склад колонии, склад фабрики и сеть "
              "автокрафта становятся одним инвентарём.",
          ],
          tasks=[item("refinedstorage:external_storage"),
                 item("create:item_vault"), item("mekanism:basic_bin")]),

        Q("autocraft_bridge", "Автокрафт поверх всего", "refinedstorage:autocrafter", 1, 1,
          text=[
              "Автокрафтер умеет работать не только с верстаком: "
              "он выдаёт компоненты в дробилку IE, механические "
              "крафтеры Create или обогатительную камеру Mekanism "
              "и забирает результат.",
              "Так один заказ в гриде запускает цепочку через три мода.",
          ],
          tasks=[item("refinedstorage:autocrafter"),
                 item("refinedstorage:pattern", 16)],
          rewards=["Производство любого предмета сборки одним щелчком"]),

        Q("logistics_bridge", "Две логистики", "create:stock_ticker", 2, 1,
          text=[
              "Create 6 и Refined Storage решают одну задачу по-разному: "
              "первый возит физические посылки, второй телепортирует "
              "данные.",
              "Разумный компромисс: RS на базе, посылки Create — "
              "между удалёнными площадками и колонией.",
          ],
          tasks=[item("create:stock_ticker"), item("refinedstorage:grid")]),

        Q("colony_bridge", "Колония и техника", "minecolonies:blockhutmechanic", 0, 2,
          text=[
              "Механик колонии умеет делать детали технологических "
              "модов, если рецепт разучен. Курьер разносит их по "
              "зданиям, а склад подключается к сети RS.",
              "Итог: колония начинает снабжать вашу фабрику, а "
              "фабрика — колонию.",
          ],
          tasks=[item("minecolonies:blockhutmechanic"),
                 item("minecolonies:blockhutwarehouse")]),

        Q("transport_bridge", "Транспорт", "create:track_station", 1, 2,
          text=[
              "Поезда Create возят руду с шахты, дирижабли Aeronautics — "
              "грузы через сложный рельеф, телепорты Mekanism и "
              "путевые камни — игрока.",
              "Переносные интерфейсы Create и энергоинтерфейс Create "
              "Addition разгружают транспорт автоматически.",
          ],
          tasks=[item("create:track_station"),
                 item("create:portable_storage_interface"),
                 item("mekanism:teleporter")]),

        Q("defense_bridge", "Оборона", "create_radar:fire_controller", 2, 2,
          text=[
              "Турели IE защищают базу от мобов, стража MineColonies — "
              "колонию от набегов, артиллерия Big Cannons с радаром — "
              "от игроков и воздушных целей.",
              "Все три системы питаются от общей энергосети.",
          ],
          tasks=[item("immersiveengineering:turret_gun"),
                 item("minecolonies:blockhutbarracks"),
                 item("create_radar:fire_controller")]),

        Q("adventure_bridge", "Приключение и техника", "mekanism:meka_tool", 0, 3,
          text=[
              "Технологическое снаряжение резко упрощает "
              "приключенческие моды: MekaSuit держит удар боссов "
              "Eternal Tales, дрель IE копает Сумеречный лес, "
              "джетпак заменяет крылья Aether.",
              "И наоборот: артефакты Eternal Tales и Aether "
              "усиливают выживаемость на опасных производствах.",
          ],
          tasks=[item("mekanism:meka_tool"),
                 item("mekanism:mekasuit_bodyarmor")]),
    ],
)

chapter(
    "final_goals", "final", 20, "Финальные цели", "minecraft:nether_star",
    "Чем заканчивается сборка",
    [
        "У сборки нет одного финала — у неё их десять. Ниже собраны "
        "вершины каждой ветки. Пройти все — значит увидеть всё, "
        "что она может предложить.",
    ],
    [
        Q("goal_create", "Вершина Create", "create:factory_gauge", 0, 0,
          text=[
              "Полностью автоматизированная фабрика на фабричных "
              "указателях, железная дорога между площадками и "
              "летающая база на Create Aeronautics.",
          ],
          tasks=[item("create:factory_gauge", 4), item("create:steam_engine", 4),
                 item("simulated:physics_assembler")]),

        Q("goal_ie", "Вершина Immersive Engineering", "immersiveengineering:excavator", 1, 0,
          text=[
              "Экскаватор на найденной керном жиле, дуговая печь, "
              "дизель-генераторы на собственном биодизеле и полный "
              "набор инструментов инженера.",
          ],
          tasks=[item("immersiveengineering:excavator"),
                 item("immersiveengineering:arc_furnace"),
                 item("immersiveengineering:diesel_generator"),
                 item("immersiveengineering:railgun")]),

        Q("goal_mek", "Вершина Mekanism", "mekanism:pellet_antimatter", 2, 0,
          text=[
              "Термоядерный реактор, паровая турбина, SPS с "
              "антивеществом и полностью собранный MekaSuit.",
          ],
          tasks=[item("mekanism:pellet_antimatter"),
                 item("mekanism:mekasuit_bodyarmor"),
                 item("mekanism:meka_tool"),
                 item("mekanismgenerators:fusion_reactor_controller")]),

        Q("goal_storage", "Вершина хранения", "refinedstorage:64k_storage_disk", 0, 1,
          text=[
              "Сеть с дисками 64k, беспроводным доступом и "
              "автокрафтом произвольной глубины — или полный "
              "набор дисков QIO Mekanism.",
          ],
          tasks=[item("refinedstorage:64k_storage_disk"),
                 item("refinedstorage:wireless_grid"),
                 item("mekanism:qio_drive_supermassive")]),

        Q("goal_colony", "Вершина колонии", "minecolonies:blockhuttownhall", 1, 1,
          text=[
              "Колония пятого уровня со всеми зданиями, полным "
              "деревом исследований и гарнизоном, который отражает "
              "любой набег.",
          ],
          tasks=[adv("minecolonies:minecolonies/colony_population_50"),
                 item("minecolonies:blockhutuniversity"),
                 item("minecolonies:blockhutbarracks")]),

        Q("goal_adventure", "Вершина приключений", "twilightforest:lamp_of_cinders", 2, 1,
          text=[
              "Все три подземелья Aether, полная цепочка боссов "
              "Сумеречного леса и Светоч углей в руках.",
          ],
          tasks=[item("aether:hammer_of_kingbdogz"),
                 item("twilightforest:lamp_of_cinders"),
                 item("twilightforest:trophy_pedestal")]),

        Q("goal_eternal", "Вершина Eternal Tales", "eternal_tales:the_ultimate_two", 0, 2,
          text=[
              "Все девять измерений, победа над Унахзаалом, "
              "Ultimate World и предельные предметы Аркемеров.",
          ],
          tasks=[adv("eternal_tales:kill_unahzaal"),
                 adv("eternal_tales:enter_in_the_ultimate_world"),
                 adv("eternal_tales:get_the_ultimate_two"),
                 adv("eternal_tales:pass_all_quests")]),

        Q("goal_space", "Вершина космоса", "ad_astra:tier_4_rocket", 0, 3,
          text=[
              "Ракета четвёртого уровня, реактивный костюм и база на Глейсио с "
              "распылителем кислорода. Другая звёздная система, обжитая всерьёз.",
          ],
          tasks=[item("ad_astra:tier_4_rocket"), item("ad_astra:jet_suit"),
                 adv("ad_astra:interstellar")]),

        Q("goal_magic", "Вершина магии", "botania:dice", 1, 3,
          text=[
              "Страж Гайи во второй ипостаси, Кости судьбы и хотя бы одна реликвия. "
              "Цветочная магия, доведённая до конца.",
          ],
          tasks=[item("botania:dice"), adv("botania:challenge/gaia_guardian_hardmode")]),

        Q("goal_hunt", "Вершина охоты", "cataclysm:the_incinerator", 2, 3,
          text=[
              "Все десять боссов Катаклизма и полный комплект брони Игнитиума. "
              "Трофейный зал, в котором нет пустых мест.",
          ],
          tasks=[adv("cataclysm:kill_all_bosses"),
                 item("cataclysm:ignitium_elytra_chestplate")]),

        Q("goal_all", "Всё сразу", "minecraft:nether_star", 1, 4,
          deps=["goal_create", "goal_ie", "goal_mek", "goal_storage",
                "goal_colony", "goal_adventure", "goal_eternal",
                "goal_space", "goal_magic", "goal_hunt"],
          shape="big",
          text=[
              "Десять вершин пройдены. Дальше сборка не ведёт вас "
              "никуда — дальше вы ведёте её сами.",
              "Хорошая следующая цель: построить то, что не "
              "предусмотрено ни одним модом, но возможно из их "
              "деталей.",
          ],
          tasks=[item("minecraft:nether_star")],
          rewards=["Полное прохождение сборки"]),
    ],
)
