# -*- coding: utf-8 -*-
"""Сюжетные линии: сквозные цепочки через несколько модов с ветвлениями."""
from dsl import chapter, Q, item, give, adv, dim, check, loot, ponder

E = "eternal_tales:"

chapter(
    "story_forge", "story", 10, "Путь механика", "create:mechanical_press",
    "От первого сплава до поезда, который сам возит руду",
    [
        "Есть простой способ понять, чего стоит ваш завод: перестать к нему подходить. "
        "Эта линия ведёт от руки на рукоятке привода к составу, который уходит на шахту "
        "по расписанию и возвращается с рудой, пока вы спите.",
        "Развилки на пути настоящие: можно пройти через ветер или через воду, через "
        "жёрнов или через колёса. Сходятся они на одном — на поезде.",
    ],
    [
        Q("hand", "Рука на рукоятке", "create:hand_crank", 0, 0,
          text=["Первый оборот вала — всегда ваш. Пресс на ручном приводе, десять листов "
                "железа, руки в мозолях. Запомните это чувство: скоро его заменит вода."],
          tasks=[item("create:hand_crank"), item("create:mechanical_press"), item("create:iron_sheet", 10)],
          rewards=loot(("create:andesite_alloy", 12), xp=30)),
        Q("wind", "Дорога ветра", "create:windmill_bearing", -1, 1, deps=["hand"],
          text=["Подшипник, шестьдесят четыре парусных рамы, высокая точка. Ветряк не "
                "требует ничего, кроме неба, и за это ему прощают медлительность."],
          tasks=[item("create:windmill_bearing"), item("create:sail_frame", 64)],
          rewards=loot(("create:white_sail", 32), xp=50)),
        Q("water", "Дорога воды", "create:large_water_wheel", 1, 1, deps=["hand"],
          text=["Два больших колеса в замкнутой канавке. Тише ветряка, надёжнее и "
                "не зависят от погоды. Классика."],
          tasks=[item("create:large_water_wheel", 2)],
          rewards=loot(("create:cogwheel", 16), ("create:large_cogwheel", 8), xp=50)),
        Q("source", "Источник найден", "create:stressometer", -1, 2, deps=["wind"],
          text=["Любой из двух путей приводит сюда: к стрессометру, стрелка которого "
                "впервые не в красном. Теперь можно ставить машины, а не игрушки."],
          tasks=[item("create:stressometer")],
          rewards=loot(("create:wrench", 1), xp=40)),
        Q("source_w", "Источник найден", "create:stressometer", 1, 2, deps=["water"],
          text=["Двойник узла выше: развилка сходится. Книга засчитает тот путь, "
                "по которому вы пришли."],
          tasks=[item("create:stressometer")],
          rewards=loot(xp=10)),
        Q("mill", "Жёрнов или колёса", "create:millstone", -1, 3, deps=["source", "source_w"],
          text=["Быстрый путь — жёрнов, дешёвый и медленный. Он даст первые сто "
                "дроблёных кусков и покажет, что руда умеет удваиваться."],
          tasks=[give("create:crushed_raw_iron", 64)],
          rewards=loot(("minecraft:iron_ingot", 96), xp=60)),
        Q("wheels", "Жёрнов или колёса", "create:crushing_wheel", 1, 3, deps=["source", "source_w"],
          text=["Длинный путь — латунь, дробильные колёса, поток. Он дороже на входе "
                "и в пять раз быстрее на выходе. Сдайте сто двадцать восемь дроблёного "
                "железа с колёс — и книга поверит, что линия работает."],
          tasks=[item("create:crushing_wheel", 2), give("create:crushed_raw_iron", 128)],
          rewards=loot(("create:brass_ingot", 32), ("minecraft:iron_ingot", 192), xp=120)),
        Q("smelt", "Плавильный ряд", "create:encased_fan", 0, 4, deps=["mill", "wheels"],
          text=["Вентилятор над лавой, лента под ним, сундук в конце. Дроблёное входит, "
                "слитки выходят. Первое место на базе, где ничего не надо делать руками."],
          tasks=[item("create:encased_fan", 2), item("create:belt", 16), ponder("create:encased_fan")],
          rewards=loot(("create:andesite_funnel", 8), ("create:chute", 8), xp=80)),
        Q("boiler", "Котёл на восемнадцать", "create:steam_engine", 0, 5, deps=["smelt"],
          text=["Бак, четыре горелки, четыре двигателя. Уровень котла растёт с объёмом "
                "и жаром; ваш первый котёл будет второго уровня, и этого хватит, чтобы "
                "остановить ветряк навсегда."],
          tasks=[item("create:steam_engine", 4), item("create:fluid_tank", 16), item("create:blaze_burner", 4)],
          rewards=loot(("create:copper_casing", 16), xp=120)),
        Q("precision", "Линия точности", "create:precision_mechanism", -1, 6, deps=["boiler"],
          text=["Пять крафтеров кольцом, деплойеры с золотым листом, стержнями и "
                "шестернями, лента по кругу. Сдайте восемь механизмов, собранных без рук."],
          tasks=[give("create:precision_mechanism", 8)],
          rewards=loot(("create:precision_mechanism", 12), ("create:mechanical_arm", 1), xp=150)),
        Q("rails", "Первая ветка", "create:track", 1, 6, deps=["boiler"],
          text=["Шестьдесят четыре рельса от базы до шахты. Не по прямой — Create умеет "
                "красивые кривые, и первые пути кладут дольше, чем нужно, просто потому "
                "что нравится смотреть."],
          tasks=[item("create:track", 64), item("create:track_station", 2)],
          rewards=loot(("create:track", 64), ("create:track_signal", 4), xp=100)),
        Q("train", "Поезд, который не ждёт", "create:schedule", 0, 7, deps=["precision", "rails"],
          text=["Локомотив с котлом, вагон с переносными интерфейсами, расписание: "
                "«на шахту, ждать полного, домой, ждать пустого, повторить». Кондуктор в "
                "фуражке. Отойдите и посмотрите, как он уезжает."],
          tasks=[item("create:controls"), item("create:schedule"), item("railways:conductor_cap"),
                 item("create:portable_storage_interface", 2)],
          rewards=loot(("create:railway_casing", 8), ("create:large_bogey", 2), xp=250,
                       text="Первое достижение, которое движется само")),
    ],
)

