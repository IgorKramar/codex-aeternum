# -*- coding: utf-8 -*-
from dsl import chapter, Q, item, adv, check, chain

chapter(
    "fd_kitchen", "life", 10, "Кухня", "farmersdelight:cooking_pot",
    "Farmer's Delight: ножи, доска, котелок и сковорода",
    [
        "Farmer's Delight превращает еду в отдельную систему. Готовые "
        "блюда дают эффект сытости — он не даёт голоду убывать какое-то "
        "время, что заметно удобнее ванильных стейков.",
    ],
    chain([
        Q("knife", "Нож", "farmersdelight:flint_knife", 0, 0,
          text=[
              "Нож режет ингредиенты на разделочной доске и служит "
              "лёгким оружием. Кремнёвый → железный → золотой → "
              "алмазный → незеритовый.",
          ],
          tasks=[item("farmersdelight:flint_knife"),
                 item("farmersdelight:iron_knife")]),

        Q("board", "Разделочная доска", "farmersdelight:cutting_board", 0, 1,
          text=[
              "Доска разбирает предметы: с ножа получаются нарезки мяса, "
              "с топора — доски, с киркой — щебень.",
              "Это же самый дешёвый способ снять шкуру и разделать тушу.",
          ],
          tasks=[item("farmersdelight:cutting_board")]),

        Q("pot", "Котелок", "farmersdelight:cooking_pot", 0, 2,
          text=[
              "Котелок варит супы и рагу на костре. Рецепт — до шести "
              "ингредиентов плюс ёмкость (миска, бутылка).",
              "Ставьте несколько котелков на один длинный костёр — "
              "получится кухня.",
          ],
          tasks=[item("farmersdelight:cooking_pot"),
                 item("farmersdelight:beef_stew")]),

        Q("skillet", "Сковорода", "farmersdelight:skillet", 1, 2,
          text=[
              "Сковорода жарит быстрее печи и работает прямо в руках, "
              "если под ней источник огня. Она же неплохое оружие "
              "с эффектом поджога.",
          ],
          tasks=[item("farmersdelight:skillet")]),

        Q("stove", "Плита", "farmersdelight:stove", 0, 3,
          text=["Плита жарит до шести предметов одновременно и "
                "показывает их на поверхности."],
          tasks=[item("farmersdelight:stove")]),

        Q("crops", "Новые культуры", "farmersdelight:tomato", 0, 4,
          text=[
              "Томаты, капуста, лук, рис. Дикие версии растут в "
              "соответствующих биомах — с них и начинают.",
              "Рис сажается на мелководье, помидоры требуют опоры.",
          ],
          tasks=[item("farmersdelight:tomato"), item("farmersdelight:cabbage"),
                 item("farmersdelight:onion"), item("farmersdelight:rice")]),

        Q("soil", "Богатая почва", "farmersdelight:rich_soil", 0, 5,
          text=[
              "Органический компост делается в компостере из "
              "органики, солома — из пшеницы. Богатая почва ускоряет "
              "рост и не требует полива.",
          ],
          tasks=[item("farmersdelight:organic_compost"),
                 item("farmersdelight:rich_soil")]),

        Q("feast", "Пиршество", "farmersdelight:roast_chicken_block", 0, 6,
          text=[
              "Блюда-пиршества ставятся на стол и кормят несколько "
              "игроков: жареная курица, пирог, окорок в мёде, "
              "запечённая треска.",
          ],
          tasks=[item("farmersdelight:roast_chicken_block"),
                 item("farmersdelight:honey_glazed_ham")],
          rewards=["Лучшая еда в сборке"]),

        Q("storage_fd", "Хранение продуктов", "farmersdelight:oak_cabinet", 1, 5,
          deps=["crops"],
          text=["Шкафы, корзины и ящики для урожая. Ящик сжимает "
                "девять единиц в один блок."],
          tasks=[item("farmersdelight:oak_cabinet")],
          optional=True),

        Q("rope", "Верёвка и подвешивание", "farmersdelight:rope", 2, 5,
          deps=["crops"],
          text=["Верёвка позволяет подвешивать предметы, а "
                "«вязанки» сушат урожай."],
          tasks=[item("farmersdelight:rope")],
          optional=True),
    ]),
)

