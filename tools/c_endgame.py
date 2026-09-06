# -*- coding: utf-8 -*-
"""Эндгейм: монументальные цели, на которые уходят десятки часов после «финала»."""
from dsl import chapter, Q, item, give, adv, dim, loot

E = "eternal_tales:"

chapter(
    "end_monuments", "endgame", 10, "Монументы", "minecraft:beacon",
    "Постройки, которые оправдывают весь завод",
    [
        "Финал сборки — не бой и не предмет. Финал — то, что остаётся стоять, когда вы "
        "выходите из игры. Каждое задание здесь требует продукции в таких количествах, "
        "что сделать её руками нельзя в принципе. Только фабрика. Только автоматика.",
        "Сдаёте — получаете. И получаете то, что ускорит следующий монумент.",
    ],
    [
        Q("spire", "Шпиль", "create:metal_girder", 0, 0,
          text=["Тысяча двадцать четыре металлические балки Create. Башня из них "
                "видна из соседнего чанка, если Distant Horizons не врёт."],
          tasks=[give("create:metal_girder", 1024)],
          rewards=loot(("create:brass_casing", 64), ("create:sturdy_sheet", 64), xp=1200)),
        Q("bridge", "Мост через мир", "create:track", 1, 0,
          text=["Две тысячи сорок восемь рельсов. Ветка от базы до колонии, от колонии "
                "до шахты, от шахты до пристани дирижаблей. Поезд, идущий по кольцу "
                "полчаса."],
          tasks=[give("create:track", 2048)],
          rewards=loot(("create:railway_casing", 32), ("railways:track_coupler", 8), xp=1500)),
        Q("vault_city", "Хранилище на миллион", "refinedstorage:64k_storage_disk", 2, 0,
          text=["Шестнадцать дисков на шестьдесят четыре тысячи. Миллион слотов. "
                "Сеть, которой хватит на всё, что вы когда-либо добудете."],
          tasks=[give("refinedstorage:64k_storage_disk", 16)],
          rewards=loot(("refinedstorage:64k_storage_part", 64), xp=1500)),
        Q("matrix", "Матрица", "mekanism:induction_casing", 0, 1,
          text=["Пятьдесят четыре корпуса и восемь предельных индукционных ячеек. "
                "Батарея, которая переживёт термоядерный реактор."],
          tasks=[give("mekanism:induction_casing", 54), give("mekanism:ultimate_induction_cell", 8)],
          rewards=loot(("mekanism:ultimate_induction_provider", 4), ("mekanism:pellet_antimatter", 4), xp=2000)),
        Q("shipyard", "Верфь", "aeronautics:pearlescent_levitite", 1, 1,
          text=["Двести пятьдесят шесть перламутрового левитита и шестьдесят четыре умных "
                "пропеллера. Столько нужно, чтобы поднять в воздух что-то размером "
                "с колонию."],
          tasks=[give("aeronautics:pearlescent_levitite", 256), give("aeronautics:smart_propeller", 64)],
          rewards=loot(("simulated:navigation_table", 4), ("simulated:gyroscopic_mechanism", 32), xp=2500)),
        Q("fortress", "Бастион", "createbigcannons:nethersteel_screw_breech", 2, 1,
          text=["Восемь незеритовых винтовых затворов и сто двадцать восемь фугасных "
                "снарядов. Крепость, которую не берут."],
          tasks=[give("createbigcannons:nethersteel_screw_breech", 8), give("createbigcannons:he_shell", 128)],
          rewards=loot(("createbigcannons:nethersteel_ingot", 64), ("create_radar:fire_controller", 4), xp=2500)),
        Q("cathedral", "Собор", "domum_ornamentum:architectscutter", 0, 2, deps=["spire"],
          text=["Две тысячи блоков через резак архитектора — любых, но не ванильных. "
                "Домум Орнаментум делает их из чего угодно; вопрос только в терпении. "
                "Книга примет фахверк: тысяча двадцать четыре панели."],
          tasks=[give("domum_ornamentum:dynamic_timberframe", 1024)],
          rewards=loot(("minecraft:emerald_block", 16), xp=1500)),
        Q("eternal_town", "Вечный город заново", E + "the_ultimate_bricks", 1, 2, deps=["vault_city"],
          text=["Пятьсот двенадцать Предельных кирпичей. Отстройте Вечный город из "
                "материала, который делают только Аркемеры."],
          tasks=[give(E + "the_ultimate_bricks", 512)],
          rewards=loot((E + "crystal_of_greatness", 4), (E + "restored_astral", 1), xp=3000)),
    ],
)

