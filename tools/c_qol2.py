# -*- coding: utf-8 -*-
"""Новые удобства расширенной сборки."""
from dsl import chapter, Q, item, give, adv, check, loot, chain

chapter(
    "more_qol2", "more", 15, "Новые удобства", "buildinggadgets2:gadget_building",
    "Гаджеты, молоты, баки и прочее, что экономит часы",
    [
        "Сборка выросла вдвое, и вместе с ней выросло число мелочей, которые "
        "делают её терпимой. Эта глава — про них.",
    ],
    [
        Q("gadgets", "Building Gadgets 2", "buildinggadgets2:gadget_building", 0, 0,
          text=[
              "Строительный гаджет копирует блок под прицелом и кладёт его рядами, "
              "стенами, лестницами или по поверхности. Обменный меняет один блок "
              "на другой в целой стене. Разрушающий сносит объём за раз.",
              "Копирующий снимает постройку в шаблон и ставит её где угодно — "
              "это схематическая пушка Create, только в кармане.",
              "Все гаджеты работают на энергии FE, так что подключите их к сети.",
          ],
          tasks=[item("buildinggadgets2:gadget_building"),
                 item("buildinggadgets2:gadget_exchanging"),
                 item("buildinggadgets2:gadget_copy_paste"),
                 item("buildinggadgets2:template_manager")],
          rewards=loot(("minecraft:diamond", 8), xp=200)),

        Q("hammers", "Just Hammers", "justhammers:iron_hammer", 1, 0,
          text=[
              "Молот ломает не блок, а область: три на три, потом пять на пять, "
              "а разрушитель — пять на пять на пять.",
              "Формы улучшаются через ядра, и первое ядро требует уже готовый "
              "незеритовый молот — так что путь неблизкий. Зато карьер после "
              "него копается руками.",
          ],
          tasks=[item("justhammers:iron_hammer")],
          rewards=loot(("minecraft:iron_block", 4), xp=150)),

        Q("trash", "Trash Cans", "trashcans:item_trash_can", 2, 0,
          text=[
              "Бак для предметов, бак для жидкостей, бак для энергии и "
              "универсальный, который ест всё сразу.",
              "У каждого фильтр на девять позиций с белым и чёрным списком. "
              "Автоматика перестаёт захлёбываться булыжником.",
          ],
          tasks=[item("trashcans:item_trash_can"), adv("trashcans:trash_can")],
          rewards=loot(("minecraft:hopper", 4), xp=120)),

        Q("lootr2", "Lootr", "lootr:trophy", 3, 0,
          text=[
              "Сундук в структуре теперь личный: каждый игрок открывает свой "
              "набор добычи и не может обнести чужой.",
              "Мод считает, сколько контейнеров вы открыли, и за сотню выдаёт "
              "Столетний трофей.",
          ],
          tasks=[adv("lootr:1chest"), adv("lootr:social")],
          rewards=loot(("minecraft:gold_ingot", 16), xp=200)),

        Q("compasses", "Компасы", "naturescompass:naturescompass", 0, 1,
          text=[
              "Компас природы ищет биом по названию, компас исследователя — "
              "структуру. Оба показывают направление, расстояние и измерение.",
              "В мире со ста биомами и полусотней типов структур это разница "
              "между «нашёл за минуту» и «искал весь вечер».",
          ],
          tasks=[item("naturescompass:naturescompass"),
                 item("explorerscompass:explorerscompass")],
          rewards=loot(("minecraft:map", 4), xp=150)),

        Q("enchdesc", "Описания чар", "minecraft:enchanted_book", 1, 1,
          text=[
              "Enchantment Descriptions пишет прямо в подсказке, что делает "
              "каждая чара. Зажмите Shift на зачарованной книге.",
              "Polymorph рядом решает вторую вечную проблему больших сборок: "
              "когда на одну раскладку в верстаке подходит пять рецептов, "
              "он даёт выбрать нужный.",
          ],
          tasks=[check("Прочитано: Shift показывает описание чары")],
          rewards=loot(("minecraft:lapis_lazuli", 32), xp=100)),

        Q("macaw", "Серия Macaw's", "mcwroofs:oak_roof", 2, 1,
          text=[
              "Семь модов, шесть тысяч блоков декора: крыши под настоящим углом, "
              "двери двадцати стилей, окна со ставнями и занавесками, ажурные "
              "лестницы, мосты с перилами, фонари и праздничный декор.",
              "Кровельный молоток меняет форму уже поставленной крыши, "
              "плоскогубцы снимают перила с моста, ключ запирает ставни.",
          ],
          tasks=[item("mcwroofs:oak_roof"), item("mcwroofs:roofing_hammer"),
                 item("mcwwindows:window_base")],
          rewards=loot(("mcwroofs:oak_roof", 32), ("mcwlights:wall_lantern", 8), xp=200)),

        Q("styles", "Style Colonies", "minecolonies:blockhuttownhall", 3, 1,
          text=[
              "Десять новых архитектурных стилей для колонии: Аквática, "
              "Стимпанк, Фронтир, Античность, Багровая крепость, Подводная база, "
              "Улей, Порча, Тропики и Сказка.",
              "Больше четырёх тысяч чертежей. Колония перестаёт выглядеть "
              "одинаково у всех.",
          ],
          tasks=[check("Выбрать новый стиль при постройке колонии")],
          rewards=loot(("minecolonies:blockhutcitizen", 2), xp=200)),
    ],
)