chapter(
    "life_furniture", "life", 20, "Мебель и уют", "handcrafted:bench",
    "Handcrafted, Refurbished Furniture, Furnicraft и декор",
    [
        "В сборке три независимых мебельных мода плюс декоративные "
        "блоки Create, Domum Ornamentum и Eternal Tales. Вместе они "
        "закрывают любой интерьер.",
    ],
    [
        Q("handcrafted", "Handcrafted", "handcrafted:bench", 0, 0,
          text=[
              "Столы, стулья, скамьи, шкафы, тумбы и полки для всех "
              "пород дерева, а также посуда, подушки, простыни, "
              "трофеи мобов и настенные украшения.",
              "Отделочные планки (Trim) и угловые элементы дают "
              "аккуратные стыки стен.",
          ],
          tasks=[item("handcrafted:bench"), item("handcrafted:blue_cushion")]),

        Q("refurbished", "Refurbished Furniture", "refurbished_furniture:computer", 1, 0,
          text=[
              "Современная мебель: кухни с раковинами и шкафами, "
              "ванные комнаты, диваны, жалюзи, потолочные вентиляторы, "
              "почтовые ящики, телевизор и работающий компьютер.",
              "Многие предметы функциональны: раковина набирает воду, "
              "холодильник хранит еду, тостер жарит хлеб.",
          ],
          tasks=[item("refurbished_furniture:computer"),
                 item("refurbished_furniture:bath")]),

        Q("furnicraft", "Furnicraft", "minecraft:crafting_table", 2, 0,
          text=[
              "Furnicraft в этой сборке — датапак (ketket_furnitures). "
              "Мебель собирается на верстаке плотника из дерева, "
              "железа, шерсти и фонарей.",
              "Рецепты полностью описаны внутри самого датапака и "
              "видны в JEI.",
          ],
          tasks=[check("Собрать любую мебель Furnicraft")]),

        Q("domum", "Domum Ornamentum", "domum_ornamentum:architectscutter", 0, 1,
          text=[
              "Резак архитектора делает кирпич, черепицу, фахверк, "
              "панели, светильники, ковры и двери из любых материалов.",
              "Формально это библиотека MineColonies, но её блоки "
              "полезны в любом строительстве.",
          ],
          tasks=[item("domum_ornamentum:architectscutter")]),

        Q("create_deco2", "Декор Create", "create:copper_shingles", 1, 1,
          text=[
              "Медная черепица и плитка со всеми стадиями окисления, "
              "стекло в рамах, металлические балки, лестницы, "
              "скатерти, почтовые ящики и ламповые индикаторы.",
              "Copycat-блоки принимают вид любого другого блока.",
          ],
          tasks=[item("create:copper_shingles")]),

        Q("et_deco", "Декор Eternal Tales", "eternal_tales:soul_lava_lamp", 2, 1,
          text=[
              "Мод добавляет сотни блоков из каждого измерения: янтарные кирпичи, "
              "кометная древесина, эдемский камень, лава-лампы, вазы, картины "
              "и пластинки.",
              "Музей и витрины позволяют выставлять трофеи.",
          ],
          tasks=[item("eternal_tales:soul_lava_lamp")],
          optional=True),

        Q("comforts2", "Гамаки и мешки", "comforts:hammock_red", 0, 2,
          text=[
              "Гамак вешается на верёвку с гвоздём и пропускает день. "
              "Спальный мешок пропускает ночь, не меняя точку "
              "возрождения.",
          ],
          tasks=[item("comforts:rope_and_nail")]),

        Q("macaw", "Серия Macaw's", "mcwroofs:oak_roof", 1, 2,
          text=[
              "Семь модов одного автора закрывают то, чего в ванили нет совсем: крыши "
              "под настоящим углом, двери и калитки всех видов, окна со ставнями, "
              "лестницы и перила, мосты, фонари и праздничный декор.",
              "Крафтится всё из обычных материалов и стыкуется с любым стилем — "
              "от деревенского до промышленного.",
          ],
          tasks=[item("mcwroofs:oak_roof"), item("mcwdoors:oak_japanese_door"),
                 item("mcwwindows:oak_window")],
          optional=True),
    ],
)

