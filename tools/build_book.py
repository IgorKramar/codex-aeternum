# -*- coding: utf-8 -*-
"""Собирает JSON-главы книги и проверяет ссылки на предметы."""
import importlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import dsl  # noqa: E402
from rewards import REWARDS  # noqa: E402
from polish import INTROS  # noqa: E402

MODULES = [m[:-3] for m in sorted(os.listdir(HERE))
           if m.startswith("c_") and m.endswith(".py")]

for m in MODULES:
    importlib.import_module(m)

OUT = os.path.join(HERE, "..", "src", "main", "resources", "assets", "codex", "book", "chapters")
OUT = os.path.normpath(OUT)
VALID = os.environ.get("VALID_IDS", "")
VALID_ADV = os.environ.get("VALID_ADV", "")

valid = set()
if VALID and os.path.isfile(VALID):
    valid = set(open(VALID, encoding="utf-8").read().split())
valid_adv = set()
if VALID_ADV and os.path.isfile(VALID_ADV):
    valid_adv = set(open(VALID_ADV, encoding="utf-8").read().split())

os.makedirs(OUT, exist_ok=True)
for f in os.listdir(OUT):
    if f.endswith(".json"):
        os.remove(os.path.join(OUT, f))

LANG_RU = {}
LANG_EN = {}
missing_en = []

try:
    from lang_en import EN  # noqa: E402
except Exception:
    EN = {}


def put(key, ru, en_val):
    LANG_RU[key] = ru
    if en_val:
        LANG_EN[key] = en_val
    else:
        missing_en.append(key)
        LANG_EN[key] = ru


def localize(c):
    en_c = EN.get(c["id"], {})
    base = "codex.chapter." + c["id"]
    put(base + ".title", c["title"], en_c.get("title"))
    c["title"] = base + ".title"
    if c.get("subtitle"):
        put(base + ".subtitle", c["subtitle"], en_c.get("subtitle"))
        c["subtitle"] = base + ".subtitle"
    en_intro = en_c.get("intro") or []
    for i, p in enumerate(c.get("intro", [])):
        put(f"{base}.intro.{i}", p, en_intro[i] if i < len(en_intro) else None)
        c["intro"][i] = f"{base}.intro.{i}"
    en_q_all = en_c.get("quests", {})
    for q in c["quests"]:
        en_q = en_q_all.get(q["id"], {})
        qb = f"codex.quest.{c['id']}.{q['id']}"
        put(qb + ".title", q["title"], en_q.get("title"))
        q["title"] = qb + ".title"
        en_text = en_q.get("text") or []
        for i, p in enumerate(q.get("text", [])):
            put(f"{qb}.text.{i}", p, en_text[i] if i < len(en_text) else None)
            q["text"][i] = f"{qb}.text.{i}"
        en_tasks = en_q.get("tasks") or []
        for i, tk in enumerate(q.get("tasks", [])):
            if tk.get("note"):
                put(f"{qb}.task.{i}", tk["note"], en_tasks[i] if i < len(en_tasks) else None)
                tk["note"] = f"{qb}.task.{i}"
        r = q.get("rewards")
        if r:
            en_r = en_q.get("rewards") or []
            for i, p in enumerate(r.get("text", [])):
                put(f"{qb}.reward.{i}", p, en_r[i] if i < len(en_r) else None)
                r["text"][i] = f"{qb}.reward.{i}"


bad_icons = []
bad_items = []
bad_deps = []
bad_adv = []
bad_rewards = []
known_rewards = set(REWARDS)
dupes = []
seen_chapters = set()
total_quests = 0

XP_BY_SECTION = {"start": 15, "world": 15, "story": 0, "endgame": 0, "more": 30, "magic": 45, "tech2": 45, "space": 70, "hunt": 60, "create": 25, "createx": 40, "ie": 30, "mek": 40,
                 "storage": 30, "colony": 30, "dim": 45, "eternal": 60, "life": 20, "final": 120,
                 "trials": 0}