chapter(
    "story_current", "story", 20, "Ток", "immersiveengineering:wirecoil_steel",
    "Три завода — одна энергосеть",
    [
        "Три технологии сборки долго живут отдельно: Create крутит валы, IE тянет "
        "провода, Mekanism молчит и обогащает. Эта линия — про то, как заставить их "
        "говорить друг с другом, и заканчивается она реактором, который питает всё.",
    ],
    [
        Q("coke", "Дым над коксовой", "immersiveengineering:coke_oven", 0, 0,
          text=["Первый шаг IE — всегда кокс. Сдайте шестьдесят четыре — книге нужно "
                "знать, что печь дышит, а не просто стоит."],
          tasks=[give("immersiveengineering:coal_coke", 64)],
          rewards=loot(("immersiveengineering:blastbrick", 27), xp=60)),
        Q("steel", "Сталь двух домов", "immersiveengineering:ingot_steel", 0, 1, deps=["coke"],
          text=["В сборке две стали, и они не взаимозаменяемы. Доменная печь IE и инфузер "
                "Mekanism — соберите обе. Этот узел — первая точка, где два мода "
                "стоят на одной площадке."],
          tasks=[give("immersiveengineering:ingot_steel", 32), give("mekanism:ingot_steel", 32)],
          rewards=loot(("mekanism:steel_casing", 4), ("immersiveengineering:component_steel", 16), xp=120)),
        Q("dynamo", "Первый ток", "immersiveengineering:dynamo", -1, 2, deps=["steel"],
          text=["Водяное колесо IE на динамо, медный провод к конденсатору. Мало, "
                "зато уже энергия — та самая, которую понимает Mekanism."],
          tasks=[item("immersiveengineering:dynamo"), item("immersiveengineering:capacitor_lv"),
                 item("immersiveengineering:connector_lv", 4)],
          rewards=loot(("immersiveengineering:wirecoil_copper", 8), xp=60)),
        Q("alternator", "Вал в провод", "createaddition:alternator", 1, 2, deps=["steel"],
          text=["Генератор Create Addition на паровом котле. Вращение уходит в провод, "
                "провод — в конденсатор IE. Первое рукопожатие Create и IE."],
          tasks=[item("createaddition:alternator", 2), item("createaddition:rolling_mill")],
          rewards=loot(("createaddition:connector", 8), ("createaddition:copper_spool", 8), xp=100)),
        Q("grid", "Единая сеть", "immersiveengineering:transformer", 0, 3, deps=["dynamo", "alternator"],
          text=["Трансформатор поднимает напряжение, стальной провод несёт его через "
                "двор, энергокуб Mekanism принимает. Один счётчик на три мода."],
          tasks=[item("immersiveengineering:transformer"), item("immersiveengineering:wirecoil_steel", 4),
                 item("mekanism:basic_energy_cube")],
          rewards=loot(("immersiveengineering:capacitor_mv", 1), xp=150)),
        Q("ore5", "Пятикратная руда", "mekanism:chemical_crystallizer", -1, 4, deps=["grid"],
          text=["Сеть есть — теперь ей есть что кормить. Полная цепочка Mekanism: "
                "растворение, промывка, кристаллизация. Сдайте шестьдесят четыре "
                "кристалла железа — доказательство того, что установка живёт."],
          tasks=[item("mekanism:chemical_dissolution_chamber"), item("mekanism:chemical_crystallizer"),
                 give("mekanism:crystal_iron", 64)],
          rewards=loot(("mekanism:ingot_osmium", 64), ("mekanism:alloy_reinforced", 8), xp=250)),
        Q("diesel", "Дизель", "immersiveengineering:diesel_generator", 1, 4, deps=["grid"],
          text=["Клош выращивает, выжималка и ферментёр перерабатывают, завод смешивает, "
                "генератор ревёт. Сдайте шестнадцать вёдер биодизеля — сеть должна "
                "переживать ночь."],
          tasks=[item("immersiveengineering:diesel_generator"), give("immersiveengineering:biodiesel_bucket", 16)],
          rewards=loot(("immersiveengineering:capacitor_hv", 1), xp=250)),
        Q("fission", "Сердце базы", "mekanismgenerators:fission_reactor_casing", 0, 5, deps=["ore5", "diesel"],
          text=["Реактор деления, котёл, турбина, матрица. Три мода, один провод, "
                "гигаватт. Сдайте четыре топливные сборки — те, что у вас есть в запасе, "
                "а не те, что в реакторе."],
          tasks=[item("mekanismgenerators:fission_reactor_logic_adapter"), item("mekanismgenerators:turbine_rotor", 4),
                 give("mekanismgenerators:fission_fuel_assembly", 4)],
          rewards=loot(("mekanism:elite_control_circuit", 8), ("mekanismgenerators:turbine_blade", 16), xp=600,
                       text="Энергия, которую больше не считают")),
    ],
)

