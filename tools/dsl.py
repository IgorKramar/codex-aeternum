# -*- coding: utf-8 -*-
"""Мини-язык для описания глав книги."""

CHAPTERS = []


def item(i, n=1, note=None):
    d = {"type": "item", "id": i, "count": n}
    if note:
        d["note"] = note
    return d


def give(i, n=1, note=None):
    """Цель со сдачей предметов: они забираются при получении награды."""
    d = {"type": "item", "id": i, "count": n, "consume": True}
    if note:
        d["note"] = note
    return d


def ponder(i, note=None):
    d = {"type": "ponder", "id": i}
    if note:
        d["note"] = note
    return d


def loot(*stacks, xp=0, text=()):
    """Награда: пары (id, count), опыт и пояснение."""
    return {
        "items": [{"id": i, "count": n} for i, n in stacks],
        "xp": xp,
        "text": list(text) if not isinstance(text, str) else [text],
    }


def adv(i, note=None):
    d = {"type": "advancement", "id": i}
    if note:
        d["note"] = note
    return d


def dim(i, note=None):
    d = {"type": "dimension", "id": i}
    if note:
        d["note"] = note
    return d


def biome(i, note=None):
    d = {"type": "biome", "id": i}
    if note:
        d["note"] = note
    return d


def check(note):
    """Ручная отметка. Игрок ставит галочку сам, поэтому формулировка — просьба."""
    text = note if note.lower().startswith(("прочитано", "вручную")) else "Вручную: " + note
    return {"type": "check", "id": note[:40], "note": text}


def Q(qid, title, icon, x, y, deps=(), text=(), tasks=(), rewards=(), shape=None, optional=False):
    q = {
        "id": qid,
        "title": title,
        "icon": icon,
        "x": x,
        "y": y,
    }
    if deps:
        q["deps"] = list(deps)
    if text:
        q["text"] = list(text) if not isinstance(text, str) else [text]
    if tasks:
        q["tasks"] = list(tasks)
    if rewards:
        if isinstance(rewards, dict):
            q["rewards"] = rewards
        else:
            q["rewards"] = {"items": [], "xp": 0,
                            "text": list(rewards) if not isinstance(rewards, str) else [rewards]}
    if shape:
        q["shape"] = shape
    if optional:
        q["optional"] = True
    return q


def chapter(cid, section, order, title, icon, subtitle="", intro=(), quests=()):
    c = {
        "id": cid,
        "section": section,
        "order": order,
        "title": title,
        "icon": icon,
        "subtitle": subtitle,
        "intro": list(intro),
        "quests": list(quests),
    }
    CHAPTERS.append(c)
    return c


def chain(quests):
    """Проставляет зависимости по цепочке, если они не заданы явно."""
    prev = None
    for q in quests:
        if prev is not None and "deps" not in q:
            q["deps"] = [prev["id"]]
        prev = q
    return quests
