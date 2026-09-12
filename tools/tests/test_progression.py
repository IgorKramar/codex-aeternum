"""Контракт связной книги и совместимость идентификаторов сохранений."""
import sys
from pathlib import Path
import unittest
from collections import defaultdict
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from build_book import load_content


class ProgressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapters, cls.en = load_content()
        cls.quests = {c['id']+'/'+q['id']: q for c in cls.chapters for q in c['quests']}

    def test_original_progress_identifiers_survive(self):
        original = set(Path(__file__).with_name('legacy_quest_ids.txt').read_text().splitlines())
        self.assertEqual(907, len(original))
        self.assertTrue(original <= self.quests.keys())
        self.assertGreater(len(self.quests), len(original))

    def test_map_coordinates_are_unique_with_room_for_big_nodes(self):
        occupied = defaultdict(set)
        for c in self.chapters:
            for q in c['quests']:
                xy = (q['x'], q['y'])
                self.assertNotIn(xy, occupied[c['map']], c['id']+'/'+q['id'])
                occupied[c['map']].add(xy)
        self.assertGreater(len(occupied['create']), 100)

    def test_map_dependencies_always_move_forward(self):
        by_gid = {c['id']+'/'+q['id']: c for c in self.chapters for q in c['quests']}
        for gid, q in self.quests.items():
            for dep in q.get('deps', []) + q.get('any_deps', []):
                target = dep if '/' in dep else gid.split('/')[0]+'/'+dep
                if by_gid[target]['map'] == by_gid[gid]['map']:
                    self.assertLess(self.quests[target]['x'], q['x'], f'{target} -> {gid}')

    def test_choices_and_recipe_order_are_real(self):
        mill = self.quests['story_forge/mill']
        self.assertEqual([], mill['deps'])
        self.assertEqual({'source', 'source_w'}, set(mill['any_deps']))
        precision = self.quests['create_brass/precision']
        self.assertNotIn('arm', precision['deps'])
        self.assertIn('precision', self.quests['create_brass/arm']['deps'])
        self.assertIn('evaporation', self.quests['mek_ore/injection']['deps'])

    def test_industrial_entry_does_not_require_backpack_or_manual_tour(self):
        self.assertEqual(['crafting'], self.quests['start_first_day/iron']['deps'])
        self.assertEqual(['start_first_day/iron'], self.quests['create_basics/andesite']['deps'])

    def test_no_internal_belt_items_or_wrong_nuclear_equipment(self):
        for q in self.quests.values():
            self.assertFalse(any(t.get('id') == 'create:belt' for t in q.get('tasks', [])))
        self.assertNotIn('mekanism:solar_neutron_activator',
                         [t.get('id') for t in self.quests['mek_nuclear/fuel']['tasks']])

    def test_cross_chapter_connections_exist_in_all_advanced_sections(self):
        connected = set()
        for c in self.chapters:
            if any('/' in d for q in c['quests'] for d in q.get('deps', [])+q.get('any_deps', [])):
                connected.add(c['section'])
        self.assertTrue({'create','mek','magic','space','eternal','storage','colony','ie'} <= connected)

    def test_required_path_never_requires_optional_quest(self):
        for gid, q in self.quests.items():
            if q.get('optional'):
                continue
            for dep in q.get('deps', []):
                target = dep if '/' in dep else gid.split('/')[0]+'/'+dep
                self.assertFalse(self.quests[target].get('optional'), f'{gid} requires {target}')

    def test_manual_operation_goals_are_honest_and_optional(self):
        operations = [q for q in self.quests.values() if q['id'].endswith('_run')]
        self.assertGreaterEqual(len(operations), 18)
        for q in operations:
            self.assertTrue(q['optional'])
            self.assertEqual('check', q['tasks'][0]['type'])
            self.assertTrue(q['tasks'][0].get('note', '').strip(), q['id'])


if __name__ == '__main__':
    unittest.main()