chapter(
    "life_world", "world", 10, "Мир сборки", "minecraft:filled_map",
    "Terralith, компасы и дальняя прорисовка",
    [
        "Terralith переделывает мир целиком: настоящие горные хребты, каньоны, "
        "пещерные системы, оазисы и вулканы — больше сотни биомов.",
        "Lithostitched и TerraBlender следят, чтобы он не спорил с измерениями, "
        "которые добавляют остальные моды.",
    ],
    [
        Q("terralith", "Terralith", "minecraft:grass_block", 0, 0,
          text=[
              "Terralith меняет форму мира: настоящие горные хребты, "
              "каньоны, пещерные системы, оазисы и вулканы.",
              "Ванильные структуры и генерация руд сохраняются.",
          ],
          tasks=[check("Найти биом Terralith")]),

        Q("compass", "Компасы исследователя", "naturescompass:naturescompass", 1, 0,
          text=[
              "Nature's Compass ищет биом по названию, Explorer's Compass — структуру. "
              "Выбираете в списке, компас показывает направление и расстояние.",
              "В мире, где биомов больше сотни, а структур ещё больше, это не читерство, "
              "а способ не потратить вечер на поиски деревни.",
          ],
          tasks=[item("naturescompass:naturescompass"),
                 item("explorerscompass:explorerscompass")]),

        Q("dh", "Distant Horizons", "minecraft:spyglass", 2, 0,
          text=[
              "Distant Horizons рисует ландшафт далеко за границей "
              "прогрузки чанков, используя упрощённые модели.",
              "Данные копятся при исследовании и хранятся локально; "
              "первый проход по местности всегда самый долгий.",
          ],
          tasks=[check("Прочитано")]),

        Q("xaero", "Карты Xaero", "minecraft:filled_map", 0, 1,
          text=[
              "Мини-карта и полная карта ведутся автоматически. "
              "Точки, зоны, отслеживание существ и союзников "
              "настраиваются в меню карты.",
              "Better Party синхронизирует метки группы с обеими картами.",
          ],
          tasks=[check("Открыть полную карту (клавиша M)")]),

        Q("structures", "Структуры", "minecraft:chest", 1, 1,
          text=[
              "Помимо ванильных в мире генерируются: постройки "
              "Create (Structures Arise и Rustic Structures), "
              "деревни и башни Eternal Tales, подземелья Cataclysm, "
              "путевые камни и структуры Terralith.",
          ],
          tasks=[check("Найти любую модовую структуру")]),

        Q("waystones2", "Сеть путевых камней", "waystones:waystone", 2, 1,
          text=[
              "Камни, найденные в мире, активируются бесплатно. "
              "Свои камни ставятся где угодно. Общий камень "
              "(Sharestone) даёт доступ всей группе, портальный "
              "камень связывает две точки напрямую.",
              "Портальные свитки и варп-пыль позволяют перемещаться "
              "без камня.",
          ],
          tasks=[item("waystones:waystone"), item("waystones:sharestone"),
                 item("waystones:warp_dust")]),

        Q("lootr_world", "Личная добыча", "lootr:trophy", 0, 2,
          text=[
              "Lootr делает сундуки в структурах личными: каждый игрок открывает свой "
              "набор добычи. Крепость, разграбленная соседом час назад, для вас "
              "по-прежнему полна.",
          ],
          tasks=[check("Прочитано")]),

        Q("mobs", "Мобы сборки", "minecraft:zombie_head", 1, 2,
          text=[
              "Помимо ванильных в мире водятся сотни существ Eternal Tales, звери "
              "Alex's Mobs, боссы Cataclysm и Mowzie's Mobs, мутанты Mutant Monsters, "
              "налётчики MineColonies и обитатели Aether и Сумеречного леса.",
              "LetMeDespawn убирает лишних мобов, чтобы сервер "
              "не задыхался.",
          ],
          tasks=[check("Прочитано")]),
    ],
)