chapter(
    "tech2_newage", "tech2", 60, "Create: New Age", "create_new_age:generator_coil",
    "Электричество, тепло и ядерный реактор для Create",
    [
        "Create Addition даёт простые генераторы. Create: New Age идёт дальше — "
        "к магнитам, катушкам, моторам и настоящему ядерному реактору, который "
        "плавится, если забыть про охлаждение.",
        "Обе ветки работают на одной энергии, так что выбирать не нужно: "
        "берите из каждой то, что удобнее.",
    ],
    chain([
        Q("coil", "Катушка генератора", "create_new_age:generator_coil", 0, 0,
          text=[
              "Восемь медных слитков вокруг блока андезитового сплава. Катушка "
              "превращает вращение в электричество, но только если вокруг "
              "стоят магниты.",
              "Сила магнита решает всё: магнетит даёт единицу, незеритовый — "
              "двадцать четыре. Угольные щётки снимают ток с восьми катушек сразу.",
          ],
          tasks=[item("create_new_age:generator_coil"), item("create_new_age:carbon_brushes"),
                 item("create_new_age:magnetite_block", 4)],
          rewards=loot(("minecraft:copper_ingot", 32), xp=150)),

        Q("energiser", "Энергайзер", "create_new_age:basic_energiser", 0, 1,
          text=[
              "Он «перезаряжает» предметы на депоте под собой. Железо за тысячу "
              "единиц становится перегруженным, золото за две тысячи, алмаз "
              "за десять.",
              "Перегруженные материалы идут в моторы, провода и всё остальное.",
          ],
          tasks=[item("create_new_age:basic_energiser"), item("create_new_age:overcharged_iron", 8)],
          rewards=loot(("create_new_age:overcharged_iron", 8), xp=200)),

        Q("wires", "Провода", "create_new_age:copper_wire", 0, 2,
          text=[
              "Провод натягивается между двумя коннекторами на шестнадцать "
              "блоков. Медный тянет тысячу единиц в тик, алмазный — восемь тысяч.",
              "Проводка Create: New Age выглядит как настоящая ЛЭП и "
              "прокладывается так же.",
          ],
          tasks=[item("create_new_age:electrical_connector", 2),
                 item("create_new_age:copper_wire", 4)],
          rewards=loot(("create_new_age:copper_wire", 8), xp=150)),

        Q("motor", "Моторы", "create_new_age:basic_motor", 0, 3,
          text=[
              "Мотор превращает электричество обратно во вращение с настраиваемой "
              "скоростью. Базовый выдаёт пятьсот двенадцать единиц нагрузки, "
              "усиленный — восемь тысяч.",
              "Расширения позади мотора умножают его отдачу вдвое и втрое.",
          ],
          tasks=[item("create_new_age:basic_motor"), item("create_new_age:basic_motor_extension")],
          rewards=loot(("create_new_age:overcharged_gold", 4), xp=250)),

        Q("heat", "Тепло", "create_new_age:heat_pipe", 0, 4,
          text=[
              "Тепловые трубы разносят тепло, солнечные пластины его собирают, "
              "двигатель Стирлинга превращает в вращение.",
              "Нагреватель заменяет горелку ифрита под котлом Create — вместо "
              "угля он ест тепло.",
          ],
          tasks=[item("create_new_age:heat_pipe", 4), item("create_new_age:stirling_engine"),
                 item("create_new_age:heater")],
          rewards=loot(("create_new_age:heat_pipe", 8), xp=250)),

        Q("thorium", "Торий", "create_new_age:thorium", 0, 5,
          text=[
              "Ториевая руда, дроблением — радиоактивный торий, последовательной "
              "сборкой — ядерное топливо.",
              "Торий размножается в смесителе: камень, глина и вода удваивают "
              "запас. Топливо для реактора можно выращивать бесконечно.",
          ],
          tasks=[item("create_new_age:thorium", 8), item("create_new_age:nuclear_fuel")],
          rewards=loot(("create_new_age:thorium", 16), xp=300)),

        Q("reactor", "Ядерный реактор", "create_new_age:reactor_rod", 0, 6,
          text=[
              "Корпус, реакторное стекло, стержни, приёмник топлива и вентиляция. "
              "Каждый стержень даёт тридцать градусов в тик, и это тепло надо "
              "куда-то девать.",
              "Не отвели — расплавление: взрыв, кориум на месте реактора и "
              "радиация вокруг. Обшивайте корпусом и надевайте кожаную броню.",
          ],
          tasks=[item("create_new_age:reactor_casing", 16), item("create_new_age:reactor_rod", 2),
                 item("create_new_age:reactor_fuel_acceptor"),
                 item("create_new_age:reactor_heat_vent", 2)],
          rewards=loot(("create_new_age:overcharged_diamond", 4), xp=800)),
    ]),
)

