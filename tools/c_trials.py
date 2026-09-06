# -*- coding: utf-8 -*-
"""Испытания: задания со сдачей предметов и ощутимыми наградами, как в GTNH."""
from dsl import chapter, Q, item, give, adv, loot, chain

chapter(
    "trials_early", "trials", 10, "Испытания: первые дни", "minecraft:iron_pickaxe",
    "Сдайте ресурсы — получите то, что ускорит старт",
    [
        "Испытания устроены иначе, чем остальные главы. Здесь книга не просит "
        "показать предмет, а забирает его: нажмите «Сдать предметы», и они исчезнут "
        "из инвентаря в обмен на награду.",
        "Награды подобраны так, чтобы стоить больше сданного — но только в том случае, "
        "если вы пришли за ними вовремя.",
        "Без мода на сервере предметы не забираются и награда не выдаётся: испытание "
        "просто засчитывается.",
    ],
    chain([
        Q("logs", "Дровосек", "minecraft:oak_log", 0, 0,
          text=["Шестьдесят четыре бревна любого дуба. Дерево в этой сборке валится "
                "послойно, так что стопка соберётся быстрее, чем кажется."],
          tasks=[give("minecraft:oak_log", 64)],
          rewards=loot(("minecraft:iron_axe", 1), ("minecraft:bread", 16), xp=30)),

        Q("cobble", "Каменотёс", "minecraft:cobblestone", 1, 0,
          text=["Три стопки булыжника. Он всё равно копится — пусть хоть раз пригодится."],
          tasks=[give("minecraft:cobblestone", 192)],
          rewards=loot(("minecraft:stone_bricks", 128), ("minecraft:torch", 32), xp=30)),

        Q("iron", "Первое железо", "minecraft:iron_ingot", 0, 1,
          text=["Тридцать два слитка. Взамен — то, что жалко тратить самому: кирка с "
                "починкой хватит надолго."],
          tasks=[give("minecraft:iron_ingot", 32)],
          rewards=loot(("minecraft:iron_pickaxe", 1), ("minecraft:iron_ingot", 48), xp=60,
                       text="Полтора слитка за каждый сданный — по сути, удвоение руды до Create")),

        Q("food", "Кладовая", "minecraft:cooked_beef", 1, 1,
          text=["Тридцать два стейка или столько же жареной курицы. Кухня сборки скоро "
                "сделает их ненужными, а пока — хороший обмен."],
          tasks=[give("minecraft:cooked_beef", 32)],
          rewards=loot(("farmersdelight:cooking_pot", 1), ("farmersdelight:iron_knife", 1),
                       ("farmersdelight:rice", 16), xp=40)),

        Q("leather", "Кожевник", "minecraft:leather", 0, 2,
          text=["Шестнадцать кож. Рюкзаку хватит и меньше, но улучшенный рюкзак делается "
                "из железа, а железо у вас уже забрали."],
          tasks=[give("minecraft:leather", 16)],
          rewards=loot(("sophisticatedbackpacks:iron_backpack", 1), xp=60)),

        Q("glass", "Стеклодув", "minecraft:glass", 1, 2,
          text=["Шестьдесят четыре стекла. Create просит стекло почти на каждый корпус — "
                "и вот ему за это плата."],
          tasks=[give("minecraft:glass", 64)],
          rewards=loot(("create:andesite_alloy", 32), ("create:framed_glass", 16), xp=40)),
    ]),
)

