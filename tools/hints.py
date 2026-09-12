# -*- coding: utf-8 -*-
"""Индекс источников предметов книги: рецепты, добыча с существ, сундуки и блоки.

Берётся из установленных JAR сборки, а не из чужих версий модов:
    python3 tools/hints.py ~/.local/share/PrismLauncher/instances/1.21.1/minecraft/mods \\
        ~/.local/share/PrismLauncher/libraries/com/mojang/minecraft/1.21.1/minecraft-1.21.1-client.jar

Результат — src/main/resources/assets/codex/book/hints.json: для каждого предмета целей
и наград до трёх рецептов (тип и ингредиенты), существа, из которых он выпадает, сундуки
структур и блоки, при разрушении которых он появляется. Имена предметов, существ и блоков
клиент подставляет сам на языке игры, поэтому здесь только идентификаторы.
"""
import io
import json
import os
import re
import sys
import zipfile
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / 'src/main/resources/assets/codex/book/hints.json'
CHAPTERS = HERE.parent / 'src/main/resources/assets/codex/book/chapters'
RE_ID = re.compile(r'^[a-z0-9_.-]+:[a-z0-9_./-]+$')
RESULT_KEYS = ('result', 'results', 'output', 'outputs', 'main_output', 'secondary_output',
               'secondaryoutputs', 'item_output', 'item_outputs', 'secondary_result', 'itemoutput')
# Ключи, значения которых не являются ингредиентами: шаблон, условия, служебные поля.
SKIP_KEYS = {'type', 'pattern', 'category', 'group', 'neoforge:conditions', 'conditions',
             'show_notification', 'processingTime', 'processing_time', 'heat_requirement',
             'loops', 'transitional_item', 'transitionalItem', 'keep_held_item', 'keepHeldItem',
             'energy', 'duration', 'experience', 'cookingtime', 'per_tick_usage', 'per_tick_usage'}
# Рецепты этих типов не объясняют получение предмета игроку.
SKIP_TYPES = {'refinedstorage:recoloring', 'minecraft:crafting_special_armordye', 'cucumber:shaped_transfer_damage',
              'create:emptying', 'mekanism:pigment_extracting', 'mekanism:painting'}
MAX_RECIPES, MAX_LIST = 3, 4


def wanted_items():
    """Предметы целей и наград и достижения целей."""
    items, advancements = set(), set()
    for path in CHAPTERS.glob('*.json'):
        for chapter in json.loads(path.read_text(encoding='utf-8')):
            for q in chapter['quests']:
                for t in q.get('tasks', []):
                    kind = t.get('type', 'item')
                    if kind == 'item':
                        items.add(t['id'])
                    elif kind == 'advancement':
                        advancements.add(t['id'])
                for stack in q.get('rewards', {}).get('items', []):
                    items.add(stack['id'])
    return items, advancements


def jars(paths):
    for p in paths:
        p = os.path.expanduser(p)
        if os.path.isdir(p):
            for name in sorted(os.listdir(p)):
                if name.endswith('.jar'):
                    yield os.path.join(p, name)
        elif p.endswith('.jar'):
            yield p


def walk(zf, depth=0):
    """Файлы data/ из JAR и вложенных jarjar-архивов."""
    for entry in zf.namelist():
        if depth < 2 and entry.startswith('META-INF/jarjar/') and entry.endswith('.jar'):
            try:
                with zipfile.ZipFile(io.BytesIO(zf.read(entry))) as nested:
                    yield from walk(nested, depth + 1)
            except (zipfile.BadZipFile, KeyError):
                pass
            continue
        if entry.startswith('data/') and entry.endswith('.json'):
            yield entry, zf
        if entry == 'META-INF/neoforge.mods.toml':
            yield entry, zf


def mod_ids(text):
    return set(re.findall(r'^\s*modId\s*=\s*"([^"]+)"', text, re.MULTILINE))


