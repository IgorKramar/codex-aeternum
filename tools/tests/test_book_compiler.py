"""Проверки контракта компилятора без Minecraft и записи ресурсов."""
import copy
import importlib
import pathlib
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))


class CompilerTests(unittest.TestCase):
    def setUp(self):
        self.compiler = importlib.import_module('book_compiler')
        self.chapters = [dict(id='a', section='s', title='А', icon='m:i', quests=[
            dict(id='one', title='Один', icon='m:i', x=0, y=0, tasks=[dict(type='item', id='m:i', count=1)])]),
            dict(id='b', section='s', title='Б', icon='m:i', quests=[
            dict(id='two', title='Два', icon='m:i', x=0, y=0, deps=['a/one'])])]
        self.en = {'a': {'title': 'A', 'quests': {'one': {'title': 'One'}}},
                   'b': {'title': 'B', 'quests': {'two': {'title': 'Two'}}}}

    def validate(self):
        self.compiler.validate(self.chapters, self.en, valid_ids={'m:i'})

    def test_global_dependency_is_valid(self):
        self.validate()

    def test_wrong_chapter_cannot_resolve_local_id(self):
        self.chapters[1]['quests'][0]['deps'] = ['missing/two']
        with self.assertRaisesRegex(self.compiler.ValidationError, 'missing/two'):
            self.validate()

    def test_cycle_through_any_dependency(self):
        self.chapters[0]['quests'][0]['any_deps'] = ['b/two']
        with self.assertRaisesRegex(self.compiler.ValidationError, 'цикл'):
            self.validate()

    def test_duplicate_coordinates_and_ids(self):
        self.chapters[0]['quests'].append(copy.deepcopy(self.chapters[0]['quests'][0]))
        with self.assertRaises(self.compiler.ValidationError) as cm:
            self.validate()
        self.assertIn('координат', str(cm.exception))
        self.assertIn('дубликат', str(cm.exception))

    def test_bad_task_reward_and_missing_translation(self):
        q = self.chapters[0]['quests'][0]
        q['tasks'] += [dict(type='unknown', id='m:i'), dict(type='item', id='bad:id', count=0)]
        q['rewards'] = {'xp': -1, 'items': [{'id': 'm:i', 'count': -1}]}
        q['text'] = ['Нет перевода']
        with self.assertRaises(self.compiler.ValidationError) as cm:
            self.validate()
        for part in ('unknown', 'count', 'xp', 'bad:id', 'перевод'):
            self.assertIn(part, str(cm.exception))

    def test_consume_requires_item_task(self):
        for kind in ('check', 'advancement', 'dimension', 'biome', 'ponder'):
            with self.subTest(kind=kind):
                self.chapters[0]['quests'][0]['tasks'] = [dict(type=kind, id='m:i', consume=True)]
                with self.assertRaisesRegex(self.compiler.ValidationError, 'consume'):
                    self.validate()

    def test_java_integer_bounds_for_tasks_and_rewards(self):
        q = self.chapters[0]['quests'][0]
        limit = 2**31 - 1
        q['tasks'][0]['count'] = limit
        q['rewards'] = {'xp': limit, 'items': [{'id': 'm:i', 'count': limit}]}
        self.validate()
        for container, field in ((q['tasks'][0], 'count'), (q['rewards'], 'xp'),
                                 (q['rewards']['items'][0], 'count')):
            with self.subTest(field=field, container=container):
                container[field] = limit + 1
                with self.assertRaisesRegex(self.compiler.ValidationError, field):
                    self.validate()
                container[field] = limit
        q['tasks'] = [dict(type='check', id='manual', count=0)]
        with self.assertRaisesRegex(self.compiler.ValidationError, 'count'):
            self.validate()

    def test_consumed_sum_is_bounded_per_item_and_quest(self):
        q = self.chapters[0]['quests'][0]
        q['tasks'] = [dict(type='item', id='m:i', count=2**31 - 2, consume=True),
                      dict(type='item', id='m:i', count=1, consume=True),
                      dict(type='item', id='m:i', count=2**31 - 1)]
        self.validate()  # Non-consuming possession checks do not add to consumption.
        q['tasks'][1]['count'] = 2
        with self.assertRaisesRegex(self.compiler.ValidationError, 'сумма.*m:i'):
            self.validate()
        q['tasks'][1]['id'] = 'm:other'
        self.compiler.validate(self.chapters, self.en)

    def test_duplicate_chapters_and_advancement_catalog(self):
        self.chapters.append(copy.deepcopy(self.chapters[0]))
        self.chapters[0]['quests'][0]['tasks'] = [dict(type='advancement', id='m:missing')]
        with self.assertRaises(self.compiler.ValidationError) as cm:
            self.compiler.validate(self.chapters, self.en, valid_adv=set())
        self.assertIn('дубликат главы', str(cm.exception))
        self.assertIn('m:missing', str(cm.exception))

    def test_empty_any_dependency_does_not_add_a_gate(self):
        self.chapters[0]['quests'][0]['any_deps'] = []
        self.validate()

    def test_current_content_validates_without_mutation(self):
        builder = importlib.import_module('build_book')
        chapters, translations = builder.load_content()
        before = copy.deepcopy(chapters)
        self.compiler.validate(chapters, translations,
                               builder.catalog('VALID_IDS', 'valid_ids.txt'),
                               builder.catalog('VALID_ADV', 'valid_adv.txt'))
        self.compiler.localize(chapters, translations)
        self.assertEqual(before, chapters)
        self.assertGreater(sum(len(c['quests']) for c in chapters), 900)

    def test_build_validation_precedes_emission(self):
        builder = importlib.import_module('build_book')
        self.chapters[0]['quests'][0]['deps'] = ['missing']
        with patch.object(builder, 'load_content', return_value=(self.chapters, self.en)), \
             patch.object(builder, 'emit') as emit:
            self.assertEqual(builder.main([]), 1)
            emit.assert_not_called()

    def test_localization_does_not_mutate_source(self):
        before = copy.deepcopy(self.chapters)
        localized, ru, en = self.compiler.localize(self.chapters, self.en)
        self.assertEqual(before, self.chapters)
        self.assertEqual(localized[0]['title'], 'codex.chapter.a.title')
        self.assertEqual(en['codex.quest.b.two.title'], 'Two')

    def test_import_and_repeated_load_are_safe(self):
        builder = importlib.import_module('build_book')
        first, translations = builder.load_content()
        second, _ = builder.load_content()
        self.assertEqual(first, second)
        first[0]['title'] = 'mutated'
        third, _ = builder.load_content()
        self.assertEqual(second, third)

    def test_check_and_validation_never_write(self):
        builder = importlib.import_module('build_book')
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            target = root / 'test.json'
            target.write_text('old')
            self.assertFalse(builder.emit({target: 'new'}, check=True))
            self.assertEqual(target.read_text(), 'old')
            self.chapters[0]['quests'][0]['deps'] = ['missing']
            with self.assertRaises(self.compiler.ValidationError):
                self.compiler.localize(self.chapters, self.en)
            self.assertEqual(target.read_text(), 'old')


if __name__ == '__main__':
    unittest.main()