chapter(
    "story_expedition", "story", 30, "Экспедиция", "twilightforest:magic_map_focus",
    "Через все миры, в том порядке, в каком они открываются",
    [
        "Сборка ведёт вас по чужим мирам не случайно, а по порядку: сначала небо, "
        "потом сумерки, потом кометы — и дальше по спирали, которую выстроила война "
        "Вулканеха. Эта линия — маршрут, и у неё есть только один пункт назначения.",
    ],
    [
        Q("kit", "Снаряжение", "waystones:return_scroll", 0, 0,
          text=["Путевой камень у дома, два свитка возврата, оберег жизни из Сумеречного "
                "леса — нет, его ещё нет. Пока: камень, свитки, спальный мешок и обещание "
                "себе не забывать координаты."],
          tasks=[item("waystones:waystone"), item("waystones:return_scroll", 2), item("comforts:sleeping_bag_red")],
          rewards=loot(("waystones:warp_dust", 8), xp=40)),
        Q("sky", "Небо", "aether:aether_portal_frame", -1, 1, deps=["kit"],
          text=["Aether первым: он мягче остальных и учит главному — смотреть под ноги. "
                "Бронзовое подземелье, ключ, медаль."],
          tasks=[dim("aether:the_aether"), item("aether:bronze_dungeon_key")],
          rewards=loot(("aether:ambrosium_shard", 32), ("aether:skyroot_bucket", 1), xp=120)),
        Q("dusk", "Сумерки", "twilightforest:naga_trophy", 1, 1, deps=["kit"],
          text=["Twilight Forest вторым: он строгий, но справедливый. Нага во дворе, "
                "Лич в башне. После них лес открывается."],
          tasks=[dim("twilightforest:twilight_forest"), item("twilightforest:naga_trophy"), item("twilightforest:lich_trophy")],
          rewards=loot(("twilightforest:charm_of_life_1", 2), ("twilightforest:charm_of_keeping_1", 1), xp=200)),
        Q("comets", "Кометы", E + "comets", 0, 2, deps=["sky", "dusk"],
          text=["Второй уровень колдовства, пять компонентов, кристалл. Розовое небо "
                "и дерево, которое ответит на удар топора."],
          tasks=[dim(E + "comets"), adv(E + "kill_terrible_tree")],
          rewards=loot((E + "return_ticket", 2), (E + "skylite_ingot", 8), xp=200)),
        Q("purg", "Чистилище", E + "purgatorium", 0, 3, deps=["comets"],
          text=["Адский камень с алтаря, Рок-Блейз, три части руны, Ниетет. Здесь темно, "
                "и здесь ссыльные рассказывают, за что."],
          tasks=[dim(E + "purgatorium"), adv(E + "kill_nyetet")],
          rewards=loot((E + "sun_stone_nugget", 4), (E + "lapsidian_ingot", 16), xp=300)),
        Q("eden", "Эдем", E + "gardens_of_eden", 0, 4, deps=["purg"],
          text=["Солнечный камень открывает портал в Крае. Санфурри нальют Напиток "
                "Солнца, если вы заслужили."],
          tasks=[dim(E + "gardens_of_eden"), adv(E + "eden_quest")],
          rewards=loot((E + "aragotium_ingot", 8), xp=300)),
        Q("rayana", "Раяна", E + "rayana", -1, 5, deps=["eden"],
          text=["Джунгли и вампиры. Кровавый глаз на алтарь Аэде — Птерион."],
          tasks=[dim(E + "rayana"), adv(E + "kill_pterion")],
          rewards=loot((E + "destroyer_eye", 2), xp=350)),
        Q("karvat", "Карват", E + "lands_of_karvat", 1, 5, deps=["eden"],
          text=["Боги на алтарях. Хотя бы трое из пяти."],
          tasks=[dim(E + "lands_of_karvat"), adv(E + "kill_enicrih"), adv(E + "kill_arla"), adv(E + "kill_ikkorh")],
          rewards=loot((E + "spore_edennus", 8), (E + "crimson_eel", 8), xp=350)),
        Q("volcanech", "Вулканех", E + "volcanech", 0, 6, deps=["rayana", "karvat"],
          text=["Мир-агрессор. Голем, серный тротил, дезертиры, Арахулум."],
          tasks=[dim(E + "volcanech"), adv(E + "kill_arahulum")],
          rewards=loot((E + "truadamantite_ingot", 4), (E + "flame_sphere", 1), xp=450)),
        Q("amber", "Янтарь", E + "kingdom_of_amber", 0, 7, deps=["volcanech"],
          text=["Тринадцатый уровень колдовства. Лабиринт, тайна, Ксакксас."],
          tasks=[dim(E + "kingdom_of_amber"), adv(E + "kill_xaxxas_xix")],
          rewards=loot((E + "damaged_astral", 1), (E + "pharos", 1), xp=700)),
        Q("unahzaal", "Конец пути", E + "unahzaal_multiverse", 0, 8, deps=["amber"],
          text=["Все кристаллы в один. Шестнадцатый уровень. Мультивселенная и тот, "
                "кто её держит."],
          tasks=[dim(E + "unahzaal_multiverse"), adv(E + "kill_unahzaal")],
          rewards=loot((E + "the_ultimate_bricks", 32), ("minecraft:nether_star", 2), xp=1500,
                       text="Экспедиция окончена. Начинается другая игра")),
    ],
)

