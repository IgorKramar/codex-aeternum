"""Чистые проверка и локализация книги. Файлы и глобальный DSL не изменяются."""
from copy import deepcopy
import math

INT_MAX = 2**31 - 1


class ValidationError(ValueError):
    def __init__(self, errors):
        self.errors = errors
        super().__init__('Ошибки книги:\n' + '\n'.join(errors))


def text_fields(chapters, translations):
    """Выдаёт изменяемое поле, ключ перевода и английский текст."""
    for c in chapters:
        en_c = translations.get(c['id'], {})
        base = 'codex.chapter.' + c['id']
        yield c, 'title', base + '.title', en_c.get('title')
        if c.get('subtitle'):
            yield c, 'subtitle', base + '.subtitle', en_c.get('subtitle')
        for i in range(len(c.get('intro', []))):
            en = en_c.get('intro') or []
            yield c['intro'], i, f'{base}.intro.{i}', en[i] if i < len(en) else None
        for q in c['quests']:
            en_q = en_c.get('quests', {}).get(q['id'], {})
            qb = f"codex.quest.{c['id']}.{q['id']}"
            yield q, 'title', qb + '.title', en_q.get('title')
            for field, key, values in [('text', 'text', q.get('text', [])),
                                       ('rewards', 'reward', q.get('rewards', {}).get('text', []))]:
                en = en_q.get(field) or []
                for i in range(len(values)):
                    yield values, i, f'{qb}.{key}.{i}', en[i] if i < len(en) else None
            en = en_q.get('tasks') or []
            for i, task in enumerate(q.get('tasks', [])):
                if task.get('note'):
                    yield task, 'note', f'{qb}.task.{i}', en[i] if i < len(en) else None


def validate(chapters, translations, valid_ids=None, valid_adv=None):
    errors, chapter_ids, quests = [], set(), {}
    def fail(where, message):
        errors.append(f'{where}: {message}')
    def item(where, identifier):
        if valid_ids is not None and identifier not in valid_ids:
            fail(where, f'неизвестный предмет {identifier}')
    def integer(where, field, value, minimum):
        if type(value) is not int or not minimum <= value <= INT_MAX:
            fail(where, f'{field} должен быть целым от {minimum} до {INT_MAX}: {value}')
            return False
        return True
    for c in chapters:
        cid = c['id']
        if cid in chapter_ids:
            fail(cid, 'дубликат главы')
        chapter_ids.add(cid)
        item(cid, c['icon'])
        positions = {}
        for q in c['quests']:
            gid = cid + '/' + q['id']
            if gid in quests:
                fail(gid, 'дубликат задания')
            quests[gid] = q
            position = (q.get('x'), q.get('y'))
            if not all(type(n) in (int, float) and math.isfinite(n) for n in position):
                fail(gid, 'координаты должны быть конечными числами')
            elif position in positions:
                fail(gid, f'совпадение координат с {positions[position]}')
            else:
                positions[position] = gid
            item(gid, q['icon'])
            consumed = {}
            for t in q.get('tasks', []):
                kind = t.get('type', 'item')
                if kind not in {'item', 'advancement', 'dimension', 'biome', 'check', 'ponder'}:
                    fail(gid, f'неизвестный тип цели {kind}')
                if kind in {'item', 'ponder'}:
                    item(gid, t.get('id'))
                amount = t.get('count', 1)
                valid_count = integer(gid, 'count', amount, 1)
                consume = t.get('consume', False)
                if type(consume) is not bool:
                    fail(gid, 'consume должен быть логическим значением')
                if consume and kind != 'item':
                    fail(gid, 'consume допустим только для предметов')
                if consume and kind == 'item' and valid_count:
                    identifier = t.get('id')
                    consumed[identifier] = consumed.get(identifier, 0) + amount
                    if consumed[identifier] > INT_MAX:
                        fail(gid, f'сумма сдаваемых предметов {identifier} превышает {INT_MAX}')
                if kind == 'advancement' and valid_adv is not None and t.get('id') not in valid_adv:
                    fail(gid, f"неизвестное достижение {t.get('id')}")
            rewards = q.get('rewards', {})
            xp = rewards.get('xp', 0)
            integer(gid, 'xp', xp, 0)
            for stack in rewards.get('items', []):
                item(gid, stack.get('id'))
                integer(gid + ' награда', 'count', stack.get('count', 1), 1)
    graph = {}
    for gid, q in quests.items():
        edges = []
        for kind in ('deps', 'any_deps'):
            values = q.get(kind, [])
            if not isinstance(values, list):
                fail(gid, f'{kind} должен быть списком')
                continue
            for dep in values:
                if not isinstance(dep, str) or not dep:
                    fail(gid, f'некорректная зависимость {dep!r}')
                    continue
                target = dep if '/' in dep else gid.split('/')[0] + '/' + dep
                if target not in quests:
                    fail(gid, f'неизвестная зависимость {dep}')
                else:
                    edges.append(target)
        graph[gid] = edges
    # Итеративный DFS выдерживает длинные цепочки, не упираясь в лимит Python.
    state = {}
    for start in graph:
        if state.get(start):
            continue
        state[start] = 1
        stack = [(start, iter(graph[start]))]
        while stack:
            node, edges = stack[-1]
            target = next(edges, None)
            if target is None:
                state[node] = 2
                stack.pop()
            elif state.get(target) == 1:
                fail(node, f'цикл зависимости через {target}')
            elif not state.get(target):
                state[target] = 1
                stack.append((target, iter(graph[target])))
    for container, field, key, english in text_fields(chapters, translations):
        if not isinstance(english, str) or not english.strip():
            fail(key, 'отсутствует английский перевод')
        if not isinstance(container[field], str) or not container[field].strip():
            fail(key, 'отсутствует русский текст')
    if errors:
        raise ValidationError(errors)


def localize(chapters, translations):
    validate(chapters, translations)
    localized, ru, en = deepcopy(chapters), {}, {}
    for container, field, key, english in text_fields(localized, translations):
        ru[key], en[key] = container[field], english
        container[field] = key
    return localized, ru, en
