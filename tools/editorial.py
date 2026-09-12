"""Проверенные исправления обучения; русский и английский хранятся рядом.

Источники: рецепты и теги установленной сборки (см. docs/content-sources.md).
Поправки не меняют ключи заданий и ручных отметок в старых сохранениях.
"""
PATCHES = {
 'start_first_day/wood': (
  ['Соберите 16 дубовых брёвен: часть пойдёт на инструменты, остальное — на верстак, сундук и топливо. Эта цель проверяет именно дуб; другие породы здесь не засчитываются.',
   'TreeChop меняет рубку деревьев. Если его поведение непонятно, проверьте настройки клавиш и мода; не рассчитывайте на одинаковую комбинацию клавиш во всех установках.'],
  ['Collect 16 oak logs for tools, a crafting table, a chest and fuel. This objective counts oak specifically; other wood species do not count.',
   'TreeChop changes tree felling. Check its settings and key bindings if the behaviour is unfamiliar; bindings can differ between installations.']),
 'create_basics/cogwheel': (
  ['Шестерни меняют направление и скорость вращения. В паре большая → малая выход вращается быстрее; малая → большая — медленнее. Вал передаёт вращение без изменения скорости.',
   'Ускорение машины увеличивает потребление нагрузки. Шестерни не создают дополнительную мощность источника: при перегрузке снизьте скорость или добавьте генерацию. Схемы зацепления посмотрите в Ponder.'],
  ['Cogwheels change rotation direction and speed. A large cog driving a small one speeds up the output; a small cog driving a large one slows it down. Shafts preserve speed.',
   'Faster machines consume more stress. Gearing does not create source capacity: reduce speed or add generation when overloaded. Ponder shows valid connections.']),
 'create_basics/waterwheel': (
  ['Поставьте колесо так, чтобы текущая вода приводила его во вращение, затем выведите вал к машине. Это постоянный источник для первых операций без расхода топлива.',
   'Перед подключением нескольких машин проверьте доступную нагрузку. Большое колесо и ветряк — варианты расширения; для прохождения приборов достаточно одного работающего источника.'],
  ['Place the wheel so flowing water turns it, then connect a shaft to a machine. It provides continuous rotation for early processing without fuel.',
   'Check available stress before adding machines. A large wheel and a windmill are expansion options; the instruments branch accepts either source.']),
 'create_basics/stress': (
  ['Подключите приборы к той же сети, что и рабочая машина. Спидометр показывает скорость, стрессометр — нагрузку относительно доступной мощности.',
   'Проверьте показания до и после подключения пресса. Если сеть остановилась, сначала уменьшите скорость потребителя. Источники воды, ветра и ручной привод здесь альтернативны.'],
  ['Connect both instruments to the same network as a working machine. The speedometer shows rotation speed; the stressometer compares load with available capacity.',
   'Compare readings before and after connecting a press. If the network stops, first lower the consumer speed. Water, wind and a hand crank are alternatives here.']),
 'create_andesite/casing': (
  ['Снимите кору с бревна топором и примените к нему андезитовый сплав. Полученный корпус нужен прессу, пиле и другим ранним механизмам.',
   'Начните с восьми корпусов для мастерской. Их изготовление можно автоматизировать применением предмета; обычное прессование досок корпус не создаёт.'],
  ['Strip a log with an axe and apply andesite alloy to it. Andesite casings are used by the press, saw and other early machines.',
   'Start with eight casings for a workshop. Item application can automate their production; pressing ordinary planks does not make casings.']),
 'create_andesite/press': (
  ['Поставьте пресс над депо или лентой, подключите вращение и подайте железные слитки. Заберите восемь железных листов — они нужны для вентиляторов и жидкостной техники.',
   'Депо удобно для пробной партии; лента с подачей и выгрузкой — для непрерывного производства. Результаты и тип обработки каждого рецепта проверяйте в JEI.'],
  ['Place a press over a depot or belt, connect rotation and supply iron ingots. Collect eight iron sheets for fans and fluid machinery.',
   'A depot is convenient for a test batch; a belt with input and output supports continuous production. Check JEI for each recipe and processing type.']),
 'create_andesite/millstone': (
  ['Жёрнов — первая мельница для зерна и других совместимых материалов. Подведите вращение, загрузите пшеницу и заберите муку.',
   'Не обещайте себе удвоение любой руды: доступные входы и выходы зависят от рецепта. Для дробления руды предусмотрена отдельная ветка дробильных колёс.'],
  ['The millstone is an early mill for grain and other supported materials. Supply rotation, insert wheat and collect flour.',
   'Do not assume every ore can be doubled: supported inputs and yields depend on the recipe. Crushing wheels have their own ore-processing branch.']),
 'create_andesite/fan': (
  ['Среда перед вентилятором определяет обработку: вода — промывка, лава — обжиг, огонь или костёр — копчение, огонь душ — преобразование. Обычный лёд не включает заморозку.',
   'Подведите вращение и удерживайте предметы в обработанном потоке достаточно долго. Начните с одного рецепта из JEI, прежде чем подключать общий склад: неподходящие предметы в горячем потоке можно потерять.'],
  ['The catalyst in front of a fan selects processing: water washes, lava blasts, fire or a campfire smokes, and soul fire haunts. Ordinary ice does not enable freezing.',
   'Provide rotation and keep items in the processed airflow long enough. Test one JEI recipe before connecting general storage: unsuitable items in a hot airflow can be destroyed.']),
 'create_andesite/belt': (
  ['Соединитель из сушёной ламинарии связывает два подходящих вала в ленту. Он является предметом для установки; внутренние сегменты ленты отдельно добывать не нужно.',
   'Сначала соедините подачу, одну машину и выходной сундук. Проверьте направление движения и не перегружайте выход: задержка разгрузки остановит всю линию.'],
  ['A connector made from dried kelp links two suitable shafts into a belt. The connector is the placement item; internal belt segments are not an inventory goal.',
   'Connect an input, one machine and an output chest first. Check direction and output capacity: blocked unloading stops the entire line.']),
 'create_brass/precision': (
  ['Прецизионный механизм делается последовательной сборкой золотого листа: малая шестерня, большая шестерня, железный самородок. В этой версии последовательность повторяется пять раз.',
   'Верните незавершённую заготовку на вход и отделяйте готовый механизм от побочных результатов. Заложите запас расходников: выход не гарантирован. Механическая рука открывается после механизма, а не требуется для его первого изготовления.'],
  ['A precision mechanism starts with a golden sheet: apply a small cogwheel, a large cogwheel and an iron nugget. This version repeats the sequence five times.',
   'Return unfinished assemblies to the input and separate finished mechanisms from other results. Budget spare ingredients because success is not guaranteed. The mechanical arm follows the first mechanism; it is not required to make one.']),
 'create_brass/arm': (
  ['Механическая рука переносит предметы между выбранными точками. Для её изготовления нужен прецизионный механизм, поэтому сначала запустите последовательную сборку.',
   'Укажите источники и получателей до установки руки, затем подключите вращение. Проверьте цикл на небольшом запасе предметов: пустой источник и заполненный получатель требуют обработки в вашей схеме.'],
  ['A mechanical arm transfers items between selected points. Its recipe requires a precision mechanism, so establish sequenced assembly first.',
   'Select sources and destinations before placing the arm, then connect rotation. Test with a small batch and account for empty sources and full destinations.']),
 'mek_ore/enrichment': (
  ['Обогатительная камера подготавливает сырьё для плавки и делает обогащённые материалы для инфузера. Соедините её выход с электрической печью, задав стороны ввода и вывода.',
   'Множитель ×2 относится к рецептам блоков руды. Сырое сырьё и блоки сырья имеют другие соотношения; сравнивайте конкретный рецепт в JEI, а не переносите множитель на любой вход.'],
  ['The enrichment chamber prepares material for smelting and makes enriched infusing ingredients. Connect its output to an energized smelter and configure both machines’ sides.',
   'The ×2 label applies to ore-block recipes. Raw materials and raw blocks have different ratios; compare the actual JEI recipe instead of applying one multiplier to every input.']),
 'mek_ore/evaporation': (
  ['Первая испарительная установка превращает воду в рассол; вторая — рассол в жидкий литий. В установленной версии базовое соотношение обоих рецептов — 10 к 1.',
   'Рассол нужен для цепочки хлора, литий — для дальнейшего топлива. Серная кислота и тяжёлая вода производятся другими процессами. Проверьте температуру, вход жидкости и свободный выход перед увеличением установки.'],
  ['One thermal evaporation plant converts water into brine; another converts brine into liquid lithium. Both installed recipes have a base ratio of 10 to 1.',
   'Brine feeds the chlorine chain and lithium feeds later fuel production. Sulfuric acid and heavy water use different processes. Check temperature, fluid input and output space before expanding.']),
 'mek_power/gas_gen': (
  ['Камера реакции производит этилен из биотоплива, воды и водорода. Субстрат получается побочным продуктом, а не подаётся в этот рецепт.',
   'Подавайте этилен в газовый генератор и предусмотрите отдельный выход субстрата. Если камера перестала работать, проверьте все входы и свободное место под побочный продукт, прежде чем строить второй генератор.'],
  ['A pressurized reaction chamber produces ethene from bio fuel, water and hydrogen. Substrate is an output of this recipe, not an input.',
   'Feed ethene to the gas-burning generator and provide a separate substrate output. If the chamber stops, check every input and byproduct space before adding another generator.']),
 'story_forge/source': (
  ['Это подтверждение ветки ветряка. Подключите стрессометр и оцените запас нагрузки перед переработкой материалов.',
   'Для следующего этапа достаточно этого задания или подтверждения водяного колеса. Проходить оба источника не требуется.'],
  ['This confirms the windmill branch. Connect a stressometer and check spare capacity before processing materials.',
   'The next stage accepts this quest or the water-wheel confirmation. Completing both sources is not required.']),
 'story_forge/source_w': (
  ['Это подтверждение ветки водяного колеса. Подключите стрессометр к рабочему валу.',
   'Дальше можно перейти к переработке с одним источником. Вторую ветку оставьте для расширения мощности, если она понадобится.'],
  ['This confirms the water-wheel branch. Connect a stressometer to the working shaft.',
   'One source is enough to continue to processing. The other branch remains available if you later need more capacity.']),
 'story_forge/mill': (
  ['Дешёвая производственная ветка — переработка зерна. Подведите вращение к жёрнову, подавайте пшеницу и забирайте муку.',
   'Сдайте партию муки, когда производство налажено. Это расходуемая поставка; предметы будут списаны. Ветка дробильных колёс — альтернативный путь к следующему этапу.'],
  ['The inexpensive production route processes grain. Supply rotation and wheat to a millstone and collect flour.',
   'Deliver a batch of flour once production is established. Delivery consumes the items. The crushing-wheel branch is an alternative route to the next stage.']),
 'story_forge/wheels': (
  ['Дробильные колёса открывают переработку руды и камня. Для них потребуется латунная техника и механические крафтеры; эту ветку можно пройти позже мельницы.',
   'Накопите дроблёное железо по доступному рецепту JEI. Поставка подтверждает наличие партии, а работу самой установки вы проверяете в мире.'],
  ['Crushing wheels open ore and stone processing. They require brass technology and mechanical crafters; this branch can follow the earlier mill.',
   'Produce crushed iron using an available JEI recipe. Delivery proves that you have the batch; inspect the actual installation in the world.']),
 'story_forge/boiler': (
  ['Соберите паровую установку: соединённые баки, источник тепла, непрерывная подача воды и двигатели. Состояние котла определяется сразу несколькими условиями; увеличение одного параметра не исправляет остальные.',
   'Проверьте показатели котла и доступную нагрузку. Цель считает детали в инвентаре; она не измеряет уровень котла и не подтверждает его работу автоматически.'],
  ['Build a steam setup with connected tanks, heat, continuous water and engines. Boiler performance depends on several conditions; increasing one does not fix the others.',
   'Inspect boiler statistics and available stress. This objective counts inventory components; it does not automatically measure boiler level or operation.']),
}