chapter(
    "story_colony", "story", 40, "Город, который растёт сам", "minecolonies:blockhuttownhall",
    "Колония от четырёх жителей до технополиса",
    [
        "MineColonies — единственный мод сборки, в котором прогресс идёт, пока вас "
        "нет. Эта линия про то, как из ящика снабжения вырастает город, который "
        "снабжает вашу фабрику, а фабрика — его.",
    ],
    [
        Q("found", "Четверо", "minecolonies:supplychestdeployer", 0, 0,
          text=["Ящик, ратуша, строитель, первый дом. Четыре жителя, у которых пока "
                "нет ничего, кроме вас."],
          tasks=[item("minecolonies:blockhuttownhall"), item("minecolonies:blockhutbuilder"), item("minecolonies:blockhutcitizen")],
          rewards=loot(("minecraft:oak_log", 64), ("minecraft:cobblestone", 128), xp=60)),
        Q("supply", "Склад и хлеб", "minecolonies:blockhutwarehouse", 0, 1, deps=["found"],
          text=["Склад, курьер, фермер, повар. Сдайте шестьдесят четыре хлеба — колония "
                "должна есть, пока вы строите."],
          tasks=[item("minecolonies:blockhutwarehouse"), item("minecolonies:blockhutdeliveryman"),
                 item("minecolonies:blockhutcook"), give("minecraft:bread", 64)],
          rewards=loot(("minecolonies:blockminecoloniesrack", 16), xp=100)),
        Q("wood", "Лес и камень", "minecolonies:blockhutlumberjack", -1, 2, deps=["supply"],
          text=["Лесоруб, лесопилка, шахтёр, каменотёс. Отсюда колония берёт всё, "
                "что строит."],
          tasks=[item("minecolonies:blockhutlumberjack"), item("minecolonies:blockhutsawmill"),
                 item("minecolonies:blockhutminer"), item("minecolonies:blockhutstonemason")],
          rewards=loot(("minecraft:iron_ingot", 32), xp=120)),
        Q("guard", "Первая ночь под охраной", "minecolonies:blockhutguardtower", 1, 2, deps=["supply"],
          text=["Две башни и знамя сбора. Набег придёт раньше, чем вы думаете."],
          tasks=[item("minecolonies:blockhutguardtower", 2), item("minecolonies:banner_rally_guards")],
          rewards=loot(("minecraft:iron_sword", 2), ("minecraft:bow", 2), ("minecraft:arrow", 64), xp=100)),
        Q("population", "Двадцать пять", "minecolonies:blockhuttavern", 0, 3, deps=["wood", "guard"],
          text=["Таверна, ещё дома, больница. Двадцать пять жителей — это уже город "
                "с характером."],
          tasks=[adv("minecolonies:minecolonies/colony_population_25"), item("minecolonies:blockhuthospital")],
          rewards=loot(("minecraft:emerald", 16), xp=200)),
        Q("science", "Университет", "minecolonies:blockhutuniversity", -1, 4, deps=["population"],
          text=["Библиотека, школа, университет. Первое исследование запущено."],
          tasks=[item("minecolonies:blockhutlibrary"), item("minecolonies:blockhutschool"), item("minecolonies:blockhutuniversity")],
          rewards=loot(("minecolonies:ancienttome", 2), ("minecraft:book", 32), xp=200)),
        Q("industry", "Кузница и механик", "minecolonies:blockhutmechanic", 1, 4, deps=["population"],
          text=["Плавильня, кузнец, механик. Механик умеет делать детали Create и IE — "
                "научите его, и колония начнёт снабжать завод."],
          tasks=[item("minecolonies:blockhutsmeltery"), item("minecolonies:blockhutblacksmith"), item("minecolonies:blockhutmechanic")],
          rewards=loot(("create:andesite_alloy", 64), xp=200)),
        Q("network", "Склад в сети", "refinedstorage:external_storage", 0, 5, deps=["science", "industry"],
          text=["Внешнее хранилище Refined Storage на стойки склада. Теперь всё, что "
                "приносит колония, видно в гриде — и наоборот."],
          tasks=[item("refinedstorage:external_storage", 2), item("refinedstorage:grid")],
          rewards=loot(("refinedstorage:4k_storage_disk", 2), xp=250)),
        Q("garrison", "Гарнизон", "minecolonies:blockhutbarracks", -1, 6, deps=["network"],
          text=["Казармы с четырьмя башнями, академия, стрельбище. Восемь стражей "
                "по достижению — и ночь больше не страшна."],
          tasks=[item("minecolonies:blockhutbarracks"), adv("minecolonies:military/army_8")],
          rewards=loot(("minecraft:diamond", 8), xp=300)),
        Q("fifty", "Пятьдесят", "minecolonies:blockhutmysticalsite", 1, 6, deps=["network"],
          text=["Пятьдесят жителей, ратуша пятого уровня в планах, мистическое место "
                "для счастья. Город."],
          tasks=[adv("minecolonies:minecolonies/colony_population_50"), item("minecolonies:blockhutmysticalsite")],
          rewards=loot(("minecraft:emerald_block", 4), xp=400)),
        Q("technopolis", "Технополис", "minecolonies:blockhuttownhall", 0, 7, deps=["garrison", "fifty"],
          text=["Ратуша пятого уровня. Колония, которая кормит завод и защищает себя. "
                "Сдайте восемь предельных схем Mekanism, сделанных руками механика или "
                "вашими — не важно; важно, что обе стороны дошли до конца."],
          tasks=[adv("minecolonies:minecolonies/build_town_hall_5"), give("mekanism:ultimate_control_circuit", 8)],
          rewards=loot(("mekanism:ultimate_control_circuit", 16), ("minecraft:netherite_ingot", 4), xp=800)),
    ],
)

