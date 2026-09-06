# -*- coding: utf-8 -*-
from dsl import chapter, Q, item, adv, dim, biome, check, chain

E = "eternal_tales:"


def a(name, note=None):
    return adv(E + name, note)


chapter(
    "et_overworld", "eternal", 60, "Обычный мир", E + "cobaltingot",
    "Руды, лунные события и первые боссы",
    [
        "Eternal Tales начинается не с порталов, а с того, что старый мир перестаёт "
        "быть знакомым: в породе появляется синий кобальт, ночью восходит красная луна, "
        "а под холмом кто-то роет улей.",
    ],
    chain([
        Q("ores", "Новые руды", E + "cobaltingot", 0, 0,
          text=["Олово, серебро, вольфрам, кобальт, рубин, уран, венетий. Кобальт — первый "
                "шаг за алмаз. Уран греет без защиты — и не по-доброму."],
          tasks=[a("get_cobalt"), a("get_cobalt_pickaxe"), a("get_ruby_pickaxe"), a("get_uranium_without_an_protection")]),
        Q("moons", "Лунные события", E + "bloody_totem", 0, 1,
          text=["Кровавая луна злит мобов, синяя заливает мир слизнями, клоунская — цирк "
                "до утра. Тотемы вызывают, добыча уникальна, выживание не гарантировано."],
          tasks=[a("make_the_blood_moon_rise"), a("stay_alive_during_blood_moon"),
                 a("make_the_blue_moon_rise"), a("make_the_clown_moon_rise")]),
        Q("bosses_ow", "Боссы обычного мира", E + "ravrite_queen_banner", 0, 2,
          text=["Королева рарритов в улье под землёй, Грозный саженец из плодородной "
                "земли, Гротестерк — наследие Ксакксасов, о которых вы пока ничего не знаете."],
          tasks=[a("kill_ravrite_queen"), a("kill_dreadful_sapling"), a("kill_grotesterk")]),
        Q("seasonal", "Сезонные боссы", E + "ekatebrina_banner", 1, 2,
          text=["Екатебрина — три ступени и ледяной змей. Дух Хэллоуина — в октябре."],
          tasks=[a("kill_ekatebrina"), a("kill_halloween_spirit")], optional=True),
        Q("vivid", "Вивид", E + "livetreebanner", 0, 3,
          text=["Тот, кто сжёг деревню, если верить Мигелю. Первый по-настоящему трудный "
                "бой мода; клятвенный меч после него служит долго."],
          tasks=[a("kill_vivid"), a("get_vivids_oathsword")]),
        Q("interdim", "Межпространственный создатель", E + "interdimensional_creator", 0, 4,
          text=["Станок, на котором из пяти редкостей и уровня колдовства складывается "
                "кристалл чужого мира. Возвратный билет — первое, что стоит на нём сделать: "
                "он вернёт домой откуда угодно и просит всего один уровень."],
          tasks=[item(E + "interdimensional_creator"), item(E + "return_ticket"), a("use_return_ticket")],
          rewards=["Пропуск во все измерения мода"]),
    ]),
)

chapter(
    "et_nether_end", "eternal", 70, "Нижний мир и Край", E + "hellish_clock",
    "Часовая башня пиглинов и Древний хорус",
    [],
    chain([
        Q("nether_tower", "Часовая башня", E + "hellish_clock", 0, 0,
          text=["Башня с часами, которыми пиглины не умели пользоваться, и замками, "
                "ключи от которых у надзирателей Пылающих Пустошей. Кто её построил, "
                "узнаете в Янтаре."],
          tasks=[a("nether_quest"), item(E + "hellish_key")]),
        Q("tsar", "Царь пиглинов", E + "tsar_of_piglins_banner", 0, 1,
          text=["Тот, у кого Хрустальная корона. И его колдун."],
          tasks=[a("kill_tsar_of_piglins"), a("kill_piglin_warlock")]),
        Q("nether_res", "Адские ресурсы", E + "bonespur", 1, 1,
          text=["Костяной шип, адская рыба, огненный мох — в кристаллы и алхимию."],
          tasks=[a("get_bonespur"), item(E + "nether_fish"), item(E + "nether_fire_moss_block")]),
        Q("end_quest", "Древний хорус", E + "ancient_chorus_fruit", 0, 2,
          text=["Плод, снимающий портальную болезнь — спутника всех, кто ходит между мирами."],
          tasks=[a("end_quest"), item(E + "ancient_chorus_fruit")]),
        Q("endacea", "Эндацея", E + "end_glowstone", 1, 2,
          text=["Такси Края."],
          tasks=[a("ride_endacea")], optional=True),
    ]),
)

