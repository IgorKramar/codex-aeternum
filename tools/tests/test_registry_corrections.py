"""Блоки без предметной формы не должны блокировать прохождение книги."""
import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from build_book import load_content
from book_compiler import validate
from registry_corrections import ITEM_REPLACEMENTS, MANUAL


class RegistryCorrectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapters, cls.en = load_content()
        cls.quests = {c['id']+'/'+q['id']: q for c in cls.chapters for q in c['quests']}

    def test_no_known_missing_items_in_goals_rewards_or_icons(self):
        used = set()
        for c in self.chapters:
            used.add(c['icon'])
            for q in c['quests']:
                used.add(q['icon'])
                used.update(t['id'] for t in q.get('tasks', []) if t['type'] == 'item')
                used.update(t['id'] for t in q.get('rewards', {}).get('items', []))
        self.assertFalse(used & (ITEM_REPLACEMENTS.keys() | {'create_radar:radio'}))
        catalog = set(Path(__file__).resolve().parents[1].joinpath("valid_ids.txt").read_text().splitlines())
        validate(self.chapters, self.en, valid_ids=catalog)

    def test_world_operations_are_manual_and_translated(self):
        for gid, (identifier, ru_note, en_note) in MANUAL.items():
            q = self.quests[gid]
            cid, qid = gid.split('/')
            matching = [(i, t) for i, t in enumerate(q['tasks']) if t['id'] == identifier]
            self.assertEqual(1, len(matching), gid)
            i, task = matching[0]
            self.assertEqual('check', task['type'])
            self.assertEqual(ru_note, task['note'])
            self.assertEqual(en_note, self.en[cid]['quests'][qid]['tasks'][i])
        self.assertEqual('create:railway_casing', self.quests['create_trains/bogey']['tasks'][0]['id'])

    def test_submission_still_consumes_caps_and_reward_has_real_items(self):
        caps = self.quests['more_rails/depot']['tasks'][1]
        self.assertEqual(('railways:blue_conductor_cap', 4, True),
                         (caps['id'], caps['count'], caps['consume']))
        self.assertEqual([{'id': 'create:railway_casing', 'count': 10}],
                         self.quests['story_forge/train']['rewards']['items'])
        drill = self.quests['cbc_foundry/drill']['tasks']
        self.assertIn('createbigcannons:cast_iron_cannon_barrel', [t['id'] for t in drill])


if __name__ == '__main__':
    unittest.main()