def revise(chapters, translations):
    for c in chapters:
        for q in c['quests']:
            gid = c['id']+'/'+q['id']
            if gid in PATCHES:
                ru, en = PATCHES[gid]
                q['text'] = list(ru)
                translations[c['id']]['quests'][q['id']]['text'] = list(en)
            if gid == 'start_first_day/wood':
                q['tasks'][0].pop('note', None)
            if gid == 'mek_nuclear/fuel':
                q['tasks'] = [t for t in q['tasks'] if t['id'] != 'mekanism:solar_neutron_activator']
                for identifier in ['mekanism:chemical_oxidizer', 'mekanism:chemical_infuser', 'mekanism:chemical_dissolution_chamber']:
                    q['tasks'].append({'type':'item', 'id':identifier, 'count':1})
            if gid == 'create_andesite/millstone':
                q['tasks'][1]['id'] = 'create:wheat_flour'
                q['rewards']['text'] = []
            if gid == 'story_forge/mill':
                q['tasks'][0]['id'] = 'create:wheat_flour'
                q['tasks'][0]['count'] = 32
                q['rewards'] = {'items': [{'id':'minecraft:bread','count':16}], 'xp':40, 'text':[]}
                q['title'] = 'Мельница: партия муки'
                translations[c['id']]['quests'][q['id']]['title'] = 'Mill: a batch of flour'
            if gid == 'story_forge/wheels':
                q['title'] = 'Дробление: партия железа'
                translations[c['id']]['quests'][q['id']]['title'] = 'Crushing: a batch of iron'

