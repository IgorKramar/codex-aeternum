# -*- coding: utf-8 -*-
from dsl import chapter, Q, item, adv, dim, biome, check, chain

E = "eternal_tales:"


def a(name, note=None):
    return adv(E + name, note)


chapter(
    "et_intro", "eternal", 10, "Вечные сказания", E + "journal",
    "Журнал, Вечный город и доски объявлений",
    [],
    chain([
        Q("journal", "Журнал", E + "journal", 0, 0,
          text=["Тетрадь, в которую записывают обещания. Задания дают NPC Вечного города "
                "и поселений измерений; журнал помнит условия и награды, даже когда "
                "вы забыли, кто просил."],
          tasks=[item(E + "journal"), a("get_any_quest")]),
        Q("town", "Вечный город", E + "eternal_town_spawner", 0, 1,
          text=["Город музыкантов, построенный одним человеком для одной девочки. Здесь "
                "живут Аэтер, Мигель-Рассказчик, торговцы трофеями и бард, который играет "
                "за монету. Отсюда начинается всё."],
          tasks=[a("overworld_quest", "Задание «Город музыкантов»")]),
        Q("notice", "Доска объявлений", E + "notice_board", 0, 2,
          text=["Доска — учебник мода и одновременно место, где тратят очки уровня. "
                "Прочтите все: колдовство, археология, рыбалка, режим Тьмы, рецепты "
                "кристаллов — всё описано там, и написано теми, кто это придумал."],
          tasks=[item(E + "notice_board"), a("upgrade_skill_with_notice_board")]),
        Q("starter", "Стартовый набор", E + "starter_kit", 1, 2,
          text=["Сундук с тем, что пригодится в первый день."],
          tasks=[item(E + "starter_kit")], optional=True),
        Q("miguel", "Мигель-Рассказчик", "minecraft:egg", 0, 3,
          text=["Он продаёт призывы боссов и знает историю сгоревшей деревни, Вивида и "
                "девочки по имени Вечность. Не всё, что он говорит, правда. Но всё важно."],
          tasks=[a("spawn_miguel")]),
        Q("bard", "Бард", "minecraft:note_block", 1, 3,
          text=["Монета — песня. Гитару можно взять и себе."],
          tasks=[a("give_a_coin_to_the_bard"), item(E + "guitar")], optional=True),
        Q("coins", "Монеты", E + "ancient_coin", 2, 3,
          text=["Древние и золотые. Валюта торговцев мода, лежит в сундуках и карманах мобов."],
          tasks=[a("get_ancient_coin"), a("get_gold_coin")], optional=True),
        Q("quests_all", "Все задания", E + "let_us_tell_you_a_story_music_disc", 0, 4,
          deps=["miguel"],
          text=["Обычный мир, Нижний, Край, каждое измерение и линия Aftermath. Пройти "
                "всё — значит услышать историю целиком, от первой деревни до последней "
                "пластинки."],
          tasks=[a("pass_all_quests")],
          rewards=["Полная сюжетная линия Eternal Tales"]),
    ]),
)

