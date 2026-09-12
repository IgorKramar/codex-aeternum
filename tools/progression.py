"""Учебный граф и компоновка карт. Идентификаторы сохранений не меняются.

`deps` — обязательные предпосылки, `any_deps` — один из альтернативных путей.
Границы исходных глав нужны для авторства и переводов; `map` задаёт экран книги.
"""
from collections import defaultdict
from curriculum import add_projects
from editorial import revise
from guidebook import apply as apply_guidebook
from registry_corrections import apply as correct_registry

# Входы в учебные главы: конкретный освоенный процесс, а не номер главы.
ENTRIES = {
    'create_basics': ['start_first_day/iron'],
    'create_andesite': ['create_basics/shaft'],
    'create_kinetics': ['create_basics/cogwheel'],
    'create_fluids': ['create_andesite/press'],
    'create_copper': ['create_fluids/pump'],
    'create_brass': ['create_andesite/blaze'],
    'create_contraptions': ['create_andesite/press'],
    'create_packages': ['create_brass/brass_funnel'],
    'create_trains': ['create_brass/precision'],
    'create_tools': ['create_andesite/press'],
    'create_world': ['create_basics/andesite'],
    'ca_electric': ['create_andesite/press'],
    'aero_basics': ['create_contraptions/glue'],
    'offroad': ['create_contraptions/glue'],
    'cbc_foundry': ['create_andesite/press'],
    'cbc_advanced': ['cbc_foundry/shot'],
    'radar': ['cbc_foundry/mount'],
    'missiles': ['radar/datalink'],
    'ie_start': ['start_first_day/iron'],
    'ie_power': ['ie_start/hammer'],
    'ie_machines': ['ie_start/blast'],
    'ie_chemistry': ['ie_machines/crusher_ie'],
    'ie_gear': ['ie_start/blast'],
    'mek_start': ['start_first_day/iron'],
    'mek_power': ['mek_start/osmium'],
    'mek_ore': ['mek_start/casing'],
    'mek_nuclear': ['mek_ore/enrichment'],
    'mek_qio': ['mek_start/alloys'],
    'mek_gear': ['mek_start/casing'],
    'rs_network': ['start_first_day/iron'],
    'rs_autocraft': ['rs_network/grid'],
    'storage_local': ['start_first_day/backpack'],
    'mc_found': ['start_first_day/crafting'],
    'mc_production': ['mc_found/builder'],
    'mc_research': ['mc_found/warehouse'],
    'mc_military': ['mc_found/builder'],
    'mc_build': ['mc_found/buildtool'],
    'dim_nether': ['start_first_day/iron'],
    'dim_end': ['dim_nether/blaze'],
    'dim_aether': ['dim_nether/quartz'],
    'dim_twilight': ['start_first_day/iron'],
    'magic_botania': ['start_first_day/iron'],
    'magic_botania_runes': ['magic_botania/manasteel'],
    'magic_botania_end': ['magic_botania_runes/terrasteel'],
    'magic_agriculture': ['start_first_day/iron'],
    'magic_ars': ['start_first_day/iron'],
    'magic_irons': ['start_first_day/iron'],
    'tech2_newage': ['create_andesite/press'],
    'tech2_mektools': ['mek_start/infuser'],
    'tech2_pneumatic': ['start_first_day/iron'],
    'tech2_foregoing': ['start_first_day/iron'],
    'tech2_powah': ['start_first_day/iron'],
    'tech2_petroleum': ['ie_start/blast'],
    'space_ground': ['start_first_day/iron'],
    'space_moon': ['space_ground/checklist'],
    'space_mars': ['space_moon/tier2'],
    'space_hot': ['space_mars/tier3'],
    'space_glacio': ['space_hot/tier4'],
    'fd_kitchen': ['start_first_day/crafting'],
    'life_furniture': ['start_first_day/crafting'],
    'life_world': ['start_first_day/crafting'],
    'hunt_cataclysm': ['dim_nether/blaze'],
    'hunt_beasts': ['start_first_day/iron'],
    'hunt_apotheosis': ['start_first_day/iron'],
    'et_intro': ['start_first_day/crafting'],
    'et_skills': ['et_intro/journal'],
    'et_sorcery': ['et_intro/journal'],
    'et_archaeology': ['et_intro/journal'],
    'et_farming': ['et_intro/journal'],
    'et_overworld': ['et_intro/journal'],
    'et_nether_end': ['et_intro/journal', 'dim_nether/portal'],
    'et_comets': ['et_overworld/interdim'],
    'et_purgatorium': ['et_overworld/interdim'],
    'et_eden': ['et_nether_end/end_quest'],
    'et_rayana': ['et_eden/crystal_eden'],
    'et_karvat': ['et_rayana/crystal_ray'],
    'et_volcanech': ['et_karvat/crystal_kar'],
    'et_amber': ['et_volcanech/crystal_vol'],
    'et_unahzaal': ['et_amber/crystal_amb'],
    'et_ultimate': ['et_unahzaal/unahzaal'],
    'et_darkness': ['et_unahzaal/crystal_un'],
    'et_gear': ['et_intro/journal'],
    'story_forge': ['create_basics/andesite'],
    'story_current': ['ie_start/blast'],
    'story_expedition': ['start_first_day/iron'],
    'story_colony': ['mc_found/townhall'],
    'story_sky': ['aero_basics/assembler'],
    'trials_early': ['start_first_day/crafting'],
    'trials_mid': ['create_andesite/press'],
    'trials_late': ['create_brass/precision'],
    'trials_bosses': ['dim_nether/portal'],
    'final_bridges': ['create_brass/precision'],
    'final_goals': ['final_bridges/rot_to_fe'] ,
    'end_monuments': ['create_brass/precision'],
    'end_marathon': ['create_brass/precision'],
    'end_apotheosis': ['et_unahzaal/unahzaal'],
    'more_vanilla': ['start_first_day/iron'],
    'more_explore': ['start_first_day/map'],
    'more_kitchen': ['fd_kitchen/pot'],
    'more_rails': ['create_trains/train'],
    'more_munitions': ['cbc_foundry/shot'],
    'more_et_side': ['et_intro/journal'],
    'more_home': ['start_first_day/crafting'],
    'more_qol2': ['start_first_day/crafting'],
}

