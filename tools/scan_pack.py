# -*- coding: utf-8 -*-
"""Строит списки существующих предметов, достижений и биомов по папке модов.

Запуск (аргументом можно передать и папку с jar-файлами, и отдельный jar;
клиентский jar Minecraft нужен, чтобы в списки попала ваниль):
    python3 tools/scan_pack.py ~/.local/share/PrismLauncher/instances/1.21.1/minecraft/mods \
        ~/.local/share/PrismLauncher/libraries/com/mojang/minecraft/1.21.1/minecraft-1.21.1-client.jar

Результат кладётся рядом с этим файлом: valid_ids.txt, valid_adv.txt, valid_biomes.txt.
Списки нужны build_book.py, чтобы отлавливать опечатки и предметы,
исчезнувшие при обновлении сборки.

Языковые файлы модов для этого не годятся: в них годами остаются ключи
предметов, которых в реестре давно нет. Надёжные источники — модели
предметов, состояния блоков, рецепты, теги и таблицы добычи.
"""
import io
import os
import re
import sys
import json
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))

RE_MODEL = re.compile(r"^assets/([^/]+)/models/item/(.+)\.json$")
RE_BLOCKSTATE = re.compile(r"^assets/([^/]+)/blockstates/(.+)\.json$")
RE_ADV = re.compile(r"^data/([^/]+)/advancement[s]?/(.+)\.json$")
RE_BIOME = re.compile(r"^data/([^/]+)/worldgen/biome/(.+)\.json$")
RE_DATA_JSON = re.compile(r"^data/([^/]+)/(recipe[s]?|tags|loot_table[s]?)/(.+)\.json$")
RE_ID = re.compile(r"\"(?:id|item|name)\"\s*:\s*\"([a-z0-9_.-]+:[a-z0-9_./-]+)\"")


def jars(paths):
    for p in paths:
        p = os.path.expanduser(p)
        if os.path.isdir(p):
            for name in sorted(os.listdir(p)):
                if name.endswith(".jar"):
                    yield os.path.join(p, name)
        elif p.endswith(".jar"):
            yield p
        else:
            print("не папка и не jar:", p, file=sys.stderr)


def scan_zip(zf, ids, advs, biomes, depth=0):
    for entry in zf.namelist():
        # часть модов поставляется обёрткой: настоящие моды лежат внутри,
        # в META-INF/jarjar, и снаружи у них нет ни моделей, ни рецептов
        if depth < 2 and entry.startswith("META-INF/jarjar/") and entry.endswith(".jar"):
            try:
                inner = io.BytesIO(zf.read(entry))
                with zipfile.ZipFile(inner) as nested:
                    scan_zip(nested, ids, advs, biomes, depth + 1)
            except (zipfile.BadZipFile, KeyError):
                print("пропущен вложенный архив:", entry, file=sys.stderr)
            continue
        m = RE_MODEL.match(entry) or RE_BLOCKSTATE.match(entry)
        if m:
            ids.add(m.group(1) + ":" + m.group(2))
            continue
        m = RE_ADV.match(entry)
        if m:
            advs.add(m.group(1) + ":" + m.group(2))
            continue
        m = RE_BIOME.match(entry)
        if m:
            biomes.add(m.group(1) + ":" + m.group(2))
            continue
        if RE_DATA_JSON.match(entry):
            try:
                body = zf.read(entry).decode("utf-8", "replace")
            except KeyError:
                continue
            ids.update(RE_ID.findall(body))


def collect(paths):
    ids, advs, biomes = set(), set(), set()
    for path in jars(paths):
        name = os.path.basename(path)
        try:
            zf = zipfile.ZipFile(path)
        except zipfile.BadZipFile:
            print("пропущен нечитаемый архив:", name, file=sys.stderr)
            continue
        with zf:
            scan_zip(zf, ids, advs, biomes)
    return ids, advs, biomes


def write(path, values):
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(sorted(values)) + "\n")
    print("%-16s %6d" % (os.path.basename(path), len(values)))


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    ids, advs, biomes = collect(sys.argv[1:])
    write(os.path.join(HERE, "valid_ids.txt"), ids)
    write(os.path.join(HERE, "valid_adv.txt"), advs)
    write(os.path.join(HERE, "valid_biomes.txt"), biomes)
    return 0


if __name__ == "__main__":
    sys.exit(main())