chapter(
    "et_skills", "eternal", 20, "Навыки", E + "digging_skill_stone_active",
    "Девять навыков и очки уровня",
    [
        "Навыки растут сами — от того, что вы делаете. Каждый новый уровень любого из них "
        "даёт очко, которое можно вложить в любой другой через доску. Так копатель "
        "становится колдуном, а колдун — рыбаком, если очень нужно.",
    ],
    [
        Q("level", "Уровень игрока", "minecraft:experience_bottle", 0, 0,
          text=["Повысили навык — получили очко. Вложили очко — повысили навык. Круг, "
                "который крутится в вашу пользу."],
          tasks=[a("get_any_skill_boost_effect")]),
        Q("digging", "Копание", "minecraft:diamond_pickaxe", -1, 1,
          text=["От руды. Выше уровень — чаще лишний кусок."],
          tasks=[a("get_first_digging_skill_level"), item(E + "digging_chest")]),
        Q("slaying", "Убийство", "minecraft:iron_sword", 0, 1,
          text=["От мобов: очки равны их здоровью, делённому на двадцать. Открывает эмблемы."],
          tasks=[check("Поднять навык убийства")]),
        Q("archery", "Стрельба", "minecraft:bow", 1, 1,
          text=["От луков и метательного. Открывает ювелирный стол и перчатку лучника."],
          tasks=[a("get_any_archery_armor")]),
        Q("growing", "Выращивание", E + "gardeners_pot", -1, 2,
          text=["От растений в горшке садовника. С пятого уровня — вода и удобрение."],
          tasks=[a("get_gardeners_pot"), item(E + "growing_chest")]),
        Q("fishing", "Рыбалка и ловля", E + "fish_web", 0, 2,
          text=["Рыбалка — от редкой рыбы, ловля — от насекомых в сачке. Насекомые "
                "становятся наживкой; чем реже жук, тем ценнее улов."],
          tasks=[a("get_fishing_web"), item(E + "bug_net"), item(E + "fishing_chest")]),
        Q("archaeology_skill", "Археология", E + "venetium_brush", 1, 2,
          text=["От раскопок кистью и от разбора чертежей в шреддере."],
          tasks=[a("excavate_suspicious_block_by_venetium_or_truadamantite_brush")]),
        Q("speech", "Красноречие", "minecraft:emerald", -1, 3,
          text=["От торговли. Скидки растут."],
          tasks=[check("Поторговать с торговцем Eternal Tales")]),
        Q("sorcery_skill", "Колдовство", E + "sorcery_skill_stone_active", 0, 3,
          text=["От рунных камней, эссенций и артефактов. Без уровня колдовства кристалл "
                "измерения не соберётся — это главный замок мода."],
          tasks=[a("get_rune"), item(E + "sorcery_chest")]),
        Q("fear", "Страх", E + "totem_of_eternal_darkness", 1, 3,
          text=["Только в Вечной Тьме. От мобов под страхом; даёт скорость, силу и ночное "
                "зрение по уровню."],
          tasks=[a("activate_eternal_darkness_mode")], optional=True),
    ],
)

chapter(
    "et_sorcery", "eternal", 30, "Колдовство", E + "rune_tab_all",
    "Руны, эссенции, матрица и астральные чары",
    [
        "Колдовство здесь — ремесло. Руны выпадают из камней, камни стоят в каждом мире, "
        "и у каждого мира — своя руна. Из рун варят эссенции, из эссенций — силу.",
    ],
    chain([
        Q("runes", "Руны", E + "rune_tab_all", 0, 0,
          text=["Рунные камни ломают киркой; чары «Рунный старатель» умножают выпадение. "
                "Лесные, пустынные, адские, кометные, эдемские — по мирам. Сумка хранит."],
          tasks=[a("get_rune"), item(E + "rune_bag")]),
        Q("cauldron", "Котёл извлечения", E + "extraction_cauldron", 0, 1,
          text=["Больше двадцати рун — в котёл на песке душ, и получаются эссенции: "
                "валюта, за которую покупают артефакты и заряжают матрицу."],
          tasks=[a("get_extraction_cauldron"), a("get_essence_gem")]),
        Q("matrix", "Рунная матрица", E + "runic_armor_helmet", 0, 2,
          text=["Матрица кладёт руны на броню и оружие. Рунная броня — то, что в неё вложили."],
          tasks=[a("get_runic_matrix_enchantment"), a("get_runic_armor")]),
        Q("books", "Книги заклинаний", E + "sorcery_book_achievement_item", 0, 3,
          text=["Свечение, милость дельфина, портальная болезнь и десятки других — "
                "одноразовые и многоразовые."],
          tasks=[a("get_any_sorcery_book")]),
        Q("astral", "Астральный зачарователь", E + "astral_enchancer", 0, 4,
          text=["Чары, которых нет у обычного стола, и уровни выше обычного предела."],
          tasks=[a("enchant_something_on_astral_enchancer")]),
        Q("rituals", "Ритуалы", E + "ritual_activator_luck_blueprint", 0, 5,
          text=["Активаторы вызывают духов, приносят удачу, насылают проклятия, роняют "
                "звёзды. Чертежи — на ювелирном столе, копии — на принтере."],
          tasks=[a("get_any_blueprint"), a("duplicate_blueprint_on_printer")]),
        Q("altars", "Алтари", E + "arei_altar", 1, 5,
          text=["Ареи, Арлы, Арахулума, Хациру, Хиротса, Иккорха, Энихриха, кровавый, "
                "чистилищный, адский, королевский. Каждый зовёт своего."],
          tasks=[item(E + "arei_altar")], optional=True),
    ]),
)