chapter(
    "et_comets", "eternal", 80, "Кометы", E + "comet_banner",
    "Первое измерение: парящие острова и Ужасное древо",
    [],
    chain([
        Q("crystal", "Кристалл Комет", E + "comets", 0, 0,
          text=["Кристалл на создателе, портал из кометных межпространственных кирпичей, "
                "щелчок — и небо становится розовым."],
          tasks=[item(E + "comets")]),
        Q("enter", "Первый шаг", E + "blue_comets_grass_block", 0, 1,
          text=["Первый внеземной уровень почвы. Между островами — пустота, и она "
                "не прощает."],
          tasks=[a("into_comets"), dim(E + "comets")]),
        Q("skylite", "Скайлит и аэролит", E + "skylite_ingot", 0, 2,
          text=["Скайлит из руды, аэролит из сундуков. Оба нужны кристаллу Чистилища."],
          tasks=[item(E + "skylite_ingot"), a("get_aerolite_nugget")]),
        Q("tree", "Ужасное древо", E + "comet_banner", 0, 3,
          text=["Срубите кометное дерево Топором трагедии — и дерево ответит. Первый босс "
                "измерения; из него падает адский огонь для алтаря Чистилища."],
          tasks=[a("kill_terrible_tree")],
          rewards=["Ключ к Чистилищу"]),
        Q("quest_comets", "Задание Комет", E + "comet_flea_egg", 1, 3,
          text=["Банши в разрушенном доме, кометные блохи в кратере и история о войне, "
                "в которой Вулканех стёр этот мир с карты."],
          tasks=[a("comets_quest")]),
        Q("ice", "Ледяные земли", E + "cryothermic_ice", 1, 2,
          deps=["enter"],
          text=["Криотермический лёд и то, что в нём живёт."],
          tasks=[a("enter_into_comets_icelands_biome")], optional=True),
        Q("comethorn", "Комеророг", E + "geobstractsite_tubes", 2, 2,
          deps=["enter"],
          text=["Его можно приручить. Странная дружба."],
          tasks=[a("tame_comethorn")], optional=True),
    ]),
)

chapter(
    "et_purgatorium", "eternal", 90, "Чистилище", E + "purgatory_banner",
    "Тьма, Рок-Блейз и Павшая руна",
    [
        "Сюда ссылают. Отсюда не возвращаются — так считают в Королевстве Янтаря, "
        "и Хевелина, живущая в разрушенном доме с умирающим братом, с этим не спорит.",
        "Кристалл требует четвёртого уровня колдовства: огненный мох, скайлит, "
        "лапсидий, аэролит и адский камень.",
    ],
    chain([
        Q("hellrock", "Адский камень", E + "hellrock", 0, 0,
          text=["Астероидный камень к алтарю, адский огонь с Древа в руках — и алтарь отдаёт "
                "адский камень. Без него дверь вниз не открывается."],
          tasks=[item(E + "hellrock")]),
        Q("rock_blaze", "Рок-Блейз", E + "hellish_banner", 0, 1,
          text=["Алтарь, огонь, босс. С него — первая часть Павшей руны."],
          tasks=[a("kill_rock_blaze")]),
        Q("crystal_purg", "Кристалл Чистилища", E + "purgatorium", 0, 2,
          tasks=[item(E + "purgatorium"), a("into_purgatorium"), dim(E + "purgatorium")],
          text=["Портал из кирпичей Чистилища. Внутри темно всегда."]),
        Q("rune", "Павшая руна", E + "fallen_rune", 0, 3,
          text=["Первая часть — с Рок-Блейза, вторая — из дропа местных мобов, третья — "
                "у Странника, который продаёт её не за деньги."],
          tasks=[item(E + "fallen_rune")]),
        Q("nyetet", "Ниетет, Павший Титан", E + "purgatory_banner", 0, 4,
          text=["Когда-то он был героем. Руна на алтарь — и он придёт напомнить об этом. "
                "Из него сыплются осколки солнечного камня."],
          tasks=[a("kill_nyetet")],
          rewards=["Солнечный камень — ключ к Эдемским Садам"]),
        Q("quest_purg", "Задание Чистилища", E + "leviathan_blossom", 1, 3,
          text=["Пять Цветков левиафана для умирающего брата. И правда о том, почему "
                "Хевелина здесь."],
          tasks=[a("purgatorium_quest")]),
        Q("lapsidian", "Лапсидий", E + "lapsidian_ingot", 1, 2,
          deps=["crystal_purg"],
          text=["Металл этого мира. Кристаллы и снаряжение."],
          tasks=[item(E + "lapsidian_ingot"), item(E + "soulbone")]),
    ]),
)

