# -*- coding: utf-8 -*-
from dsl import chapter, Q, item, adv, check, chain

chapter(
    "rs_network", "storage", 10, "Refined Storage: сеть", "refinedstorage:controller",
    "Контроллер, кабели, диски и гриды",
    [],
    chain([
        Q("silicon", "Кремний и процессоры", "refinedstorage:silicon", 0, 0,
          text=["Кварц в кремний, кремний с железом или золотом в заготовку, заготовка "
                "в печь. Три уровня процессоров — расходник всей сети."],
          tasks=[item("refinedstorage:silicon", 8), item("refinedstorage:basic_processor", 4)]),
        Q("quartz_iron", "Кварцевое железо", "refinedstorage:quartz_enriched_iron", 0, 1,
          text=["Кварц и железо. Из него — кабели, корпуса, всё."],
          tasks=[item("refinedstorage:quartz_enriched_iron", 16)]),
        Q("controller", "Контроллер", "refinedstorage:controller", 0, 2,
          text=["Сердце. Принимает энергию, раздаёт всем, кто подключён. Одна сеть — один "
                "контроллер; чем больше устройств, тем больше он ест."],
          tasks=[item("refinedstorage:controller")],
          rewards=["Работающая сеть хранения"]),
        Q("cable", "Кабели и реле", "refinedstorage:cable", 0, 3,
          text=["Кабель соединяет. Реле включает и выключает участок по условию."],
          tasks=[item("refinedstorage:cable", 16), item("refinedstorage:relay")]),
        Q("drive", "Дисковод и диски", "refinedstorage:disk_drive", 0, 4,
          text=["Восемь дисков в один блок. Тысяча, четыре, шестнадцать, шестьдесят четыре "
                "тысячи предметов. Корпус позволяет разобрать диск обратно."],
          tasks=[item("refinedstorage:disk_drive"), item("refinedstorage:1k_storage_disk"),
                 item("refinedstorage:storage_housing")]),
        Q("grid", "Грид", "refinedstorage:grid", 0, 5,
          text=["Окно в сеть: поиск, сортировка, перенос. Крафтовый добавляет верстак, "
                "грид шаблонов пишет рецепты. Портативный — в кармане на батарее."],
          tasks=[item("refinedstorage:grid"), item("refinedstorage:crafting_grid")],
          rewards=["Единый доступ ко всему складу"]),
        Q("blocks_storage", "Блоки-хранилища", "refinedstorage:1k_storage_block", 1, 4,
          deps=["drive"],
          text=["Диск, ставший блоком. Без дисковода."],
          tasks=[item("refinedstorage:1k_storage_block")], optional=True),
        Q("external", "Внешнее хранилище", "refinedstorage:external_storage", 1, 5,
          deps=["grid"],
          text=["Сундук, бочка, хранилище Create, бак — всё становится частью сети. "
                "Дисковый интерфейс переливает между дисками."],
          tasks=[item("refinedstorage:external_storage"), item("refinedstorage:disk_interface")]),
        Q("io", "Импорт и экспорт", "refinedstorage:importer", 0, 6,
          text=["Импортёр забирает, экспортёр выдаёт по фильтру, интерфейс — в обе стороны. "
                "Улучшения: скорость, стопка, регулятор, шёлк, удача."],
          tasks=[item("refinedstorage:importer"), item("refinedstorage:exporter"), item("refinedstorage:interface"),
                 item("refinedstorage:speed_upgrade"), item("refinedstorage:stack_upgrade")]),
        Q("constructor", "Конструктор и деструктор", "refinedstorage:constructor", 1, 6,
          text=["Конструктор ставит блоки из сети в мир, деструктор ломает и складывает "
                "обратно. Стена, которая строит себя."],
          tasks=[item("refinedstorage:constructor"), item("refinedstorage:destructor")]),
        Q("monitor", "Монитор и детектор", "refinedstorage:storage_monitor", 2, 6,
          text=["Число на блоке. Сигнал по порогу."],
          tasks=[item("refinedstorage:storage_monitor"), item("refinedstorage:detector")]),
        Q("wireless", "Беспроводной доступ", "refinedstorage:wireless_grid", 0, 7,
          text=["Передатчик даёт покрытие, грид открывает сеть отовсюду. Сетевые передатчик "
                "и приёмник связывают сегменты — даже между измерениями."],
          tasks=[item("refinedstorage:wireless_transmitter"), item("refinedstorage:wireless_grid"),
                 item("refinedstorage:network_transmitter"), item("refinedstorage:network_receiver")]),
        Q("security", "Безопасность", "refinedstorage:security_manager", 1, 7,
          text=["Кому что можно."],
          tasks=[item("refinedstorage:security_manager"), item("refinedstorage:security_card")], optional=True),
    ]),
)

