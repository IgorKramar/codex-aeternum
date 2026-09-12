"""Полнота руководства и неизменность ключей прогресса при редактуре."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from guidebook import apply
from book_compiler import ValidationError


class GuidebookTests(unittest.TestCase):
    def setUp(self):
        self.chapters = [{'id':'chapter','section':'s','quests':[
            {'id':'boss','tasks':[{'type':'advancement','id':'mod:kill_boss'}]}]}]
        self.en = {'chapter': {'quests': {'boss': {'title': 'Boss'}}}}
        self.doc = {'section':'s', 'chapters':{'chapter':{'intro':['Введение'], 'intro_en':['Introduction']}},
                    'quests':{'chapter/boss':{'text':['Подготовка','Действие','Результат'],
                        'text_en':['Preparation','Action','Result'],
                        'task_notes':{'0':{'ru':'Победить хранителя','en':'Defeat the guardian'}}}}, 'additions':[]}

    def run_apply(self, document=None):
        with tempfile.TemporaryDirectory() as temp:
            Path(temp,'s.json').write_text(json.dumps(self.doc if document is None else document))
            apply(self.chapters, self.en, Path(temp))

    def test_human_goal_preserves_advancement_key(self):
        self.run_apply()
        task = self.chapters[0]['quests'][0]['tasks'][0]
        self.assertEqual('mod:kill_boss', task['id'])
        self.assertEqual('Победить хранителя', task['note'])
        self.assertEqual(['Defeat the guardian'], self.en['chapter']['quests']['boss']['tasks'])

    def test_no_silent_partial_rewrite_or_extra_quest(self):
        for kind in ['missing', 'extra']:
            with self.subTest(kind=kind):
                doc = copy.deepcopy(self.doc)
                if kind == 'missing':doc['quests'].clear()
                else:doc['quests']['chapter/typo'] = doc['quests']['chapter/boss']
                with self.assertRaises(ValidationError):self.run_apply(doc)

    def test_advancement_needs_action_in_both_languages(self):
        for notes in [{}, {'0':{'ru':'Победить хранителя'}}]:
            doc = copy.deepcopy(self.doc);doc['quests']['chapter/boss']['task_notes'] = notes
            with self.assertRaises(ValidationError):self.run_apply(doc)

    def test_new_branch_requires_description_and_keeps_old_id(self):
        new = {'chapter':'chapter','id':'guide_supply','title':'Запасы','title_en':'Supplies',
               'icon':'minecraft:chest','deps':['boss'],'tasks':[],'optional':True}
        self.doc['additions'] = [new]
        self.doc['quests']['chapter/guide_supply'] = {'text':['Один','Два','Три'],'text_en':['One','Two','Three']}
        self.run_apply()
        self.assertEqual(['boss','guide_supply'],[q['id'] for q in self.chapters[0]['quests']])
        self.assertEqual('Supplies',self.en['chapter']['quests']['guide_supply']['title'])

    def test_missing_section_is_rejected(self):
        self.chapters.append({'id':'other','section':'absent','quests':[]})
        with self.assertRaisesRegex(ValidationError,'Неполный'):self.run_apply()

    def test_empty_intro_is_rejected(self):
        self.doc['chapters']['chapter']['intro_en'] = []
        with self.assertRaisesRegex(ValidationError,'введения'):self.run_apply()

    def test_corrected_reward_and_icon_replace_unobtainable_content(self):
        entry = self.doc['quests']['chapter/boss']
        entry['icon'] = 'minecraft:diamond'
        entry['rewards_override'] = {'xp':10, 'items':[{'id':'minecraft:diamond','count':1}], 'text':[]}
        self.run_apply()
        quest = self.chapters[0]['quests'][0]
        self.assertEqual('minecraft:diamond', quest['icon'])
        self.assertEqual(entry['rewards_override'], quest['rewards'])


if __name__ == '__main__':unittest.main()