chapter(
    "et_eden", "eternal", 100, "Эдемские Сады", E + "eden_banner",
    "Солнечный мир Санфурри",
    [
        "После Чистилища свет режет глаза. Здесь живут Санфурри — мессии, хускарлы и "
        "воины, — и здесь пили Напиток Солнца, пока Вулканех не пришёл за королём.",
        "Кристалл Эдема требует шестого уровня: серебро, два самородка солнечного камня, "
        "дыхание дракона и ослепление монстра.",
    ],
    chain([
        Q("sunstone", "Солнечный камень", E + "sun_stone_nugget", 0, 0,
          text=["Осколки с Ниетета — в целый камень. Камень — на портал в Крае."],
          tasks=[item(E + "sun_stone_nugget", 4)]),
        Q("enter_eden", "Врата Эдема", E + "edem_grass_block", 0, 1,
          tasks=[a("into_eden"), dim(E + "gardens_of_eden")],
          text=["Третий уровень почвы. Первый мир, где вам рады."]),
        Q("crystal_eden", "Кристалл Эдема", E + "gardens_of_eden", 0, 2,
          tasks=[item(E + "gardens_of_eden")]),
        Q("sunfurry", "Санфурри", E + "sunfurry_warrior_armor_helmet", 0, 3,
          text=["Их броня, их оружие, их торговля. Напиток Солнца — для мессий и тех "
                "чужаков, кто заслужил."],
          tasks=[a("eden_warrior"), a("eden_quest"), item(E + "drink_of_the_sun")]),
        Q("jaghax", "Джагакс", E + "eden_banner", 0, 4,
          text=["«Скажи, чего ты хочешь?» — спросит он. Отвечайте оружием."],
          tasks=[a("kill_jaghax")]),
        Q("adam_eve", "Адам и Ева", E + "eve_banner", 1, 4,
          text=["«Действительно ли ты первый?» Скрытые боссы сада."],
          tasks=[a("kill_adam"), a("kill_eve")], optional=True),
        Q("scorched", "Выжженные земли", E + "old_days_heart", 1, 3,
          deps=["enter_eden"],
          text=["Там, куда дошёл Вулканех."],
          tasks=[a("find_scorched_lands_of_eden_biome")]),
        Q("aragotium", "Арготий", E + "aragotium_ingot", 2, 3,
          deps=["enter_eden"],
          text=["Мифический металл. Компонент кристалла Вулканеха."],
          tasks=[a("get_aragotium_ingot")]),
    ]),
)

chapter(
    "et_rayana", "eternal", 110, "Раяна", E + "rayana_banner",
    "Тропики, вампиризм и Птерион",
    [
        "Джунгли, в которых ночь длится дольше, чем должна. Племя Аэде строит храмы, "
        "племя Даредиан прячется в горах, а между ними летает то, что принесло сюда "
        "болезнь.",
        "Кристалл требует восьмого уровня: даркплазма, костедуш, глаз разрушителя, "
        "кожа санхога, адская рыба.",
    ],
    chain([
        Q("crystal_ray", "Кристалл Раяны", E + "rayana", 0, 0,
          tasks=[item(E + "rayana"), a("get_destroyers_eye")]),
        Q("enter_ray", "Джунгли Раяны", E + "rayana_grass_block", 0, 1,
          tasks=[a("into_rayana"), dim(E + "rayana")],
          text=["Четвёртый уровень почвы. Гиацинтовое золото под ногами."]),
        Q("vampirism", "Вампиризм", E + "bloody_eye", 0, 2,
          text=["Вампиры роняют Кровавый камень. Из него и местных руд — Кровавый глаз."],
          tasks=[item(E + "bloody_eye")]),
        Q("pterion", "Птерион", E + "rayana_banner", 0, 3,
          text=["Глаз на алтарь Кровавого культа в храме Аэде — храм ищите по каменным "
                "столбам из земли. Птерион спустится сам. «Летающий ужас» на языке Аэде."],
          tasks=[a("kill_pterion"), a("rayana_quest")],
          rewards=["Избавление Раяны от заразы"]),
        Q("volkihar", "Волкихар", E + "volkihar", 1, 3,
          deps=["vampirism"],
          text=["Сила вампирского владыки — в ваших руках."],
          tasks=[a("get_volkihar")], optional=True),
        Q("kraken", "Заражённый кракен", E + "mucunfectio_banner", 1, 2,
          deps=["enter_ray"],
          text=["Большой, с щупальцами, из карантинной зоны Мукунфекцио."],
          tasks=[a("kill_infected_kracken"), a("find_mucunfectio_biome")], optional=True),
    ]),
)

