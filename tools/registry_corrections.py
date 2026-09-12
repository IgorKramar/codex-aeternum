"""Поправки по реестру предметов и ресурсам JAR установленной сборки.

Внутренние блоки не становятся предметными целями. Ручные проверки
описывают наблюдаемый результат и не выдают инвентарь за работающую машину.
"""
from dsl import item


ITEM_REPLACEMENTS = {
    'createbigcannons:cannon_cast': 'createbigcannons:small_cast_mould',
    'createbigcannons:cannon_drill_bit': 'create:piston_extension_pole',
    'minecolonies:sceptergold': 'structurize:sceptergold',
    'create:large_bogey': 'create:railway_casing',
    'railways:conductor_cap': 'railways:blue_conductor_cap',
    'createaddition:accumulator': 'createaddition:modular_accumulator',
    'createaddition:liquid_blaze_burner': 'createaddition:straw',
    'refurbished_furniture:bath': 'refurbished_furniture:white_bath',
    'waystones:sharestone': 'waystones:blue_sharestone',
    'irons_spellbooks:arcane_debris': 'irons_spellbooks:arcane_essence',
    'railways:generic_crossing': 'create:track',
    'treechop:chopped_log': 'minecraft:iron_axe',
}

# Русский и английский текст находятся рядом, чтобы механика не расходилась.
TEXT = {
    'cbc_foundry/cast': (
        ['Выпилите малую модель формы из бревна механической пилой. Моделью создают слой литейной формы; сама форма существует в мире и не выдаётся отдельным предметом.',
         'Подготовьте литейный песок, соберите форму по Ponder и заполните расплавом. После застывания снимите оболочку: перед стрельбой полученную заготовку ещё нужно рассверлить.'],
        ['Cut a small cast mould from a log with a mechanical saw. Use the mould to construct a cast layer; the cast itself exists in the world and is not an inventory item.',
         'Prepare casting sand, build the cast as shown in Ponder and fill it with molten metal. Remove the casing after solidification; the resulting blank still needs boring before use.']),
    'cbc_foundry/drill': (
        ['Сверлильному станку нужны вращение, удлинители поршня и вода. Буровая головка — часть установленного механизма, отдельного предмета для неё нет.',
         'Закрепите литую заготовку на вращающейся установке по Ponder. Скорость сверла должна быть не ниже скорости заготовки; при остановке проверьте воду и вращение. Получите рассверленный чугунный ствол.'],
        ['The cannon drill needs rotation, piston extension poles and water. Its drill bit is part of the placed mechanism, not a separate inventory item.',
         'Mount a cast blank on a rotating assembly as shown in Ponder. Run the drill at least as fast as the workpiece; check water and rotation if it stops. Obtain a bored cast iron cannon barrel.']),
    'radar/misc_radar': (
        ['Бинокль позволяет вручную наводить орудия, подключённые к сетевому контроллеру. Привяжите его к контроллеру: присядьте и нажмите правой кнопкой по блоку.',
         'Приблизьте изображение и удерживайте левую кнопку, указывая точку наведения. Проверьте результат на безопасной мишени без боеприпасов.'],
        ['Binoculars manually aim guns connected to a network controller. Sneak and right-click the controller to pair them.',
         'Zoom in and hold the left mouse button to designate the aiming point. Test against a safe target with unloaded guns.']),
    'mc_found/buildtool': (
        ['Инструмент строительства относится к Structurize, который используется MineColonies. Выберите проект, проверьте высоту и поворот предварительного вида, затем подтвердите размещение.',
         'Строительные очки помогают осматривать проект. После размещения оформите заказ на строительство в интерфейсе хижины и обеспечьте строителя материалами; один предварительный вид работу не запускает.'],
        ['The Build Tool belongs to Structurize, which MineColonies uses. Select a blueprint, check preview height and rotation, then confirm placement.',
         'Build goggles help inspect the blueprint. After placement, request construction through the hut interface and supply the builder; a preview alone does not start the job.']),
    'create_trains/bogey': (
        ['Откройте сборку поезда на станции и примените железнодорожный корпус к пути внутри зоны сборки: появится тележка. Она создаётся на рельсах и не является отдельным предметом.',
         'Установите две тележки на одной прямой в зоне сборки. Проверьте их положение, прежде чем приклеивать корпус вагона. Кодекс автоматически проверяет только запас корпусов; установку тележек отметьте вручную.'],
        ['Enter train assembly at a station and use a railway casing on track inside the assembly area to place a bogey. Bogeys are created on the rails and are not separate inventory items.',
         'Place two bogeys on the same straight track within the assembly area. Check their positions before gluing the carriage body. The Codex checks the casing stock automatically; confirm placed bogeys manually.']),
    'create_trains/snr_conductor': (
        ['Синяя фуражка делается последовательной сборкой синей шерсти: резка, установка прецизионного механизма и нити. Примените готовую фуражку к андезитовому корпусу, чтобы создать кондуктора.',
         'Это отдельное существо Steam ’n’ Rails. Посадите его у управления составом и выдайте расписание. Здесь проверяется именно синяя фуражка; свисток подготовьте для работы с кондуктором.'],
        ['Make a blue cap by sequenced assembly of blue wool: cut it, then deploy a precision mechanism and string. Use the finished cap on an andesite casing to construct a conductor.',
         'This is a separate Steam ’n’ Rails entity. Seat it at the train controls and give it a schedule. This objective counts blue caps specifically; prepare a conductor whistle as well.']),
    'ca_electric/accumulator': (
        ['Модульный аккумулятор хранит FE между генератором и потребителями. Рецепт использует латунный корпус, конденсаторы, медный стержень и электрумовую проволоку.',
         'Подключите аккумулятор к сети и сравните заряд при работающем генераторе и после его остановки. Несколько модулей расширяют хранилище в пределах правил сборки мультиблока; наличие блока в инвентаре ещё не подтверждает зарядку.'],
        ['A modular accumulator buffers FE between generators and consumers. Its recipe uses a brass casing, capacitors, a copper rod and electrum wire.',
         'Connect it to the network and compare stored energy with the generator running and stopped. Additional modules expand storage within the multiblock assembly rules; owning a block does not prove that it charges.']),
    'ca_electric/burner': (
        ['Прокатайте бумагу или бамбук, чтобы получить трубочку. Примените её к горелке с ифритом: установленная горелка сможет принимать жидкое топливо из ведра или труб.',
         'Подготовьте ведро биоэтанола и проверьте нагрев чаши. Это доработка обычной горелки, а не отдельный предмет для крафта. Подачу топлива и нагрев Кодекс не измеряет автоматически.'],
        ['Roll paper or bamboo into a straw. Apply it to a blaze burner so the placed burner can accept liquid fuel from buckets or pipes.',
         'Prepare a bucket of bioethanol and check basin heating. This modifies a regular burner; it is not a separate craftable burner item. The Codex does not automatically measure fuel flow or heating.']),
    'life_furniture/refurbished': (
        ['Соберите компьютер и белую ванну для домашней мастерской. Белая ванна делается на верстаке Refurbished Furniture из деревянной ванны и белого красителя.',
         'Эта задача проверяет конкретно белый вариант. Разместите мебель так, чтобы оставался проход; питание и функции техники настраиваются отдельно.'],
        ['Prepare a computer and a white bath for your home workshop. Craft the white bath at the Refurbished Furniture workbench using a wooden bath and white dye.',
         'This objective counts the white variant specifically. Leave a clear walkway when furnishing the room; configure appliance power and functions separately.']),
    'more_home/bed': (
        ['Подготовьте красную кровать, две синие подушки Handcrafted и белую ванну Refurbished Furniture для спальни с ванной комнатой.',
         'Цели проверяют эти конкретные цвета. Для белой ванны перекрасьте деревянную на мебельном верстаке; расположите её в отдельной зоне, сохранив проход к кровати.'],
        ['Prepare a red bed, two blue Handcrafted cushions and a white Refurbished Furniture bath for a bedroom with a bathroom.',
         'The objectives count these specific colours. Recolour a wooden bath at the furniture workbench; place it in a separate area with a clear route to the bed.']),
    'life_world/waystones2': (
        ['Обычный путевой камень добавляет точку в вашу сеть после активации. Синие общие камни образуют сеть между камнями того же цвета; для этого задания нужен именно синий вариант.',
         'Подготовьте камни и варп-пыль как компонент телепортационных предметов. Сама пыль не является свитком мгновенного перемещения. Стоимость переходов и ограничения измерений зависят от конфигурации сборки.'],
        ['Activate a normal waystone to add a destination to your network. Blue sharestones connect to other sharestones of the same colour; this objective requires blue specifically.',
         'Prepare the stones and warp dust as a crafting ingredient for teleportation items. Dust itself is not an instant teleport scroll. Travel costs and dimension restrictions depend on the pack configuration.']),
    'magic_irons/arcane': (
        ['Окружите слиток железа, меди или золота восемью арканными эссенциями на верстаке: получится арканный слиток.',
         'Арканная наковальня имеет отдельный рецепт: три блока аметиста, алмаз, обычная наковальня и два полированных глубинных сланца. Подготовьте четыре арканных слитка для следующих рецептов и изготовьте наковальню.'],
        ['Surround an iron, copper or gold ingot with eight arcane essences at a crafting table to make an arcane ingot.',
         'The arcane anvil has a separate recipe: three amethyst blocks, a diamond, a normal anvil and two polished deepslate blocks. Stock four arcane ingots for later recipes and craft the anvil.']),
    'more_rails/crossing': (
        ['Обозначьте место, где пешеходная дорога пересекает железнодорожный путь. Подготовьте рельсы и два сигнала для контроля участка. Внутренний блок пересечения путей не нужно искать в инвентаре.',
         'Сначала проверьте проезд состава без пассажиров и свободный проход после его остановки. Это ручная проверка переезда: Кодекс не определяет безопасность движения и не включает автоматический шлагбаум.'],
        ['Mark where a footpath crosses the railway. Prepare track and two signals to control the section. There is no need to obtain the internal track-crossing block as an inventory item.',
         'First test a train passing without passengers, then check the footpath with the train stopped. This is a manual crossing check: the Codex does not assess traffic safety or activate an automatic barrier.']),
    'more_rails/depot': (
        ['Подготовьте три расписания и сдайте четыре синие фуражки. Из фуражки и андезитового корпуса создаётся кондуктор; здесь принимается именно синий цвет.',
         'Это снабжение депо, а не автоматическая проверка трёх работающих составов. Маршруты и посадку кондукторов настройте отдельно; после сдачи фуражки будут изъяты.'],
        ['Prepare three schedules and submit four blue conductor caps. A cap used on an andesite casing constructs a conductor; this objective accepts blue specifically.',
         'This stocks a depot rather than automatically certifying three working trains. Configure routes and seat conductors separately; submitted caps are consumed.']),
    'story_forge/train': (
        ['Подготовьте управление, расписание, синюю фуражку и пару переносных складских интерфейсов. Тележки ставятся железнодорожными корпусами на пути в режиме сборки станции.',
         'Создайте кондуктора фуражкой на андезитовом корпусе, посадите у управления и задайте маршрут между погрузкой и разгрузкой. Отметьте вручную только после полного рейса с переносом груза: одних предметов для подтверждения работы недостаточно.'],
        ['Prepare train controls, a schedule, a blue cap and two portable storage interfaces. Place bogeys using railway casings on track while the station is in assembly mode.',
         'Construct a conductor by applying the cap to an andesite casing, seat it at the controls and schedule loading and unloading stops. Confirm manually only after a complete cargo trip; inventory alone does not prove operation.']),
    'story_sky/cast': (
        ['Отлейте чугунные заготовки и рассверлите их на станке с подачей воды. Сдайте четыре готовых чугунных ствола.',
         'Ствол — часть орудия. Для выстрела потребуются собранная пушка с затвором, подходящие снаряд и заряд; четыре отдельных ствола не являются готовой батареей.'],
        ['Cast iron blanks and bore them on a water-fed drill. Submit four finished cast iron cannon barrels.',
         'A barrel is one cannon component. Firing also requires an assembled cannon with a breech, suitable projectile and charge; four loose barrels are not a working battery.']),
}

