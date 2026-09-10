# -*- coding: utf-8 -*-
"""Cataclysm и компания: боссы, подземелья и трофейное оружие."""
from dsl import chapter, Q, item, give, adv, check, loot, chain

C = "cataclysm:"


def a(name, note=None):
    return adv(C + name, note)


chapter(
    "hunt_cataclysm", "hunt", 10, "Катаклизм", C + "the_incinerator",
    "Восемь подземелий, десять боссов и оружие, которого больше нигде нет",
    [
        "L_Ender's Cataclysm не добавляет ни руд, ни машин. Он добавляет причины "
        "выходить из дома: восемь огромных структур, в каждой сидит нечто, что "
        "убьёт вас с одного захода.",
        "Прогрессии в привычном смысле здесь нет — есть порядок по силе. Начинают "
        "с песков и затопленного города, заканчивают Древней фабрикой, где живёт "
        "Предвестник.",
        "Оружие с боссов не крафтится ни из чего другого и не имеет аналогов. "
        "Ради него всё и затевается.",
    ],
    [
        Q("root", "Первая находка", C + "black_steel_ingot", 0, 0,
          text=[
              "Мод раскидывает по миру заброшенные шпили, храмы и деревни — они "
              "попадаются сами, без поиска. В них лежат чёрная сталь и древний металл: "
              "материалы, из которых собирают снаряжение перед первым боссом.",
              "Компас исследователя ищет любую структуру мода по названию.",
          ],
          tasks=[item(C + "black_steel_ingot", 4), item(C + "ancient_metal_ingot", 4)],
          rewards=loot((C + "black_steel_ingot", 8), xp=150)),

        Q("pyramid", "Проклятая пирамида", C + "khopesh", -1, 1, deps=["root"],
          text=[
              "Пустынная гробница с ловушками и мумиями. Внутри — Древний останок, "
              "страж с копьём, и хопеш, который бьёт по площади.",
              "Песчаная буря в бутылке оттуда же: бросьте — и получите личный смерч.",
          ],
          tasks=[a("find_cursed_pyramid"), a("kill_remnant"), item(C + "khopesh")],
          rewards=loot((C + "sandstorm_in_a_bottle", 2), xp=300)),

        Q("sunken", "Затопленный город", C + "tidal_claws", 1, 1, deps=["root"],
          text=[
              "Руины на дне океана, кораллы и то, что в них живёт. Сцилла и "
              "Коралловый колосс охраняют город.",
              "Приливные когти бьют быстрее любого меча, коралловая алебарда — "
              "дальше любого копья.",
          ],
          tasks=[a("find_sunken_city"), a("kill_scylla"), item(C + "tidal_claws")],
          rewards=loot((C + "coral_bardiche", 1), xp=300)),

        Q("frosted", "Ледяная тюрьма", C + "wither_assault_shoulder_weapon", 0, 2,
          deps=["pyramid", "sunken"],
          text=[
              "Крепость во льдах, где держат Клаудиана — механического зверя, "
              "пережившего своих создателей.",
              "С него падает наплечное орудие иссушителя: оно стреляет само, пока "
              "вы заняты другим.",
          ],
          tasks=[a("find_frosted_prison"), a("kill_clawdian"),
                 item(C + "wither_assault_shoulder_weapon")],
          rewards=loot((C + "witherite_ingot", 4), xp=500)),

        Q("burning", "Горящая арена", C + "the_incinerator", 0, 3, deps=["frosted"],
          text=[
              "Круглая арена в Нижнем мире и Игнис — рыцарь в доспехах из "
              "застывшей магмы. Один из самых тяжёлых боёв мода.",
              "Мусоросжигатель с него — двуручный молот, который поджигает всё, "
              "во что попадает. Игнитиум оттуда же: броня, держащая лаву как воду.",
          ],
          tasks=[a("find_burning_arena"), a("kill_ignis"), item(C + "the_incinerator"),
                 item(C + "ignitium_ingot", 4)],
          rewards=loot((C + "ignitium_ingot", 8), xp=800)),

        Q("ignitium", "Броня Игнитиума", C + "ignitium_elytra_chestplate", 1, 3,
          deps=["burning"],
          text=[
              "Полный комплект даёт огнеупорность и не горит в лаве. Нагрудник с "
              "элитрами — единственный способ летать, не снимая брони.",
              "Шаблон улучшения падает там же, на арене.",
          ],
          tasks=[item(C + "ignitium_helmet"), item(C + "ignitium_elytra_chestplate"),
                 item(C + "ignitium_upgrade_smithing_template")],
          rewards=loot((C + "ignitium_ingot", 8), xp=600)),

        Q("acropolis", "Акрополь", C + "monstrous_helm", -1, 4, deps=["burning"],
          text=[
              "Античные развалины, где живёт Чудовище — гора мышц с глазом во лбу. "
              "Его шлем даёт сопротивление всему подряд, рог зовёт подмогу.",
          ],
          tasks=[a("find_acropolis"), a("kill_monstrosity"), item(C + "monstrous_helm")],
          rewards=loot((C + "monstrous_horn", 1), xp=700)),

        Q("citadel", "Разрушенная цитадель", C + "void_forge", 0, 5, deps=["burning"],
          text=[
              "Крепость Края, Эндер-страж и Эндер-голем. Здесь добывают Пустотный "
              "горн — меч, который бьёт по всему в радиусе и телепортирует владельца.",
          ],
          tasks=[a("find_ruined_citadel"), a("kill_ender_guardian"), item(C + "void_forge")],
          rewards=loot(("minecraft:ender_pearl", 32), xp=900)),

        Q("factory", "Древняя фабрика", C + "laser_gatling", 0, 6, deps=["citadel"],
          text=[
              "Завод, который работает без людей уже очень давно. Внутри — "
              "Предвестник, самый сильный босс мода, и лазерный гатлинг, которым "
              "он вас встретит.",
              "Механическая наковальня оттуда же: она соединяет трофеи в вещи, "
              "которые иначе не получить.",
          ],
          tasks=[a("find_ancient_factory"), a("kill_harbinger"),
                 item(C + "laser_gatling"), item(C + "mechanical_fusion_anvil")],
          rewards=loot((C + "mech_eye", 1), xp=1500)),

        Q("leviathan", "Левиафан", C + "abyssal_sacrifice", 1, 5, deps=["sunken"],
          text=[
              "Морской босс, которого призывают Бездонной жертвой. Огромный, "
              "быстрый и злопамятный.",
          ],
          tasks=[item(C + "abyssal_sacrifice"), a("kill_leviathan")],
          rewards=loot((C + "tidal_claws", 1), xp=800), optional=True),

        Q("maledictus", "Мальдиктус", C + "music_disc_maledictus", -1, 5,
          deps=["acropolis"],
          text=["Проклятый всадник, за которым остаётся собственная пластинка. "
                "Появляется в пустынных землях."],
          tasks=[a("kill_maledictus")],
          rewards=loot((C + "cursium_ingot", 4), xp=700), optional=True),

        Q("all_bosses", "Все до одного", C + "kobolediator_skull", 0, 7,
          deps=["factory"],
          text=[
              "Десять боссов: Древний останок, Сцилла, Клаудиан, Игнис, Чудовище, "
              "Эндер-страж, Эндер-голем, Левиафан, Мальдиктус и Предвестник.",
              "Мод ведёт счёт сам и выдаёт достижение, когда список закончится. "
              "Это одна из самых длинных охот в сборке.",
          ],
          tasks=[a("kill_all_bosses")],
          rewards=loot((C + "ignitium_ingot", 16), ("minecraft:netherite_ingot", 4), xp=3000,
                       text="Полный трофейный зал")),
    ],
)