chapter(
    "et_karvat", "eternal", 120, "Земли Карвата", E + "enicrih_power",
    "Божественный лес и божества",
    [
        "Древнее место, где боги ещё ходят по земле и отвечают на зов алтарей. "
        "Кристалл требует восьмого уровня: даркплазма, костедуш, кометный кристалл, "
        "спора эденнуса и багровый угорь.",
    ],
    chain([
        Q("crystal_kar", "Кристалл Карвата", E + "lands_of_karvat", 0, 0,
          tasks=[item(E + "lands_of_karvat")]),
        Q("enter_kar", "Древнее измерение", E + "karvat_grass_block", 0, 1,
          tasks=[a("into_karvat"), dim(E + "lands_of_karvat")]),
        Q("gods", "Боги Карвата", E + "enicrih_banner", 0, 2,
          text=["Энихрих — истинный король. Хациру — маг. Хиротс — болезнь. Иккорх — жизнь "
                "и смерть. Арла — сила. Каждый — свой алтарь, своя частица силы после боя."],
          tasks=[a("kill_enicrih"), a("kill_haciru"), a("kill_hirots"), a("kill_ikkorh"), a("kill_arla")]),
        Q("karvat_quest", "Божественная сила", E + "enicrih_power", 0, 3,
          text=["Украденный бог Гулибег и то, что от него осталось, — вам."],
          tasks=[a("karvat_quest"), a("get_piece_of_gulibegs_powers")]),
        Q("khogachi", "Хогачи", E + "khogachi_banner", 1, 2,
          deps=["enter_kar"],
          text=["Хранитель древа."],
          tasks=[a("kill_khogachi")], optional=True),
        Q("quetzal", "Кецалькоатль", E + "quetzalcoatl_banner", 2, 2,
          deps=["enter_kar"],
          text=["Пернатый змей и его жрец."],
          tasks=[a("kill_quetzalcoatl"), a("kill_chac_mool")], optional=True),
    ]),
)

chapter(
    "et_volcanech", "eternal", 130, "Вулканех", E + "volcanic_banner",
    "Вулканы, агрессия и предательство",
    [
        "Мир, который начал войну. Отсюда пришло уничтожение Комет и похищение "
        "короля Эдема; здесь же есть те, кто против. Кристалл требует десятого уровня: "
        "ихор, тапинелла, арготий, хитин жука, тёмный ихор.",
    ],
    chain([
        Q("crystal_vol", "Кристалл Вулканеха", E + "volcanech", 0, 0,
          tasks=[item(E + "volcanech")]),
        Q("enter_vol", "Раскалённый мир", E + "volcanite", 0, 1,
          tasks=[a("into_volcanech"), dim(E + "volcanech")]),
        Q("golem", "Вулканический голем", E + "volcanic_banner", 0, 2,
          text=["Он очень горячий. Это не метафора."],
          tasks=[a("kill_volcanic_golem")]),
        Q("sulfur", "Серная взрывчатка", E + "sulfur_tnt", 1, 2,
          deps=["enter_vol"],
          text=["Самое разрушительное, что есть до атомной бомбы. Атомная бомба тоже есть."],
          tasks=[a("blow_up_sulfur_tnt")]),
        Q("vol_quest", "Дезертирство", E + "blueprint", 0, 3,
          text=["Не все здесь хотят войны. Отсюда начинается дорога в Янтарь."],
          tasks=[a("volcanech_quest")]),
        Q("arahulum", "Арахулум", E + "arahulum_banner", 0, 4,
          text=["Все знакомые лица. Его глаз остаётся у победителя."],
          tasks=[a("kill_arahulum"), a("get_eye_of_arahulum")]),
        Q("brimstone", "Серный агарик", E + "brimstone_banner", 1, 4,
          deps=["enter_vol"],
          text=["Гриб. Босс. Грибной босс."],
          tasks=[a("kill_brimstone_agaric")], optional=True),
    ]),
)