# Явные развилки заменяют неявный chain() там, где он делал факультативы воротами.
BRANCHES = {
    'cbc_advanced': {'armor': ['steel']},
    'create_tools': {'schematic': ['extendo']},
    'et_intro': {'miguel': ['notice']},
    'et_overworld': {'vivid': ['bosses_ow']},
    'mek_gear': {'mekasuit': ['atomic_disassembler']},
    'space_moon': {'solar': ['desh']},
    'rs_autocraft': {'jei_rs': ['upgrade_craft']},
    'start_first_day': {
        'wood': [], 'crafting': ['wood'], 'iron': ['crafting'], 'night': ['crafting'],
        'death': ['crafting'], 'jade': ['crafting'], 'map': ['crafting'], 'base': ['iron'],
    },
    'create_basics': {
        'andesite': [], 'shaft': ['andesite'], 'cogwheel': ['shaft'],
        'handcrank': ['shaft'], 'waterwheel': ['shaft'], 'windmill': ['cogwheel'],
        'sail': ['windmill'], 'bigwheel': ['waterwheel'],
        'stress': ['cogwheel'], 'wrench': ['andesite'], 'goggles': ['wrench'], 'ponder': ['andesite'],
    },
    'create_andesite': {
        'casing': [], 'press': ['casing'], 'millstone': ['casing'],
        'saw': ['casing'], 'fan': ['casing'], 'belt': ['press'],
        'depot': ['press'], 'chute': ['press'], 'mixer': ['press'],
        'blaze': ['mixer', 'dim_nether/blaze'],
        'crafter_basic': ['create_brass/brass'], 'ejector': ['create_brass/precision'],
    },
    'create_kinetics': {
        'gearbox': [], 'clutch': ['gearbox'], 'chaindrive': ['gearbox'],
        'sequenced': ['clutch', 'create_brass/precision'],
        'rsc': ['create_brass/precision'], 'flywheel': ['create_copper/boiler'],
        'logic': ['clutch'], 'link': ['logic'], 'stockpile': ['logic'], 'display': ['stockpile'],
    },
    'create_fluids': {
        'pipe': [], 'pump': ['pipe'], 'tank': ['pipe'], 'hose': ['pump'],
        'spout': ['pump'], 'chocolate': ['spout', 'create_andesite/mixer'],
        'portable_fluid': ['tank', 'create_contraptions/glue'],
    },
    'create_brass': {
        'brass': [], 'brass_casing': ['brass'], 'crushing': ['brass', 'create_andesite/crafter_basic'],
        'brass_funnel': ['brass'], 'deployer': ['brass_casing'],
        'precision': ['deployer', 'create_andesite/press'],
        'arm': ['precision'], 'vault': ['brass_funnel'], 'chromatic': ['precision'],
    },
    'create_copper': {
        'copper_casing': [], 'boiler': ['copper_casing', 'create_fluids/tank'],
        'whistle': ['boiler'], 'backtank': ['copper_casing'],
        'diving': ['backtank'], 'netherite_diving': ['diving'],
    },
    'mek_start': {
        'osmium': [], 'infuser': ['osmium', 'mek_power/heat_gen'], 'steel': ['infuser'],
        'casing': ['steel'], 'circuit': ['infuser'], 'alloys': ['infuser'],
        'cables': ['steel'], 'sorter': ['circuit'], 'energy': ['circuit'],
        'configurator': ['alloys'], 'box': ['osmium'],
    },
    'mek_power': {
        'heat_gen': [], 'solar': ['mek_start/alloys'], 'wind': ['mek_start/alloys'],
        'bio': ['mek_ore/crusher_mek'], 'gas_gen': ['bio'],
        'boiler': ['mek_start/casing'], 'turbine': ['boiler'], 'induction': ['mek_start/alloys'],
    },
    'mek_ore': {
        'enrichment': [], 'crusher_mek': ['enrichment'], 'purification': ['enrichment'],
        'evaporation': ['purification'], 'injection': ['purification', 'evaporation'],
        'dissolution': ['injection'], 'factory': ['enrichment'],
        'miner': ['mek_start/alloys'], 'upgrades': ['enrichment'], 'sawmill': ['enrichment'],
    },
    'mek_nuclear': {
        'uranium': [], 'hazmat': ['uranium'], 'fuel': ['uranium'],
        'reactor': ['hazmat', 'fuel'], 'waste': ['reactor'],
        'fusion': ['waste', 'mek_ore/evaporation'], 'sps': ['waste'],
    },
}