chapter(
    "tech2_mektools", "tech2", 70, "Инструменты Mekanism", "mekanismtools:refined_obsidian_pickaxe",
    "Шесть материалов, которые обходят незерит",
    [
        "Mekanism Tools берёт металлы основного мода и делает из них полный "
        "набор инструментов, брони, щитов и пакселей.",
        "Смысл не в разнообразии, а в цифрах: два материала здесь честно лучше "
        "незерита, а один — самый быстрый инструмент в игре.",
    ],
    [
        Q("lapis", "Лазурит", "mekanismtools:lapis_lazuli_pickaxe", 0, 0,
          text=[
              "Прочность смешная, зато зачаровываемость тридцать два — вдвое "
              "выше золота.",
              "Это не рабочий инструмент, а способ выбить хорошие чары дёшево "
              "и перенести их наковальней на что-то приличное.",
          ],
          tasks=[item("mekanismtools:lapis_lazuli_pickaxe")],
          rewards=loot(("minecraft:lapis_block", 4), xp=100)),

        Q("glowstone", "Рафинированный светокамень", "mekanismtools:refined_glowstone_pickaxe", 1, 0,
          text=[
              "Скорость пятнадцать против девяти у незерита — самый быстрый "
              "инструмент в сборке. Прочности хватает ненадолго, но копает он "
              "как нож сквозь масло.",
              "Броня из него светится и, как золото, нравится пиглинам.",
          ],
          tasks=[item("mekanismtools:refined_glowstone_pickaxe")],
          rewards=loot(("minecraft:glowstone", 16), xp=150)),

        Q("osmium", "Осмий", "mekanismtools:osmium_paxel", 0, 1,
          text=[
              "Тысяча слитков прочности и урон плюс четыре — по урону осмий "
              "уже на уровне незерита, а медлительность компенсируется "
              "чарами эффективности.",
              "Паксель объединяет кирку, топор и лопату: один слот вместо трёх.",
          ],
          tasks=[item("mekanismtools:osmium_paxel"), adv("mekanismtools:paxel")],
          rewards=loot(("mekanism:ingot_osmium", 16), xp=250)),

        Q("obsidian", "Рафинированный обсидиан", "mekanismtools:refined_obsidian_helmet", 0, 2,
          text=[
              "Четыре тысячи прочности, урон плюс восемь, тридцать одно очко "
              "защиты против двадцати у незерита и вязкость пять.",
              "Это лучшее обычное снаряжение сборки — до супремиума и "
              "MekaSuit ничего сравнимого нет.",
          ],
          tasks=[item("mekanismtools:refined_obsidian_helmet"),
                 item("mekanismtools:refined_obsidian_pickaxe"),
                 adv("mekanismtools:better_than_netherite")],
          rewards=loot(("mekanism:ingot_refined_obsidian", 8), xp=500)),

        Q("shield", "Щиты", "mekanismtools:osmium_shield", 1, 2,
          text=["Щит из любого материала мода. Обсидиановый держит тысячу "
                "шестьсот восемьдесят ударов против трёхсот тридцати шести "
                "у ванильного."],
          tasks=[item("mekanismtools:osmium_shield"),
                 adv("mekanismtools:not_enough_shielding")],
          rewards=loot(("mekanism:ingot_steel", 16), xp=200), optional=True),
    ],
)