chapter(
    "et_amber", "eternal", 140, "Королевство Янтаря", E + "royal_banner",
    "Светлое измерение с тёмной тайной",
    [
        "Богатый, светлый, вежливый мир, который ссылает в Чистилище неугодных и "
        "хранит в лабиринте то, о чём не говорят. Кристалл требует тринадцатого уровня: "
        "фарос, рыба иллюминатов, сфера пламени, труадамантит, Кристалл Величия.",
    ],
    chain([
        Q("truadamantite", "Труадамантит", E + "truadamantite_ingot", 0, 0,
          text=["Истинная сила. Броня и кисть — лучшие в своём роде."],
          tasks=[a("get_truadamantite_ingot"), a("get_truadamantite_armor")]),
        Q("greatness", "Кристалл Величия", E + "crystal_of_greatness", 0, 1,
          text=["И фарос — маяк. Оба — в кристалл Янтаря."],
          tasks=[item(E + "crystal_of_greatness"), item(E + "pharos")]),
        Q("crystal_amb", "Кристалл Янтаря", E + "kingdom_of_amber", 0, 2,
          tasks=[item(E + "kingdom_of_amber")]),
        Q("enter_amb", "Янтарные земли", E + "amber_grass_block", 0, 3,
          tasks=[a("into_amber"), dim(E + "kingdom_of_amber")],
          text=["Пятый, последний уровень почвы."]),
        Q("maze", "Янтарный лабиринт", E + "maze_lock_on", 0, 4,
          text=["Королевская тайна за замком. Ключ — в самом королевстве, у тех, кто "
                "не хочет, чтобы его нашли."],
          tasks=[a("explain_amber_maze"), a("amber_quest")]),
        Q("xaxxas", "Ксакксас XIX", E + "royal_banner", 0, 5,
          text=["Готовьтесь к войне. Правитель Янтаря — последний босс обычной прогрессии."],
          tasks=[a("kill_xaxxas_xix")],
          rewards=["Открывает путь к Унахзаалу"]),
        Q("keybekium", "Даредиан", E + "keybekium_ingot", 1, 4,
          deps=["enter_amb"],
          text=["Металл, из которого ковали оружие для вторжения в Эдем."],
          tasks=[item(E + "keybekium_ingot")]),
        Q("smuciel", "Смуциэль", E + "smuciel_banner", 1, 5,
          deps=["enter_amb"],
          text=["Божий суд. Скрытый босс."],
          tasks=[a("kill_smuciel")], optional=True),
    ]),
)

chapter(
    "et_unahzaal", "eternal", 150, "Унахзаал", E + "unahzaal_bricks",
    "Мультивселенная и конец пути",
    [],
    chain([
        Q("astral", "Повреждённый астрал", E + "damaged_astral", 0, 0,
          text=["Компонент кристалла. Восстановленный астрал — награда за то, что будет потом."],
          tasks=[item(E + "damaged_astral")]),
        Q("crystal_un", "Кристалл Унахзаала", E + "unahzaal_multiverse", 0, 1,
          text=["Янтарь, Кометы, Эдем, Вулканех и повреждённый астрал — в один кристалл."],
          tasks=[item(E + "unahzaal_multiverse")]),
        Q("enter_un", "Мультивселенная", E + "unahzaal_bricks", 0, 2,
          tasks=[a("into_unahzaal"), dim(E + "unahzaal_multiverse")]),
        Q("eye", "Глаз Унахзаала", E + "eye_of_unahzaal_banner", 0, 3,
          tasks=[a("kill_eye_of_unahzaal")]),
        Q("armor_un", "Броня Унахзаала", E + "grand_unahzaal_armor_helmet", 0, 4,
          text=["Хтоническая, орихалковая хтоническая, Великого жреца. Потолок защиты."],
          tasks=[a("get_chthonic_armor"), a("get_orichalcum_chthonic_armor"), a("get_grand_unahzaal_armor")]),
        Q("unahzaal", "Унахзаал", E + "unahzaal_bricks_dimension", 0, 5,
          text=["Конец пути. В Вечной Тьме бой другой, и награда другая — Кольцо Бедствия."],
          tasks=[a("kill_unahzaal")],
          rewards=["Завершение основной прогрессии Eternal Tales"]),
        Q("gifts", "Дары Унахзаала", E + "extradimensional_sting", 1, 5,
          deps=["unahzaal"],
          text=["Один из пяти. Выбирайте медленно."],
          tasks=[a("get_one_of_five_unahzaal_gifts")]),
        Q("tetra", "Тетраграмматон", E + "tetragrammaton_banner", 1, 4,
          deps=["enter_un"],
          text=["Ложный бог и последний хор."],
          tasks=[a("kill_tetragrammaton"), a("get_seraphim")], optional=True),
    ]),
)