def collect(value, under_result, results, ingredients, fluids, id_keys=('item', 'id', 'block')):
    """Обходит рецепт целиком: под ключами результата — продукты, иначе ингредиенты и жидкости."""
    if isinstance(value, dict):
        for k, v in value.items():
            lk = k.lower()
            if lk in SKIP_KEYS:
                continue
            target_result = under_result or lk in RESULT_KEYS
            if lk in ('fluid', 'fluidtag', 'fluid_tag'):
                if isinstance(v, str):
                    fluids.append(('~#' if lk != 'fluid' else '~') + v)
                else:
                    inner = []
                    collect(v, False, [], inner, [])
                    fluids.extend('~' + f for f in inner)
                continue
            if lk == 'tag' and isinstance(v, str):
                (results if target_result else ingredients).append('#' + v)
            elif lk in id_keys and isinstance(v, str) and RE_ID.match(v):
                (results if target_result else ingredients).append(v)
            else:
                collect(v, target_result, results, ingredients, fluids, id_keys)
    elif isinstance(value, list):
        for v in value:
            collect(v, under_result, results, ingredients, fluids, id_keys)
    elif isinstance(value, str):
        if value.startswith('#') or RE_ID.match(value):
            (results if under_result else ingredients).append(value)


def ids_in(value, out, fluids, id_keys=('item', 'id', 'block')):
    collect(value, False, [], out, fluids, id_keys)


class Tags:
    """Теги предметов сборки: раскрывают результаты рецептов, заданные тегом."""

    def __init__(self):
        self.members = defaultdict(set)

    def add(self, namespace, path, doc):
        for v in doc.get('values', []):
            v = v.get('id') if isinstance(v, dict) else v
            if isinstance(v, str):
                self.members[f'{namespace}:{path}'].add(v)

    def expand(self, tag, depth=0):
        out = set()
        for v in self.members.get(tag, ()):
            if v.startswith('#'):
                if depth < 4:
                    out |= self.expand(v[1:], depth + 1)
            else:
                out.add(v)
        return out


def conditions_ok(recipe, installed):
    def evaluate(c):
        t = c.get('type', '')
        if t.endswith('mod_loaded'):
            return c.get('modid') in installed
        if t.endswith(':not'):
            return not evaluate(c.get('value', {}))
        if t.endswith(':and'):
            return all(evaluate(x) for x in c.get('values', []))
        if t.endswith(':or'):
            return any(evaluate(x) for x in c.get('values', []))
        if t.endswith(':false'):
            return False
        return True
    return all(evaluate(c) for c in recipe.get('neoforge:conditions', []) if isinstance(c, dict))


