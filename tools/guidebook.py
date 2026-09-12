"""Полная авторская редакция: содержание, дополнительные ветки, человеческие цели."""
from copy import deepcopy
import json
from pathlib import Path

from book_compiler import ValidationError

GUIDES = Path(__file__).with_name('guides')


def apply(chapters, translations, directory=GUIDES):
    by_chapter = {c['id']: c for c in chapters}
    sections = {c['section'] for c in chapters}
    documents = {}
    for path in sorted(directory.glob('*.json')):
        doc = json.loads(path.read_text(encoding='utf-8'))
        section = doc['section']
        if section in documents:
            raise ValidationError([f'Повтор руководства: {section}'])
        documents[section] = doc
    if documents.keys() != sections:
        raise ValidationError([f'Неполный набор руководств: нет {sorted(sections-documents.keys())}; лишние {sorted(documents.keys()-sections)}'])
    for section, doc in documents.items():
        for addition in doc.get('additions', []):
            q = deepcopy(addition)
            cid, en_title = q.pop('chapter'), q.pop('title_en')
            if cid not in by_chapter or by_chapter[cid]['section'] != section:
                raise ValidationError([f'Новая ветка {cid}/{q["id"]} относится к другой карте'])
            if any(old['id'] == q['id'] for old in by_chapter[cid]['quests']):
                raise ValidationError([f'Повтор задания: {cid}/{q["id"]}'])
            q['x'], q['y'] = 0, 0  # Общий layout назначает координаты после всех дополнений.
            by_chapter[cid]['quests'].append(q)
            translations[cid]['quests'][q['id']] = {'title': en_title}
        expected_chapters = {c['id'] for c in chapters if c['section'] == section}
        if doc['chapters'].keys() != expected_chapters:
            raise ValidationError([f'{section}: введения охватывают не все главы'])
        expected = {c['id']+'/'+q['id'] for c in chapters if c['section'] == section for q in c['quests']}
        if doc['quests'].keys() != expected:
            raise ValidationError([f'{section}: нет описаний {sorted(expected-doc["quests"].keys())}; лишние {sorted(doc["quests"].keys()-expected)}'])
        for cid in expected_chapters:
            c = by_chapter[cid]
            intro = doc['chapters'][cid]
            if any(not isinstance(intro.get(key), list) or not intro[key]
                   or any(not isinstance(p, str) or not p.strip() for p in intro[key])
                   for key in ('intro', 'intro_en')):
                raise ValidationError([f'{cid}: нужны введения на обоих языках'])
            c['intro'] = list(intro['intro'])
            translations[cid]['intro'] = list(intro['intro_en'])
            for q in c['quests']:
                gid = cid+'/'+q['id']
                entry = doc['quests'][gid]
                en = translations[cid]['quests'][q['id']]
                for field, target in [('text', q), ('text_en', en)]:
                    paragraphs = entry[field]
                    if not isinstance(paragraphs, list) or len(paragraphs) < 3 or any(not isinstance(p, str) or not p.strip() for p in paragraphs):
                        raise ValidationError([f'{gid}: нужны содержательные абзацы на обоих языках'])
                    target['text'] = list(paragraphs)
                for field in ('tasks', 'deps', 'rewards'):
                    if field+'_override' in entry:
                        q[field] = deepcopy(entry[field+'_override'])
                if 'title' in entry:
                    q['title'], en['title'] = entry['title'], entry['title_en']
                if 'icon' in entry:
                    q['icon'] = entry['icon']
                notes = entry.get('task_notes', {})
                if any(not index.isdigit() or int(index) >= len(q.get('tasks', [])) for index in notes):
                    raise ValidationError([f'{gid}: неверный индекс пояснения цели'])
                en_notes = list(en.get('tasks', []))
                en_notes += [''] * max(0, len(q.get('tasks', []))-len(en_notes))
                for i, task in enumerate(q.get('tasks', [])):
                    note = notes.get(str(i))
                    if note is not None:
                        if not note.get('ru') or not note.get('en'):
                            raise ValidationError([f'{gid}: неполный перевод цели {i}'])
                        task['note'], en_notes[i] = note['ru'], note['en']
                    if task.get('type') == 'advancement' and note is None:
                        raise ValidationError([f'{gid}: достижению нужна человеческая формулировка'])
                en['tasks'] = en_notes