chapter(
    "et_ultimate", "eternal", 160, "Ultimate World", E + "ultimate_world",
    "Аркемеры, эфирий и настоящий эндгейм",
    [
        "После конца пути есть ещё один мир. Его кристалл складывается из Унахзаала, "
        "Раяны, Чистилища, Карвата и Предельных кирпичей, а живут в нём Аркемеры — "
        "цивилизация, чьи машины делают чёрные дыры ручными.",
    ],
    chain([
        Q("crystal_ult", "Кристалл Ultimate World", E + "ultimate_world", 0, 0,
          tasks=[item(E + "ultimate_world"), item(E + "the_ultimate_bricks")]),
        Q("enter_ult", "Предельный мир", E + "ultimate_world", 0, 1,
          tasks=[a("enter_in_the_ultimate_world"), dim(E + "ultimate_world")]),
        Q("aetherium", "Эфирий", E + "aetherium", 0, 2,
          text=["Энергия Аркемеров: броня, трубки, оружие."],
          tasks=[a("get_aetherium"), a("get_arkemer_aetherium_imbued_armor")]),
        Q("arkemer_tech", "Технологии Аркемеров", E + "arkemer_quarry", 0, 3,
          text=["Карьер, шреддер, гравицикл, смартфон. Рельсотрон «Алеф» и «Разрушитель "
                "небес» — их оружие."],
          tasks=[a("get_arkemer_quarry"), a("make_arkemer_gravicycle"), a("get_arkemer_aleph_railgun"),
                 a("make_arkemer_rift_heavenbreaker")]),
        Q("blackhole", "Чёрная дыра в руках", E + "stabilized_miniature_black_hole", 0, 4,
          text=["Стабилизированная. Маленькая. В кармане. Броня, кованная в эргосфере."],
          tasks=[a("get_stabilized_miniature_black_hole"), a("get_ergosphere_forged_armor")]),
        Q("emblems", "Эмблемы", E + "grand_emblem", 0, 5,
          text=["Великая, сингулярности, Аркемеров."],
          tasks=[a("get_the_grand_emblem"), a("get_singularity_emblem"), a("get_arkemer_emblem")]),
        Q("ultimate_items", "Предельные предметы", E + "the_ultimate_two", 0, 6,
          text=["The Ultimate One, The Ultimate Two, Перчатка Судеб, Сердце Стихий, Первая "
                "Призма, Порядок Вселенной. Дальше предметов нет."],
          tasks=[a("get_the_ultimate_one"), a("get_the_ultimate_two"), a("get_gauntlet_of_the_destinies"),
                 a("get_heart_of_the_elements"), a("get_the_first_prism"), a("learn_order_of_the_universe")],
          rewards=["Абсолютный потолок Eternal Tales"]),
        Q("hammer", "Молот Вечности", E + "hammer_of_eternity", 1, 5,
          deps=["arkemer_tech"],
          text=["Мультитул, божественные кирка и мотыга."],
          tasks=[a("get_hammer_of_eternity"), a("get_divine_pickaxe"), a("get_divine_hoe")]),
        Q("aftermath", "Aftermath", E + "ageagoria_anthem", 0, 7,
          text=["То, что случилось после. Испытание камня Флечереши — Новая игра+."],
          tasks=[a("aftermath_quest"), a("pass_flecheresha_stone_trial")],
          rewards=["Полное прохождение сюжета Eternal Tales"]),
    ]),
)