chapter(
    "end_marathon", "endgame", 20, "Марафон", "minecraft:clock",
    "Числа, за которыми не угнаться без цепочки автокрафта",
    [
        "Здесь нет боссов и нет построек — только объём. Каждое задание сдаётся "
        "одним нажатием, но собрать его можно только сетью, которая делает вещи сама. "
        "Это проверка автокрафта, замаскированная под жадность.",
    ],
    [
        Q("mech1024", "Тысяча механизмов", "create:precision_mechanism", 0, 0,
          text=["Тысяча двадцать четыре прецизионных механизма. Одна линия крафтеров даёт "
                "один в несколько секунд; считайте сами, сколько линий вам нужно."],
          tasks=[give("create:precision_mechanism", 1024)],
          rewards=loot(("create:rotation_speed_controller", 32), ("create:mechanical_crafter", 64), xp=3000)),
        Q("steel4096", "Четыре тысячи стали", "immersiveengineering:ingot_steel", 1, 0,
          text=["Четыре тысячи девяносто шесть слитков стали IE. Дуговая печь на "
                "дизельной сети — единственный реалистичный путь."],
          tasks=[give("immersiveengineering:ingot_steel", 4096)],
          rewards=loot(("immersiveengineering:graphite_electrode", 16), ("immersiveengineering:capacitor_hv", 4), xp=3000)),
        Q("circuits256", "Двести пятьдесят шесть предельных", "mekanism:ultimate_control_circuit", 2, 0,
          text=["Атомный сплав в промышленных объёмах. Без пятикратной руды и "
                "автокрафта на глубину в двадцать рецептов это невозможно."],
          tasks=[give("mekanism:ultimate_control_circuit", 256)],
          rewards=loot(("mekanism:alloy_atomic", 128), ("mekanism:qio_drive_supermassive", 1), xp=4000)),
        Q("antimatter64", "Антивещество", "mekanism:pellet_antimatter", 0, 1, deps=["circuits256"],
          text=["Шестьдесят четыре гранулы антивещества. SPS, работающий неделю на "
                "термоядерном реакторе. Это уже не игра, это физика."],
          tasks=[give("mekanism:pellet_antimatter", 64)],
          rewards=loot(("mekanism:antiprotonic_nucleosynthesizer", 1), ("mekanism:mekasuit_bodyarmor", 1), xp=6000)),
        Q("processors1024", "Тысяча процессоров", "refinedstorage:advanced_processor", 1, 1, deps=["mech1024"],
          text=["Тысяча двадцать четыре продвинутых процессора. Сеть, которая делает "
                "сама себя."],
          tasks=[give("refinedstorage:advanced_processor", 1024)],
          rewards=loot(("refinedstorage:64k_storage_disk", 8), ("refinedstorage:autocrafter", 16), xp=3000)),
        Q("crystals9", "Девять миров в кармане", E + "unahzaal_multiverse", 2, 1, deps=["steel4096"],
          text=["По одному кристаллу каждого измерения Eternal Tales — все девять, "
                "сданные разом. Это значит, что вы можете вернуться куда угодно "
                "в любой момент. А значит, можете и отдать."],
          tasks=[give(E + "comets"), give(E + "purgatorium"), give(E + "gardens_of_eden"), give(E + "rayana"),
                 give(E + "lands_of_karvat"), give(E + "volcanech"), give(E + "kingdom_of_amber"),
                 give(E + "unahzaal_multiverse"), give(E + "ultimate_world")],
          rewards=loot((E + "return_ticket", 16), (E + "the_ultimate_bricks", 64), xp=5000)),
    ],
)

chapter(
    "end_apotheosis", "endgame", 30, "Апофеоз", "minecraft:nether_star",
    "Последние задания книги",
    [
        "Три вещи, которые сделать труднее всего, и одна, которую нельзя сделать, "
        "не сделав всё остальное.",
    ],
    [
        Q("darkness_unahzaal", "Тьма побеждена", E + "calamity_ring", 0, 0,
          text=["Унахзаал в режиме Вечной Тьмы. Кольцо Бедствия — доказательство."],
          tasks=[adv(E + "kill_unahzaal_with_hard_mode"), adv(E + "kill_noxifer"), adv(E + "kill_luciden")],
          rewards=loot(("minecraft:nether_star", 8), (E + "totem_of_death", 1), xp=8000)),
        Q("arkemer", "Наследие Аркемеров", E + "stabilized_miniature_black_hole", 1, 0,
          text=["Стабилизированная чёрная дыра, Порядок Вселенной, Первая Призма, обе "
                "Предельные вещи. Всё, что оставила цивилизация, которая умела больше нас."],
          tasks=[adv(E + "get_stabilized_miniature_black_hole"), adv(E + "learn_order_of_the_universe"),
                 adv(E + "get_the_first_prism"), adv(E + "get_the_ultimate_two")],
          rewards=loot((E + "hammer_of_eternity", 1), xp=8000)),
        Q("seven", "Семь вершин", "minecraft:enchanted_golden_apple", 2, 0,
          text=["Фабричный указатель, экскаватор, антивещество, миллионное хранилище, "
                "колония пятого уровня, Светоч углей, Ultimate World. Не сдавать — показать."],
          tasks=[item("create:factory_gauge", 4), item("immersiveengineering:excavator"), item("mekanism:pellet_antimatter", 8),
                 item("refinedstorage:64k_storage_disk", 16), adv("minecolonies:minecolonies/build_town_hall_5"),
                 item("twilightforest:lamp_of_cinders"), dim(E + "ultimate_world")],
          rewards=loot(("minecraft:enchanted_golden_apple", 16), ("minecraft:netherite_block", 4), xp=10000)),
        Q("codex", "Кодекс закрыт", "minecraft:writable_book", 1, 1, deps=["darkness_unahzaal", "arkemer", "seven"],
          shape="big",
          text=["Три предыдущих узла — и один звёздный осколок в руках. Больше книге "
                "нечего вам сказать. Спасибо, что дочитали.",
                "Дальше — то, что не предусмотрел ни один мод и что возможно из их деталей. "
                "Это уже ваша книга."],
          tasks=[give("minecraft:nether_star", 1)],
          rewards=loot(("minecraft:dragon_egg", 1), ("minecraft:elytra", 1), ("minecraft:nether_star", 16), xp=20000,
                       text="Полное прохождение сборки")),
    ],
)