chapter(
    "trials_mid", "trials", 20, "Испытания: заводской гул", "create:precision_mechanism",
    "Продукция машин в обмен на машины",
    [
        "Когда производство налажено, сдать стопку продукции легко. Награды здесь — "
        "детали, которые дороги не материалом, а временем сборки.",
    ],
    chain([
        Q("alloy", "Андезитовая река", "create:andesite_alloy", 0, 0,
          text=["Сто двадцать восемь андезитового сплава. Столько делает смеситель за "
                "пару минут — если он у вас уже есть."],
          tasks=[give("create:andesite_alloy", 128)],
          rewards=loot(("create:andesite_casing", 32), ("create:mechanical_saw", 1), xp=60)),

        Q("sheets", "Прокат", "create:iron_sheet", 1, 0,
          text=["Шестьдесят четыре железных листа и тридцать два медных."],
          tasks=[give("create:iron_sheet", 64), give("create:copper_sheet", 32)],
          rewards=loot(("create:copper_casing", 16), ("create:mechanical_press", 1), xp=80)),

        Q("brass", "Латунный стандарт", "create:brass_ingot", 0, 1,
          text=["Шестьдесят четыре слитка латуни. Первый серьёзный обмен: взамен — "
                "то, без чего латунная эпоха не начинается."],
          tasks=[give("create:brass_ingot", 64)],
          rewards=loot(("create:brass_casing", 32), ("create:crushing_wheel", 2), xp=120)),

        Q("precision", "Точная работа", "create:precision_mechanism", 1, 1,
          text=["Шестнадцать прецизионных механизмов. Если они собираются вручную — "
                "это долго; если линией крафтеров — это проверка линии."],
          tasks=[give("create:precision_mechanism", 16)],
          rewards=loot(("create:rotation_speed_controller", 4), ("create:mechanical_arm", 2), xp=200)),

        Q("steel_ie", "Сталевар", "immersiveengineering:ingot_steel", 0, 2,
          text=["Шестьдесят четыре слитка стали Immersive Engineering. Доменная печь "
                "справится за один вечер."],
          tasks=[give("immersiveengineering:ingot_steel", 64)],
          rewards=loot(("immersiveengineering:drill", 1), ("immersiveengineering:drillhead_steel", 1),
                       ("immersiveengineering:powerpack", 1), xp=150)),

        Q("coke", "Коксохимия", "immersiveengineering:coal_coke", 1, 2,
          text=["Сто двадцать восемь кокса и восемь вёдер креозота."],
          tasks=[give("immersiveengineering:coal_coke", 128), give("immersiveengineering:creosote_bucket", 8)],
          rewards=loot(("immersiveengineering:treated_wood_horizontal", 128),
                       ("immersiveengineering:cokebrick", 27), xp=80,
                       text="Второй коксовой печи хватит на всю игру")),

        Q("osmium", "Осмиевый запас", "mekanism:ingot_osmium", 0, 3,
          text=["Шестьдесят четыре осмия и тридцать две стали Mekanism."],
          tasks=[give("mekanism:ingot_osmium", 64), give("mekanism:ingot_steel", 32)],
          rewards=loot(("mekanism:steel_casing", 8), ("mekanism:basic_control_circuit", 16), xp=120)),

        Q("circuits", "Схемотехника", "mekanism:advanced_control_circuit", 1, 3,
          text=["Восемь продвинутых схем. Взамен — четыре элитных: обмен, который "
                "экономит ступень химии."],
          tasks=[give("mekanism:advanced_control_circuit", 8)],
          rewards=loot(("mekanism:elite_control_circuit", 4), ("mekanism:alloy_reinforced", 4), xp=160)),

        Q("processors", "Кремниевая долина", "refinedstorage:improved_processor", 0, 4,
          text=["Шестнадцать улучшенных процессоров Refined Storage."],
          tasks=[give("refinedstorage:improved_processor", 16)],
          rewards=loot(("refinedstorage:advanced_processor", 8), ("refinedstorage:16k_storage_disk", 1), xp=140)),

        Q("bread", "Хлебная подать", "minecraft:bread", 1, 4,
          text=["Сто двадцать восемь хлеба для колонии. Пекарь MineColonies делает "
                "столько за день, а вы получите то, что колония не делает."],
          tasks=[give("minecraft:bread", 128)],
          rewards=loot(("minecolonies:scroll_tp", 2), ("minecolonies:ancienttome", 1), xp=100)),
    ]),
)

chapter(
    "trials_late", "trials", 30, "Испытания: высокие технологии", "mekanism:pellet_polonium",
    "Сдача редких материалов на пике сборки",
    [
        "Здесь сданное действительно дорого. Награды — предметы, которых в мире "
        "нет: ускоряющие модули, диски, схемы верхнего уровня.",
    ],
    chain([
        Q("sturdy", "Тяжёлая промышленность", "create:sturdy_sheet", 0, 0,
          text=["Шестьдесят четыре прочных листа Create."],
          tasks=[give("create:sturdy_sheet", 64)],
          rewards=loot(("create:railway_casing", 16), ("create:track", 128), xp=200)),

        Q("electrum", "Проводник", "createaddition:electrum_ingot", 1, 0,
          text=["Тридцать два электрума и шестьдесят четыре электрумовой проволоки."],
          tasks=[give("createaddition:electrum_ingot", 32), give("createaddition:electrum_wire", 64)],
          rewards=loot(("createaddition:electric_motor", 2), ("createaddition:modular_accumulator", 4), xp=200)),

        Q("nethersteel", "Оружейник", "createbigcannons:nethersteel_ingot", 0, 1,
          text=["Шестнадцать слитков незеритовой стали Big Cannons."],
          tasks=[give("createbigcannons:nethersteel_ingot", 16)],
          rewards=loot(("createbigcannons:nethersteel_screw_breech", 1),
                       ("createbigcannons:he_shell", 8), xp=300)),

        Q("duroplast", "Полимеры", "immersiveengineering:plate_duroplast", 1, 1,
          text=["Тридцать два дуропласта и четыре ведра биодизеля."],
          tasks=[give("immersiveengineering:plate_duroplast", 32), give("immersiveengineering:biodiesel_bucket", 4)],
          rewards=loot(("immersiveengineering:railgun", 1), ("immersiveengineering:capacitor_hv", 1), xp=250)),

        Q("atomic", "Атомный сплав", "mekanism:alloy_atomic", 0, 2,
          text=["Шестнадцать атомных сплавов Mekanism."],
          tasks=[give("mekanism:alloy_atomic", 16)],
          rewards=loot(("mekanism:ultimate_control_circuit", 4), ("mekanism:teleportation_core", 2), xp=350)),

        Q("polonium", "Ядерный цикл", "mekanism:pellet_polonium", 1, 2,
          text=["Восемь гранул полония и восемь гранул плутония. Это доказательство "
                "работающего реактора и переработки отходов."],
          tasks=[give("mekanism:pellet_polonium", 8), give("mekanism:pellet_plutonium", 8)],
          rewards=loot(("mekanism:sps_casing", 16), ("mekanism:sps_port", 2), xp=500)),

        Q("disks", "Архивариус", "refinedstorage:64k_storage_disk", 0, 3,
          text=["Четыре диска на 64k."],
          tasks=[give("refinedstorage:64k_storage_disk", 4)],
          rewards=loot(("refinedstorage:64k_storage_part", 8), ("refinedstorage:wireless_grid", 1), xp=250,
                       text="Восемь частей — это два новых диска; беспроводной грид в придачу")),

        Q("levitite", "Легче воздуха", "aeronautics:levitite", 1, 3,
          text=["Шестьдесят четыре левитита."],
          tasks=[give("aeronautics:levitite", 64)],
          rewards=loot(("aeronautics:pearlescent_levitite", 16), ("aeronautics:smart_propeller", 4), xp=300)),

        Q("truadamantite", "Истинная сила", "eternal_tales:truadamantite_ingot", 0, 4,
          text=["Шестнадцать труадамантита из Королевства Янтаря."],
          tasks=[give("eternal_tales:truadamantite_ingot", 16)],
          rewards=loot(("eternal_tales:truadamantite_brush", 1), ("eternal_tales:crystal_of_greatness", 1), xp=500)),
    ]),
)