by_section = {}
for c in dsl.CHAPTERS:
    if c["id"] in INTROS:
        c["intro"] = list(INTROS[c["id"]])
    for q in c["quests"]:
        gid = c["id"] + "/" + q["id"]
        if gid in REWARDS:
            q["rewards"] = dict(REWARDS[gid])
        r = q.get("rewards")
        if r is None:
            r = {"items": [], "xp": 0, "text": []}
            q["rewards"] = r
        if r.get("xp", 0) == 0 and q.get("tasks"):
            base = XP_BY_SECTION.get(c["section"], 20)
            r["xp"] = base * 2 if q.get("shape") == "big" else base
    
    if c["id"] in seen_chapters:
        dupes.append(c["id"])
    seen_chapters.add(c["id"])
    by_section.setdefault(c["section"], []).append(c)

    ids = set()
    for q in c["quests"]:
        total_quests += 1
        if q["id"] in ids:
            dupes.append(c["id"] + "/" + q["id"])
        ids.add(q["id"])
    for q in c["quests"]:
        known_rewards.discard(c["id"] + "/" + q["id"])
        for s in q.get("rewards", {}).get("items", []):
            if valid and s["id"] not in valid:
                bad_rewards.append(f"{c['id']}/{q['id']}: {s['id']}")
        for d in q.get("deps", []):
            key = d.split("/")[-1]
            if key not in ids:
                bad_deps.append(f"{c['id']}/{q['id']} -> {d}")
        if valid and q["icon"] not in valid:
            bad_icons.append(f"{c['id']}/{q['id']}: {q['icon']}")
        for t in q.get("tasks", []):
            if t.get("type", "item") == "item" and valid and t["id"] not in valid:
                bad_items.append(f"{c['id']}/{q['id']}: {t['id']}")
            if t.get("type") == "advancement" and valid_adv and t["id"] not in valid_adv:
                bad_adv.append(f"{c['id']}/{q['id']}: {t['id']}")
    if valid and c["icon"] not in valid:
        bad_icons.append(f"{c['id']} (иконка главы): {c['icon']}")

for c in dsl.CHAPTERS:
    localize(c)

# разделы
SECTIONS_PATH = os.path.normpath(os.path.join(OUT, "..", "sections.json"))
sections = json.load(open(SECTIONS_PATH, encoding="utf-8"))
from lang_en import SECTIONS_EN, SECTIONS_RU  # noqa: E402
for sid, s in sections.items():
    key = "codex.section." + sid
    put(key, SECTIONS_RU.get(sid, sid), SECTIONS_EN.get(sid))
    s["title"] = key
json.dump(sections, open(SECTIONS_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

from lang_en import UI_EN, UI_RU  # noqa: E402
LANG_RU.update(UI_RU)
LANG_EN.update(UI_EN)

LANG_DIR = os.path.normpath(os.path.join(OUT, "..", "..", "lang"))
os.makedirs(LANG_DIR, exist_ok=True)
json.dump(dict(sorted(LANG_RU.items())), open(os.path.join(LANG_DIR, "ru_ru.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
json.dump(dict(sorted(LANG_EN.items())), open(os.path.join(LANG_DIR, "en_us.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

for sec, chapters in by_section.items():
    path = os.path.join(OUT, sec + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(chapters, f, ensure_ascii=False, indent=1)

print(f"Глав: {len(dsl.CHAPTERS)}, заданий: {total_quests}, файлов: {len(by_section)}, "
      f"строк локализации: {len(LANG_RU)}, без английского: {len(missing_en)}")
if missing_en and os.environ.get("SHOW_MISSING"):
    for k in missing_en[:60]:
        print("   ", k)
for name, lst in (("Дубли", dupes), ("Битые зависимости", bad_deps),
                  ("Неизвестные иконки", bad_icons), ("Неизвестные предметы в целях", bad_items),
                  ("Неизвестные достижения", bad_adv),
                  ("Неизвестные предметы в наградах", bad_rewards),
                  ("Награды без задания", sorted(known_rewards))):
    if lst:
        print(f"\n!! {name} ({len(lst)}):")
        for x in lst[:80]:
            print("   ", x)