PATCHES.update({
 'create_packages/cardboard': (
  ['Смешайте четыре порции бамбука, сахарного тростника или саженцев с 250 mB воды в чаше. Полученную целлюлозу обработайте механическим прессом — получится картон.', 'Подведите воду и растительное сырьё до строительства упаковочной линии. Бумага под прессом этот рецепт не заменяет.'],
  ['Mix four portions of bamboo, sugar cane or saplings with 250 mB of water in a basin. Press the resulting pulp into cardboard.', 'Supply water and plant material before building the packaging line. Pressing paper is not a substitute for this recipe.']),
 'create_trains/sturdy': (
  ['Прочный лист начинается с обсидиановой пыли. Залейте заготовку 500 mB лавы через разливщик, затем дважды обработайте прессом.', 'Для линии нужны подача лавы и последовательный проход через три операции. Отделите готовые листы от заготовок и накопите запас для железнодорожной техники.'],
  ['Start a sturdy sheet with obsidian dust. Fill the workpiece with 500 mB of lava using a spout, then press it twice.', 'Supply lava and route the workpiece through the three operations in order. Separate finished sheets from workpieces and stock them for railway machinery.']),
 'create_fluids/chocolate': (
  ['Для 250 mB шоколада смешайте сахар, какао-бобы и 250 mB молока в нагретой чаше.', 'Слив извлекает из бутылочки 250 mB мёда и возвращает стеклянную бутылку. Предусмотрите оба выхода — жидкий продукт и пустую тару.'],
  ['Mix sugar, cocoa beans and 250 mB of milk in a heated basin to make 250 mB of chocolate.', 'An item drain empties a honey bottle into 250 mB of honey and returns the glass bottle. Provide outputs for both liquid and empty containers.']),
 'rs_network/silicon': (
  ['Заготовке процессора нужны кремний, красная пыль, связка и материал уровня: железо для базового, золото для улучшенного, алмаз для продвинутого. Две нити и слизь дают восемь связок.', 'Обожгите заготовку в печи. Для автокрафта понадобятся отдельные шаблоны изготовления заготовки и её обработки.'],
  ['A raw processor needs silicon, redstone, a binding and its tier material: iron for basic, gold for improved, diamond for advanced. Two strings and a slimeball make eight bindings.', 'Smelt the raw processor. Autocrafting needs separate patterns for crafting and processing.']),
 'rs_autocraft/big_project': (
  ['Закажите восемь продвинутых процессоров. Сеть должна собрать заготовки из алмазов, кремния, красной пыли и связок, передать их в печь и вернуть готовые процессоры.', 'Отдельно настройте возврат из печи: выдача ингредиентов не завершает заказ. Проверьте результат в гриде, а зависшую задачу — в мониторе крафта.'],
  ['Request eight advanced processors. The network must craft raw processors from diamonds, silicon, redstone and bindings, send them to a furnace and retrieve the finished processors.', 'Configure furnace output separately: delivering ingredients does not complete the job. Check results in the grid and stalled jobs in the crafting monitor.']),
 'mek_start/steel': (
  ['Дважды обработайте железо углеродом: первый проход даёт обогащённое железо, второй — стальную пыль. Только после этого переплавьте пыль в слиток.', 'Обоим проходам нужен углерод. При расширении используйте два инфузера, чтобы не смешивать промежуточное сырьё. Совместимость стали других модов определяется тегами конкретного рецепта.'],
  ['Infuse iron with carbon twice: first enriched iron, then steel dust. Only then smelt the dust into an ingot.', 'Both passes need carbon. Use two infusers when expanding to keep intermediate materials separate. Steel compatibility is determined by each recipe’s tags.']),
 'mek_ore/purification': (
  ['С кислородом камера очистки получает три железных комка из блока руды или два из единицы сырого железа.', 'Комки идут в дробилку, грязная пыль — в обогатитель, чистая — в печь. Одной камеры очистки недостаточно для готовых слитков; сохраните предыдущую линию.'],
  ['With oxygen, the purification chamber makes three iron clumps per ore block or two per raw iron.', 'Crush the clumps, enrich the dirty dust and smelt the clean dust. The chamber alone does not produce ingots; keep the previous processing line.']),
 'mek_ore/injection': (
  ['Хлороводород позволяет получить четыре осколка из блока железной руды или восемь из трёх единиц сырого железа.', 'Осколкам ещё нужны очистка кислородом, дробление, обогащение и плавка. Добавьте инъекционную камеру перед существующей линией и обеспечьте непрерывную подачу химикатов.'],
  ['Hydrogen chloride yields four shards per iron ore block or eight per three raw iron.', 'Shards still need oxygen purification, crushing, enrichment and smelting. Add the injection chamber before the existing line and supply chemicals continuously.']),
 'mek_ore/dissolution': (
  ['Серная кислота превращает блок железной руды в 1000 mB грязной суспензии, а три единицы сырого железа — в 2000 mB. Промойте её: каждые 200 mB чистой суспензии дают один кристалл.', 'Дальше следуют инъекция хлороводорода, очистка кислородом, дробление, обогащение и плавка. Выход — пять слитков из блока руды или десять из трёх единиц сырого железа.'],
  ['Sulfuric acid turns one iron ore block into 1000 mB of dirty slurry, or three raw iron into 2000 mB. Wash it: each 200 mB of clean slurry produces one crystal.', 'Continue with hydrogen chloride injection, oxygen purification, crushing, enrichment and smelting. The yield is five ingots per ore block or ten per three raw iron.']),
 'mek_ore/crusher_mek': (
  ['Дробилка превращает железные слитки в пыль. Комбайнер восстанавливает блок железной руды из восьми единиц сырого железа и булыжника.', 'Восстановление блока расходует сырьё. Это не бесплатный замкнутый цикл и не обязательная операция при обогащении.'],
  ['The crusher turns iron ingots into dust. The combiner reconstructs an iron ore block from eight raw iron and cobblestone.', 'Reconstructing ore consumes material. It is not a free closed loop or a required enrichment step.']),
 'mek_nuclear/fuel': (
  ['Обогатите урановый слиток в жёлтый кек, окислите его до оксида урана. Отдельно растворите флюорит в серной кислоте для получения плавиковой кислоты.', 'Химический инфузер соединяет кислоту с оксидом урана в гексафторид; изотопная центрифуга превращает его в делящееся топливо. Солнечный нейтронный активатор нужен другой цепочке.'],
  ['Enrich uranium into yellow cake and oxidize it into uranium oxide. Separately dissolve fluorite in sulfuric acid to obtain hydrofluoric acid.', 'A chemical infuser combines the acid and uranium oxide into uranium hexafluoride; an isotopic centrifuge makes fissile fuel. The solar neutron activator belongs to another chain.']),
 'mek_nuclear/fusion': (
  ['Термоядерному реактору нужны дейтерий и тритий. Дейтерий получают из тяжёлой воды, а тритий — из лития в солнечном нейтронном активаторе.', 'Разделите производство двух компонентов и проверьте их стабильную подачу до запуска. Затем подготовьте хольраум и лазерную систему по руководству реактора.'],
  ['Fusion requires deuterium and tritium. Deuterium comes from heavy water; tritium comes from lithium in a solar neutron activator.', 'Separate the two fuel chains and verify sustained supply before startup. Then prepare the hohlraum and laser system using the reactor guide.']),
 'et_sorcery/matrix': (
  ['Рунная матрица — зачарование, увеличивающее выпадение рун из рунных камней и получаемые очки колдовства.', 'Полный комплект рунической брони тоже усиливает сбор рун. Эти улучшения полезны для заготовки сырья перед дальнейшим колдовством; отдельного станка «матрица» здесь нет.'],
  ['Runic Matrix is an enchantment that increases rune drops and Sorcery points from Rune Stones.', 'A full set of Runic Armor also improves rune harvesting. These upgrades help supply later sorcery; there is no separate matrix machine here.']),
 'et_darkness/super': (
  ['Здесь два отдельных достижения: активация Super Duper Darkness и победа над Унахзаалом на особых условиях.', 'Для особой победы описание достижения требует Eternal Darkness, Кольцо бедствия и человечность −5000. Одна активация усиленной Тьмы не заменяет эти условия.'],
  ['This quest contains two separate advancements: activating Super Duper Darkness and defeating Unahzaal under special conditions.', 'The special victory requires Eternal Darkness, a Calamity Ring and −5000 Humanity according to its advancement description. Activating the stronger darkness mode alone is not enough.']),
})