chapter(
    "trials_bosses", "trials", 40, "Испытания: трофеи", "minecraft:dragon_head",
    "Победы над боссами, которые книга умеет заметить",
    [
        "Здесь ничего сдавать не нужно: книга сама увидит достижение и выдаст "
        "награду. Зато наград здесь больше всего.",
    ],
    [
        Q("dragon", "Драконоборец", "minecraft:dragon_egg", 0, 0,
          tasks=[adv("minecraft:end/kill_dragon")],
          rewards=loot(("minecraft:shulker_shell", 8), ("minecraft:ender_pearl", 32), xp=400)),
        Q("wither", "Иссушитель", "minecraft:wither_skeleton_skull", 1, 0,
          tasks=[adv("minecraft:nether/summon_wither")],
          rewards=loot(("minecraft:netherite_scrap", 8), xp=400)),
        Q("naga", "Чешуя Наги", "twilightforest:naga_trophy", 0, 1,
          tasks=[adv("twilightforest:progress_naga")],
          rewards=loot(("twilightforest:naga_scale", 12), xp=150)),
        Q("lich", "Прах Лича", "twilightforest:lich_trophy", 1, 1,
          tasks=[adv("twilightforest:progress_lich")],
          rewards=loot(("twilightforest:transformation_powder", 8), xp=200)),
        Q("hydra", "Голова Гидры", "twilightforest:hydra_trophy", 2, 1,
          tasks=[adv("twilightforest:progress_hydra")],
          rewards=loot(("twilightforest:fiery_ingot", 8), xp=300)),
        Q("terrible_tree", "Кометный лесоруб", "eternal_tales:comet_banner", 0, 2,
          tasks=[adv("eternal_tales:kill_terrible_tree")],
          rewards=loot(("eternal_tales:aerolite_ingot", 8), xp=200)),
        Q("nyetet", "Павший титан", "eternal_tales:purgatory_banner", 1, 2,
          tasks=[adv("eternal_tales:kill_nyetet")],
          rewards=loot(("eternal_tales:lapsidian_ingot", 16), xp=300)),
        Q("pterion", "Крылатый ужас", "eternal_tales:rayana_banner", 2, 2,
          tasks=[adv("eternal_tales:kill_pterion")],
          rewards=loot(("eternal_tales:sunhog_leather", 8), xp=300)),
        Q("xaxxas", "Падение короля", "eternal_tales:royal_banner", 0, 3,
          tasks=[adv("eternal_tales:kill_xaxxas_xix")],
          rewards=loot(("eternal_tales:pharos", 1), xp=600)),
        Q("unahzaal", "Конец пути", "eternal_tales:unahzaal_bricks_dimension", 1, 3,
          tasks=[adv("eternal_tales:kill_unahzaal")],
          rewards=loot(("minecraft:nether_star", 4), xp=2000)),
        Q("raid", "Оборона колонии", "minecolonies:chiefsword", 2, 3,
          tasks=[adv("minecolonies:military/army_8")],
          rewards=loot(("minecraft:diamond", 8), xp=200)),
    ],
)