chapter(
    "et_darkness", "eternal", 170, "Вечная Тьма", E + "totem_of_eternal_darkness",
    "Режим повышенной сложности и человечность",
    [],
    chain([
        Q("activate", "Активация", E + "totem_of_eternal_darkness", 0, 0,
          text=["Тотем Вечности. Все сильнее, всё опаснее. Обратимо."],
          tasks=[a("activate_eternal_darkness_mode")]),
        Q("humanity", "Человечность", E + "forge_of_the_light", 0, 1,
          text=["Растёт от злых, падает от добрых. Управляет эссенциями и открывает двух "
                "боссов, которых иначе нет."],
          tasks=[a("get_100_humanity")]),
        Q("nox_luc", "Ноксифер и Люциден", E + "noxifer_banner", 0, 2,
          text=["Тьма и свет. Только здесь."],
          tasks=[a("kill_noxifer"), a("kill_luciden")]),
        Q("rings_dark", "Кольца Тьмы", E + "calamity_ring", 0, 3,
          text=["Бедствия, гарпии, кровавых слёз."],
          tasks=[a("get_calamity_ring"), a("get_harpy_ring"), a("get_ring_of_crimson_tears")]),
        Q("super", "Super Duper Darkness", E + "totem_of_death", 0, 4,
          text=["Достижение называется «Самоубийца». Это предупреждение."],
          tasks=[a("activate_super_duper_darkness_mode"), a("kill_unahzaal_with_hard_mode")], optional=True),
    ]),
)

chapter(
    "et_gear", "eternal", 180, "Снаряжение Eternal Tales", E + "truadamantite_armor_chestplate",
    "Брони, оружие и артефакты",
    [],
    [
        Q("armors_early", "Ранние брони", E + "charged_copper_armor_chestplate", 0, 0,
          text=["Заряженная медь, сломанные кости, рейнджер, охотник за сокровищами."],
          tasks=[adv(E + "get_charged_copper_armor"), adv(E + "get_forest_ranger_armor"), adv(E + "get_treasure_hunter_armor")]),
        Q("armors_mid", "Средние брони", E + "dark_mage_armor_chestplate", 1, 0,
          text=["Тёмный маг, чародей, китобой, слизистые потроха, рунная."],
          tasks=[adv(E + "get_dark_mage_armor"), adv(E + "get_walock_armor"), adv(E + "get_whaler_armor"), adv(E + "get_runic_armor")]),
        Q("armors_late", "Поздние брони", E + "truadamantite_armor_chestplate", 2, 0,
          text=["Труадамантит, хтоника, орихалк, жрец, эргосфера, эфирий."],
          tasks=[adv(E + "get_truadamantite_armor"), adv(E + "get_ergosphere_forged_armor")]),
        Q("weapons", "Оружие", E + "ammit_staff", 0, 1,
          text=["Посох Аммита, посох Хонсу, оружие Мишкоатля, Кровавый якорь, Убийца "
                "головоногих, Коса смерти, Крылья архангела — по чертежам из земли."],
          tasks=[adv(E + "get_ammit_staff"), adv(E + "get_khonshu_staff"), adv(E + "get_bloody_anchor"), adv(E + "get_hoz_de_muerte")]),
        Q("ranged", "Дальний бой", E + "atimites_crossbow", 1, 1,
          text=["Арбалет Атимиты, пушка Ракеты, Бовапрель, рельсотрон Аркемеров."],
          tasks=[adv(E + "get_atimites_crossbow"), adv(E + "get_rockets_gun")]),
        Q("accessories", "Аксессуары", E + "celestial_sphere", 2, 1,
          text=["Небесная сфера, Наблюдающая сфера, Мыслящий камень, Эхо-якорь, "
                "амулеты неуязвимости."],
          tasks=[adv(E + "get_celestial_sphere"), adv(E + "get_thinking_stone"), adv(E + "get_any_of_immunity_accessories")]),
        Q("storage_et", "Переносные сундуки", E + "portable_chest", 0, 2,
          text=["Сундук, который идёт с вами."],
          tasks=[adv(E + "get_portable_chest"), adv(E + "get_big_portable_chest")], optional=True),
        Q("fun", "Курьёзы", E + "smartphone", 1, 2,
          text=["Смартфон, фурсьюты, лава-лампы, энергетик, гравицикл. Мод умеет смеяться."],
          tasks=[adv(E + "make_smartphone"), adv(E + "get_all_of_the_lava_lamps"), adv(E + "use_energy_drink")],
          optional=True),
    ],
)