def dedupe(seq, limit):
    seen, out = set(), []
    for x in seq:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out[:limit]


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    wanted, wanted_advancements = wanted_items()
    advancements = {}
    recipes = defaultdict(list)
    drops, chests, blocks = defaultdict(list), defaultdict(list), defaultdict(list)
    installed = {'minecraft', 'neoforge'}
    documents = []
    for jar in jars(argv):
        try:
            zf = zipfile.ZipFile(jar)
        except zipfile.BadZipFile:
            print('пропущен:', jar, file=sys.stderr)
            continue
        for entry, source in walk(zf):
            if entry.endswith('neoforge.mods.toml'):
                installed |= mod_ids(source.read(entry).decode('utf-8', 'replace'))
                continue
            try:
                documents.append((entry, json.loads(source.read(entry))))
            except (ValueError, KeyError):
                continue
    tags = Tags()
    for entry, doc in documents:
        parts = entry.split('/')
        if len(parts) > 4 and parts[2] == 'tags' and parts[3] in ('item', 'items') and isinstance(doc, dict):
            tags.add(parts[1], '/'.join(parts[4:])[:-5], doc)
    features, placed, biome_features, spawns, world = {}, {}, defaultdict(set), defaultdict(set), defaultdict(set)
    structures = defaultdict(set)
    for entry, doc in documents:
        if not isinstance(doc, dict):
            continue
        parts = entry.split('/')
        namespace, kind = parts[1], parts[2]
        if kind in ('recipe', 'recipes'):
            if not conditions_ok(doc, installed):
                continue
            rtype = doc.get('type', '')
            if rtype in SKIP_TYPES:
                continue
            results, ingredients, fluids = [], [], []
            collect(doc, False, results, ingredients, fluids)
            produced = set()
            for r in results:
                produced |= tags.expand(r[1:]) if r.startswith('#') else {r}
            hit = sorted(produced & wanted)
            if not hit:
                continue
            ingredients = [i for i in dedupe(ingredients, 12) if i not in produced]
            for item in hit:
                recipes[item].append({'type': rtype, 'in': ingredients + dedupe(fluids, 2)})
        elif kind in ('loot_table', 'loot_tables') and len(parts) > 4:
            table, tail = parts[3], '/'.join(parts[4:])[:-5]
            found = []
            ids_in(doc, found, [], ('item', 'id', 'name'))
            found = [f for f in dedupe(found, 40) if f in wanted and not f.startswith('#')]
            if not found:
                continue
            if table == 'entities':
                for item in found:
                    drops[item].append(f'{namespace}:{tail}')
            elif table == 'chests':
                for item in found:
                    chests[item].append(f'{namespace}:{tail}')
            elif table == 'blocks':
                block = f'{namespace}:{tail}'
                for item in found:
                    if item != block:
                        blocks[item].append(block)
        elif kind in ('advancement', 'advancements') and len(parts) > 3:
            aid = f"{namespace}:{'/'.join(parts[3:])[:-5]}"
            display = doc.get('display')
            if aid in wanted_advancements and isinstance(display, dict):
                advancements[aid] = {k: display[k] for k in ('title', 'description') if k in display}
        elif kind == 'worldgen' and len(parts) > 4:
            name = f"{namespace}:{'/'.join(parts[4:])[:-5]}"
            if parts[3] == 'configured_feature':
                found = []
                ids_in(doc, found, [])
                features[name] = {f for f in found if not f.startswith('#')}
            elif parts[3] == 'placed_feature':
                placed[name] = doc.get('feature') if isinstance(doc.get('feature'), str) else None
            elif parts[3] == 'biome':
                for step in doc.get('features', []):
                    for f in (step if isinstance(step, list) else [step]):
                        if isinstance(f, str):
                            biome_features[name].add(f)
                for group in doc.get('spawners', {}).values():
                    for spawner in group:
                        if isinstance(spawner, dict) and isinstance(spawner.get('type'), str):
                            spawns[spawner['type']].add(name)
            elif parts[3] == 'structure':
                for group in doc.get('spawn_overrides', {}).values():
                    for spawner in group.get('spawns', []) if isinstance(group, dict) else []:
                        if isinstance(spawner, dict) and isinstance(spawner.get('type'), str):
                            structures[spawner['type']].add(name)
    for biome, feature_ids in biome_features.items():
        for pf in feature_ids:
            configured = placed.get(pf, pf)
            for block in features.get(configured, ()):
                if block in wanted:
                    world[block].add(biome)
    def unpacking(recipe, item):
        """Рецепт «блок → 9 предметов» ничего не объясняет о добыче."""
        base = item.split(':')[1]
        return len(recipe['in']) == 1 and any(base.replace('ingot_', '').replace('_ingot', '') in i and 'block' in i for i in recipe['in'])

    index, entities = {}, {}
    for item in sorted(wanted):
        entry = {}
        if recipes[item]:
            ordered = sorted(recipes[item], key=lambda r: (unpacking(r, item), not r['type'].startswith('minecraft:'), len(r['in'])))
            unique = dedupe([json.dumps(r, sort_keys=True) for r in ordered], MAX_RECIPES)
            entry['recipes'] = [json.loads(r) for r in unique]
        if drops[item]:
            entry['drops'] = dedupe(drops[item], MAX_LIST)
            for entity in entry['drops']:
                habitat = sorted(spawns.get(entity, ()))[:MAX_LIST] + sorted(structures.get(entity, ()))[:2]
                if habitat:
                    entities[entity] = habitat
        if chests[item]:
            entry['chests'] = dedupe(chests[item], MAX_LIST)
        if blocks[item]:
            entry['blocks'] = dedupe(sorted(blocks[item], key=lambda b: 'ore' not in b), MAX_LIST)
        if world[item]:
            entry['world'] = sorted(world[item])[:MAX_LIST]
        if entry:
            index[item] = entry
    index = {'items': index, 'entities': entities, 'advancements': advancements}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(index, ensure_ascii=False, indent=1, sort_keys=True) + '\n', encoding='utf-8')
    types = defaultdict(int)
    for entry in index['items'].values():
        for r in entry.get('recipes', []):
            types[r['type']] += 1
    print(f'предметов в книге: {len(wanted)}, с источниками: {len(index["items"])}, без источников: {len(wanted) - len(index["items"])}, существ с местами обитания: {len(entities)}, достижений с описанием: {len(advancements)} из {len(wanted_advancements)}')
    print('типы рецептов:', ', '.join(f'{t} {n}' for t, n in sorted(types.items(), key=lambda kv: -kv[1])))
    print('без источников:', ' '.join(sorted(wanted - set(index['items']))))
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
