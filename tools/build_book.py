# -*- coding: utf-8 -*-
"""Компилирует книгу. --check проверяет ресурсы без записи на диск."""
import argparse
from copy import deepcopy
import importlib
import json
import os
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
from book_compiler import ValidationError, localize, validate

OUT = HERE.parent / 'src/main/resources/assets/codex/book/chapters'
XP_BY_SECTION = {'start': 15, 'world': 15, 'story': 0, 'endgame': 0,
                 'more': 30, 'magic': 45, 'tech2': 45, 'space': 70, 'hunt': 60,
                 'create': 25, 'createx': 40, 'ie': 30, 'mek': 40, 'storage': 30,
                 'colony': 30, 'dim': 45, 'eternal': 60, 'life': 20, 'final': 120, 'trials': 0}


def load_content():
    """Импорт регистрирует главы один раз; все правки выполняются над копиями."""
    import dsl
    from rewards import REWARDS
    from polish import INTROS
    from lang_en import EN
    for path in sorted(HERE.glob('c_*.py')):
        importlib.import_module(path.stem)
    chapters, translations = deepcopy(dsl.CHAPTERS), deepcopy(EN)
    known = {c['id'] + '/' + q['id'] for c in chapters for q in c['quests']}
    orphan = sorted(set(REWARDS) - known)
    if orphan:
        raise ValidationError(['Награды без задания: ' + ', '.join(orphan)])
    for c in chapters:
        if c['id'] in INTROS:
            c['intro'] = deepcopy(list(INTROS[c['id']]))
        for q in c['quests']:
            gid = c['id'] + '/' + q['id']
            if gid in REWARDS:
                q['rewards'] = deepcopy(REWARDS[gid])
            r = q.setdefault('rewards', {'items': [], 'xp': 0, 'text': []})
            if r.get('xp', 0) == 0 and q.get('tasks'):
                base = XP_BY_SECTION.get(c['section'], 20)
                r['xp'] = base * 2 if q.get('shape') == 'big' else base
    from progression import apply
    apply(chapters, translations)
    return chapters, translations


def catalog(variable, filename):
    override = os.environ.get(variable)
    if override == '':
        return None
    path = Path(override) if override else HERE / filename
    if override or path.is_file():
        return set(path.read_text(encoding='utf-8').split())
    return None


def compile_book():
    """Возвращает полностью проверенные артефакты; ошибок с частичной записью нет."""
    from lang_en import SECTIONS_EN, SECTIONS_RU, UI_EN, UI_RU
    chapters, translations = load_content()
    validate(chapters, translations, catalog('VALID_IDS', 'valid_ids.txt'),
             catalog('VALID_ADV', 'valid_adv.txt'))
    sections_path = OUT.parent / 'sections.json'
    sections = json.loads(sections_path.read_text(encoding='utf-8'))
    errors = [f"{c['id']}: неизвестный раздел {c['section']}" for c in chapters if c['section'] not in sections]
    for sid in sections:
        if not SECTIONS_RU.get(sid) or not SECTIONS_EN.get(sid):
            errors.append(f'{sid}: отсутствует перевод раздела')
    for key in UI_RU.keys() | UI_EN.keys():
        if not UI_RU.get(key) or not UI_EN.get(key):
            errors.append(f'{key}: отсутствует перевод интерфейса')
    if errors:
        raise ValidationError(errors)
    localized, ru, en = localize(chapters, translations)
    by_section = {}
    for c in localized:
        by_section.setdefault(c['section'], []).append(c)
    artifacts = {OUT / (sid + '.json'): json.dumps(cs, ensure_ascii=False, indent=1)
                 for sid, cs in by_section.items()}
    for sid, section in sections.items():
        key = 'codex.section.' + sid
        ru[key], en[key], section['title'] = SECTIONS_RU[sid], SECTIONS_EN[sid], key
    ru.update(UI_RU)
    en.update(UI_EN)
    lang_dir = OUT.parent.parent / 'lang'
    artifacts[sections_path] = json.dumps(sections, ensure_ascii=False, indent=2)
    for name, strings in [('ru_ru', ru), ('en_us', en)]:
        artifacts[lang_dir / (name + '.json')] = json.dumps(dict(sorted(strings.items())), ensure_ascii=False, indent=1)
    return artifacts


def emit(artifacts, check=False, chapters_dir=None):
    stale = set(chapters_dir.glob('*.json')) - set(artifacts) if chapters_dir else set()
    changed = [p for p, value in artifacts.items() if not p.is_file() or p.read_text(encoding='utf-8') != value]
    if check:
        for p in sorted(set(changed) | stale):
            print(f'Ресурс требует пересборки: {p}')
        return not changed and not stale
    for p in changed:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(artifacts[p], encoding='utf-8')
    for p in stale:
        p.unlink()
    return True


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args(argv)
    try:
        artifacts = compile_book()
        success = emit(artifacts, args.check, OUT)
    except (ValidationError, OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f'Проверено артефактов: {len(artifacts)}')
    return 0 if success else 1


if __name__ == '__main__':
    raise SystemExit(main())