chapter(
    "hunt_beasts", "hunt", 20, "Звери и мутанты", "alexsmobs:animal_dictionary",
    "Alex's Mobs, Mowzie's Mobs и Mutant Monsters",
    [
        "Три мода наполняют мир живностью, которой в ванили не хватало: от "
        "безобидных капибар до боссов, ради которых строят арену.",
        "Alex's Mobs — это сотня существ с собственными повадками и полезным дропом. "
        "Mowzie's Mobs — четыре босса с постановочными боями. Mutant Monsters — "
        "ванильные мобы, которым дали вырасти.",
    ],
    [
        Q("dictionary", "Определитель животных", "alexsmobs:animal_dictionary", 0, 0,
          text=[
              "Книга Alex's Mobs: где живёт, чем питается, что даёт. С ней охота "
              "перестаёт быть угадайкой.",
              "Многих зверей можно приручить, некоторых — оседлать, а с кого-то "
              "падают вещи, которых больше взять негде.",
          ],
          tasks=[item("alexsmobs:animal_dictionary")],
          rewards=loot(("minecraft:book", 4), xp=80)),

        Q("mutants", "Мутанты", "mutantmonsters:mutant_skeleton_spawn_egg", 1, 0,
          text=[
              "Мутантный зомби бьёт по площади и швыряет вас в воздух, мутантный "
              "скелет разбирает броню, мутантный крипер оставляет воронку размером "
              "с дом, мутантный эндермен таскает блоки прямо из-под ног.",
              "Появляются редко и сами. Встреча всегда неожиданная.",
          ],
          tasks=[check("Встретить любого мутанта Mutant Monsters")],
          rewards=loot(("minecraft:golden_apple", 4), xp=200)),

        Q("mowzie", "Боссы Mowzie's", "mowziesmobs:wrought_axe", 0, 1,
          text=[
              "Феррус — рыцарь с топором, стоящий в подземном зале и не двигающийся, "
              "пока его не тронешь. Умвути — древний дух джунглей. Барако — "
              "солнечный вождь на троне.",
              "Бои поставлены как в приключенческой игре: с фазами, паузами и "
              "моментами, когда надо просто отбежать.",
          ],
          tasks=[check("Победить любого босса Mowzie's Mobs")],
          rewards=loot(("minecraft:diamond", 8), xp=500)),

        Q("hunt_gear", "Охотничьи трофеи", "alexsmobs:shark_tooth", 0, 2,
          deps=["dictionary"],
          text=[
              "С акулы — зубы, с кенгуру — сумка, с крокодила — броня, с "
              "мурены — щупальца. Часть дропа Alex's Mobs идёт в снаряжение, "
              "которого нет ни в одном другом моде сборки.",
          ],
          tasks=[check("Собрать любой трофей Alex's Mobs")],
          rewards=loot(("minecraft:emerald", 16), xp=300), optional=True),

        Q("combat", "Новая боёвка", "minecraft:iron_sword", 1, 2,
          text=[
              "Better Combat меняет удары: у каждого типа оружия своя дуга, "
              "своя дальность и своё число целей. Меч рубит вбок, копьё колет "
              "далеко, топор бьёт сверху и медленно.",
              "Против боссов Cataclysm это уже не мелочь, а разница между "
              "победой и десятью попытками.",
          ],
          tasks=[check("Прочитано: у каждого оружия своя дуга удара")],
          rewards=loot(("minecraft:iron_ingot", 16), xp=100)),
    ],
)