chapter(
    "story_sky", "story", 50, "Небо и порох", "aeronautics:white_envelope",
    "Воздушный флот, артиллерия и радар — одна оборона",
    [
        "Дирижабль без пушки — прогулка. Пушка без радара — салют. Эта линия собирает "
        "три мода в одну систему: летающая платформа, наведение, залп.",
    ],
    [
        Q("lift", "Подъём", "simulated:physics_assembler", 0, 0,
          text=["Сборщик, левитит, оболочка, горелка. Первый дирижабль — деревянная "
                "коробка, которая всё-таки летит."],
          tasks=[item("simulated:physics_assembler"), give("aeronautics:levitite", 16), item("aeronautics:white_envelope", 16)],
          rewards=loot(("aeronautics:levitite", 32), ("aeronautics:adjustable_burner", 2), xp=150)),
        Q("cast", "Литьё", "createbigcannons:cannon_cast", -1, 1, deps=["lift"],
          text=["Чугун, песок, формы, сверло. Сдайте четыре рассверленных чугунных "
                "ствола — с ними уже можно стрелять."],
          tasks=[give("createbigcannons:cast_iron_cannon_barrel", 4)],
          rewards=loot(("createbigcannons:bronze_ingot", 16), ("createbigcannons:powder_charge", 16), xp=150)),
        Q("eyes", "Глаза", "create_radar:plane_radar", 1, 1, deps=["lift"],
          text=["Радар, пластины, линия данных, монитор. Первый раз, когда вы видите "
                "цель раньше, чем она вас."],
          tasks=[item("create_radar:plane_radar"), item("create_radar:data_link", 2), item("create_radar:monitor")],
          rewards=loot(("create_radar:radar_plate_block", 16), xp=150)),
        Q("mount", "Наводка", "create_radar:auto_yaw_controller", 0, 2, deps=["cast", "eyes"],
          text=["Лафет, контроллеры курса и тангажа, контроллер огня. Радар говорит — "
                "пушка поворачивается. Никакой руки."],
          tasks=[item("createbigcannons:cannon_mount"), item("create_radar:auto_yaw_controller"),
                 item("create_radar:auto_pitch_controller"), item("create_radar:fire_controller")],
          rewards=loot(("createbigcannons:steel_ingot", 32), xp=250)),
        Q("flak", "Зенитка", "createbigcannons:flak_autocannon_round", -1, 3, deps=["mount"],
          text=["Автопушка со стальным стволом и зенитными патронами. Сдайте шестьдесят "
                "четыре — против воздушных целей меньше не берут."],
          tasks=[item("createbigcannons:steel_autocannon_barrel"), give("createbigcannons:flak_autocannon_round", 64)],
          rewards=loot(("createbigcannons:autocannon_ammo_container", 2), xp=300)),
        Q("missile", "Ракета", "cbcaeronauticsmissiles:guidance_computer", 1, 3, deps=["mount"],
          text=["Двигатель, рули, вычислитель, неконтактный взрыватель, пусковая. "
                "Ракета — физический объект, и летит по-настоящему."],
          tasks=[item("cbcaeronauticsmissiles:rocket_motor", 2), item("cbcaeronauticsmissiles:actuator_fins", 4),
                 item("cbcaeronauticsmissiles:guidance_computer"), item("cbcaeronauticsmissiles:missile_mount")],
          rewards=loot(("cbcaeronauticsmissiles:rocket_motor", 8), ("cbcaeronauticsmissiles:aircraft_proximity_fuze", 4), xp=300)),
        Q("fleet", "Флагман", "simulated:navigation_table", 0, 4, deps=["flak", "missile"],
          text=["Дирижабль с гироскопом, портативным двигателем, навигационным столом, "
                "автопушкой на палубе и пусковой под гондолой. Транспондер — чтобы своя "
                "ПВО не сбила. Сдайте четыре гироскопических механизма: флоту нужна "
                "стабильность."],
          tasks=[item("simulated:navigation_table"), item("create_radar:identification_transponder"),
                 give("simulated:gyroscopic_mechanism", 4)],
          rewards=loot(("aeronautics:pearlescent_levitite", 32), ("simulated:gyroscopic_mechanism", 8), xp=800,
                       text="Небо — ваше")),
    ],
)