def apply(chapters, translations):
    by_id = {c['id']: c for c in chapters}
    for cid, rules in BRANCHES.items():
        for q in by_id[cid]['quests']:
            if q['id'] in rules:
                q['deps'] = list(rules[q['id']])
    for cid, deps in ENTRIES.items():
        for q in by_id[cid]['quests']:
            if not q.get('deps') and not q.get('any_deps'):
                q['deps'] = list(deps)

    quests = {c['id']+'/'+q['id']: q for c in chapters for q in c['quests']}
    for gid, alternatives in {
        'create_basics/stress': ['waterwheel', 'windmill', 'handcrank'],
        'story_forge/mill': ['source', 'source_w'],
        'story_forge/wheels': ['source', 'source_w'],
        'story_forge/smelt': ['mill', 'wheels'],
        'story_current/grid': ['dynamo', 'alternator'],
    }.items():
        q = quests[gid]
        if gid != 'create_basics/stress':
            q['deps'] = []
        q['any_deps'] = alternatives
    for gid in ['story_forge/source_w', 'create_basics/bigwheel', 'create_basics/sail',
                'create_copper/whistle', 'create_tools/worldshaper']:
        quests[gid]['optional'] = True

    # Внутренний блок ленты не является предметом выживания. Игрок получает соединитель.
    for c in chapters:
        for q in c['quests']:
            for t in q.get('tasks', []):
                if t['type'] == 'item' and t['id'] == 'create:belt':
                    t['id'] = 'create:belt_connector'
                    t['count'] = min(t.get('count', 1), 8)
    revise(chapters, translations)
    correct_registry(chapters, translations)
    add_projects(chapters, translations)
    apply_guidebook(chapters, translations)
    layout(chapters)


def layout(chapters):
    """Единый граф карты: обязательные и альтернативные входы слева от результата."""
    maps = defaultdict(dict)
    for c in sorted(chapters, key=lambda c: (c['order'], c['id'])):
        c['map'] = c['section']
        for q in c['quests']:
            maps[c['map']][c['id']+'/'+q['id']] = (c, q)
    for quests in maps.values():
        depths, layers, parents = {}, defaultdict(list), {}
        for gid, (c, q) in quests.items():
            parents[gid] = [d if '/' in d else c['id']+'/'+d
                            for d in q.get('deps', []) + q.get('any_deps', [])]
        def depth(gid, visiting=frozenset()):
            if gid in depths:
                return depths[gid]
            if gid in visiting:
                raise ValueError(f"Цикл компоновки: {gid}")
            depths[gid] = 1 + max((depth(d, visiting | {gid}) for d in parents[gid]
                                   if d in quests), default=-1)
            return depths[gid]
        for gid in quests:
            layers[depth(gid)].append(gid)
        height = max(map(len, layers.values()))
        for d, layer in sorted(layers.items()):
            def parent_row(gid):
                rows = [quests[p][1]['y'] for p in parents[gid] if p in quests]
                return sum(rows)/len(rows) if rows else height/2
            layer.sort(key=parent_row)
            offset = (height-len(layer))//2
            for row, gid in enumerate(layer):
                q = quests[gid][1]
                q['x'], q['y'] = 2*d, offset+row