chapter(
    "et_archaeology", "eternal", 40, "Археология", E + "venetium_brush",
    "Кисти, чертежи, вазы и тотемы",
    [],
    chain([
        Q("brush", "Кисти", E + "venetium_brush", 0, 0,
          text=["Венетиевая — начало, труадамантитовая — предел. Подозрительные блоки "
                "ждут в каждом мире."],
          tasks=[item(E + "venetium_brush"), a("excavate_suspicious_block_by_venetium_or_truadamantite_brush")]),
        Q("sherds", "Черепки и вазы", E + "brilliant_neodymium_vase", 0, 1,
          text=["Из черепков — неодимовые и урановые вазы. Урановые светятся и не в шутку."],
          tasks=[a("get_any_of_neodymium_pottery_sherds"), a("get_any_of_neodymium_vases")]),
        Q("blueprints", "Чертежи", E + "blueprint", 0, 2,
          text=["Из земли достают планы оружия, которого больше никто не делает: посох "
                "Аммита, крылья архангела, кровавый якорь."],
          tasks=[a("get_any_blueprint")]),
        Q("shredder", "Шреддер", E + "shredder", 0, 3,
          text=["Разбирает чертёж и учит вас на этом. Аркемерский — лучше."],
          tasks=[a("remove_the_blueprint_in_shredder_to_increase_archaeology_skill_level")]),
        Q("totems", "Керамические тотемы", E + "ceramic_totem", 0, 4,
          text=["Благословения богов на постоянной основе."],
          tasks=[a("get_any_archaeology_totem")]),
        Q("jewelry", "Ювелирный стол", E + "jewelry_table", 1, 2,
          deps=["brush"],
          text=["Рубин, топаз, корунд, янтарь. Качество — от лупы, наждака и навыка "
                "стрельбы. Здесь же перчатки и кольца."],
          tasks=[item(E + "jewelry_table"), item(E + "magnifying_glass"), item(E + "sandpaper")]),
        Q("rings", "Кольца", E + "gold_ring", 2, 2,
          deps=["jewelry"],
          text=["Ликантропии, гарпии, кровавых слёз, Хирсина. В слоты аксессуаров."],
          tasks=[a("get_gold_ring")], optional=True),
    ]),
)

chapter(
    "et_farming", "eternal", 50, "Сад, рыбалка и ловля", E + "gardeners_pot",
    "Горшки, машины, сети и сачки",
    [],
    chain([
        Q("pot", "Горшок садовника", E + "gardeners_pot", 0, 0,
          text=["Растение сверху, почва в слот, с пятого уровня — вода и удобрение. "
                "Адский и внеземной горшки — для флоры других миров."],
          tasks=[a("get_gardeners_pot"), a("get_nether_gardeners_pot"), a("get_ectraterrestrial_gardeners_pot")]),
        Q("machines", "Машины", E + "irrigating_machine", 0, 1,
          text=["Одна поливает, другая удобряет. Обе — без вас."],
          tasks=[a("get_irrigating_machine"), a("get_fertilizing_machine")]),
        Q("fishing_nets", "Рыболовные сети", E + "fish_web", 0, 2,
          text=["Сеть ловит сама, адская — в лаве."],
          tasks=[a("get_fishing_web"), a("get_nether_fishing_web")]),
        Q("bugs", "Сачок", E + "bug_net", 0, 3,
          text=["Жуки — наживка. Редкий жук — редкая рыба."],
          tasks=[item(E + "bug_net")]),
        Q("pets", "Питомцы", E + "raccoon_flag", 0, 4,
          text=["Еноты, гультравы, тарко, комерог, королева рарритов. Енота можно погладить."],
          tasks=[a("pet_the_raccoon"), a("tame_all_types_of_gultravs")], optional=True),
    ]),
)