MANUAL = {
    'create_trains/bogey': ('placed_bogeys', 'Вручную: две тележки стоят на прямом пути внутри зоны сборки станции', 'Manually: two bogeys stand on straight track within the station assembly area'),
    'ca_electric/burner': ('liquid_heat', 'Вручную: горелка с трубочкой принимает биоэтанол и нагревает чашу', 'Manually: the burner with a straw accepts bioethanol and heats the basin'),
    'more_rails/crossing': ('crossing_trial', 'Вручную: проверены проезд состава и проход через остановленный участок', 'Manually: test train passage and pedestrian access with the section stopped'),
    'story_forge/train': ('freight_round_trip', 'Вручную: поезд выполнил полный рейс, загрузил и выгрузил груз через интерфейсы', 'Manually: the train completed a round trip and transferred cargo through the interfaces'),
}


def apply(chapters, translations):
    for c in chapters:
        c['icon'] = ITEM_REPLACEMENTS.get(c['icon'], c['icon'])
        for q in c['quests']:
            gid = c['id'] + '/' + q['id']
            q['icon'] = ITEM_REPLACEMENTS.get(q['icon'], q['icon'])
            for stack in q.get('tasks', []) + q.get('rewards', {}).get('items', []):
                if stack.get('type', 'item') == 'item':
                    stack['id'] = ITEM_REPLACEMENTS.get(stack['id'], stack['id'])
            if gid not in TEXT:
                continue
            en = translations[c['id']]['quests'][q['id']]
            q['text'], en['text'] = [list(lines) for lines in TEXT[gid]]
            if gid == 'cbc_foundry/cast':
                q['tasks'] = [item('createbigcannons:small_cast_mould'), item('createbigcannons:casting_sand', 4)]
            elif gid == 'cbc_foundry/drill':
                q['tasks'] = [item('createbigcannons:cannon_drill'), item('create:piston_extension_pole', 2), item('createbigcannons:cast_iron_cannon_barrel')]
            elif gid == 'radar/misc_radar':
                q['title'], en['title'] = 'Ручное наведение', 'Manual targeting'
                q['tasks'] = [item('create_radar:binoculars')]
            elif gid == 'ca_electric/burner':
                q['tasks'] = [item('create:blaze_burner'), item('createaddition:straw'), item('createaddition:bioethanol_bucket')]
            elif gid == 'more_rails/crossing':
                q['tasks'] = [item('create:track', 8), item('create:track_signal', 2)]
            elif gid == 'more_home/bed':
                q['title'], en['title'] = 'Спальня и ванная', 'Bedroom and bathroom'
            elif gid == 'story_forge/train':
                q['rewards']['items'] = [item('create:railway_casing', 10)]
                q['rewards']['items'][0].pop('type')
            if gid in MANUAL:
                identifier, ru_note, en_note = MANUAL[gid]
                # Ключ ручной отметки не зависит от формулировки текста.
                q['tasks'] = [t for t in q['tasks'] if t['id'] != identifier]
                q['tasks'].append({'type': 'check', 'id': identifier, 'note': ru_note})
                en['tasks'] = [''] * (len(q['tasks']) - 1) + [en_note]