chapter(
    "rs_autocraft", "storage", 20, "Refined Storage: автокрафт", "refinedstorage:autocrafter",
    "Шаблоны, автокрафтеры и цепочки производства",
    [
        "Автокрафт — момент, когда сеть перестаёт быть складом и становится собеседником. "
        "Вы просите «сто прецизионных механизмов», она считает дерево из сорока рецептов, "
        "находит, чего не хватает, и делает. Вам остаётся ждать.",
    ],
    chain([
        Q("pattern_grid", "Грид шаблонов", "refinedstorage:pattern_grid", 0, 0,
          text=["Рецепт записывается на шаблон. Верстак, печь, дробилка, любая машина "
                "с фильтром — всё можно описать."],
          tasks=[item("refinedstorage:pattern_grid"), item("refinedstorage:pattern", 8)]),
        Q("autocrafter", "Автокрафтер", "refinedstorage:autocrafter", 0, 1,
          text=["Хранит шаблоны, исполняет. Для машин — выдаёт компоненты соседу и ждёт "
                "результата."],
          tasks=[item("refinedstorage:autocrafter")],
          rewards=["Автоматическое производство по запросу"]),
        Q("manager", "Менеджер шаблонов", "refinedstorage:autocrafter_manager", 0, 2,
          text=["Все шаблоны в одном списке; дубли и конфликты видно сразу."],
          tasks=[item("refinedstorage:autocrafter_manager")]),
        Q("monitor_craft", "Монитор автокрафта", "refinedstorage:autocrafting_monitor", 1, 2,
          text=["Что делается, что ждёт, что застряло."],
          tasks=[item("refinedstorage:autocrafting_monitor")]),
        Q("upgrade_craft", "Крафт по требованию", "refinedstorage:autocrafting_upgrade", 0, 3,
          text=["В экспортёре или интерфейсе: нет предмета — сеть делает его сама. "
                "Так держат запас, о котором не думают."],
          tasks=[item("refinedstorage:autocrafting_upgrade")]),
        Q("wireless_craft", "Беспроводной монитор", "refinedstorage:wireless_autocrafting_monitor", 1, 3,
          text=["Тот же монитор, в кармане."],
          tasks=[item("refinedstorage:wireless_autocrafting_monitor")], optional=True),
        Q("jei_rs", "Интеграция с JEI", "minecraft:bookshelf", 0, 4,
          text=["Из рецепта в JEI — сразу заказ в сеть. Грид подсвечивает, чего нет."],
          tasks=[check("Заказать крафт из JEI через грид")]),
        Q("big_project", "Большая цепочка", "refinedstorage:advanced_processor", 0, 5,
          deps=["upgrade_craft"],
          text=["Закажите восемь продвинутых процессоров одним щелчком. Кремний, золото, "
                "красный камень, заготовки, печь — если сеть собрала это сама, она настроена."],
          tasks=[item("refinedstorage:advanced_processor", 8)],
          rewards=["Полностью автоматизированное производство"]),
    ]),
)

chapter(
    "storage_local", "storage", 30, "Локальное хранение", "sophisticatedbackpacks:diamond_backpack",
    "Рюкзаки, сундуки и всё, что не требует сети",
    [],
    [
        Q("backpack_tiers", "Уровни рюкзаков", "sophisticatedbackpacks:diamond_backpack", 0, 0,
          text=["Медный, железный, золотой, алмазный, незеритовый. Каждый уровень — больше "
                "слотов и больше модулей, и ничего не теряется по дороге."],
          tasks=[item("sophisticatedbackpacks:iron_backpack"), item("sophisticatedbackpacks:gold_backpack")]),
        Q("backpack_auto", "Автоматизация в рюкзаке", "sophisticatedbackpacks:auto_smelting_upgrade", 1, 0,
          deps=["backpack_tiers"],
          text=["Плавка, обжиг, копчение на ходу. Верстак и наковальня внутри. Зельеварня. "
                "Сжатие руды в блоки. Рюкзак становится маленькой базой."],
          tasks=[item("sophisticatedbackpacks:auto_smelting_upgrade"), item("sophisticatedbackpacks:crafting_upgrade"),
                 item("sophisticatedbackpacks:compacting_upgrade")]),
        Q("backpack_filter", "Фильтры и насосы", "sophisticatedbackpacks:advanced_filter_upgrade", 2, 0,
          deps=["backpack_tiers"],
          text=["Фильтр отсеивает мусор, пустота его уничтожает, вклад сгружает в сундук, "
                "пополнение держит хотбар полным. Насос — жидкости, батарея — энергия."],
          tasks=[item("sophisticatedbackpacks:advanced_filter_upgrade"), item("sophisticatedbackpacks:void_upgrade"),
                 item("sophisticatedbackpacks:deposit_upgrade")]),
        Q("everlasting", "Неуничтожимый рюкзак", "sophisticatedbackpacks:everlasting_upgrade", 0, 1,
          deps=["backpack_tiers"],
          text=["Не горит и не исчезает. Страховка на случай лавы."],
          tasks=[item("sophisticatedbackpacks:everlasting_upgrade")], optional=True),
        Q("vault_create", "Хранилище Create", "create:item_vault", 1, 1,
          text=["Дёшево, много, и подключается к сети через внешнее хранилище. Склад сырья "
                "до настоящей сети."],
          tasks=[item("create:item_vault", 8)]),
        Q("bins", "Бины Mekanism", "mekanism:basic_bin", 2, 1,
          text=["Один предмет, но очень много. Булыжник, дерево, руда."],
          tasks=[item("mekanism:basic_bin")]),
        Q("rack", "Стойки колонии", "minecolonies:blockminecoloniesrack", 3, 1,
          text=["Склад колонии — тоже внешнее хранилище для сети."],
          tasks=[item("minecolonies:blockminecoloniesrack")], optional=True),
    ],
)
