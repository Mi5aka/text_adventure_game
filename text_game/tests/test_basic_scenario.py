import unittest
from unittest.mock import patch

from text_game.scenarios import Scenario


class TestScenario(unittest.TestCase):

    def setUp(self):
        self.game = Scenario()
        self.covid_ending = [
            '', '2', '', '1', '', '1', '', '2', '', '2', 'да', 'нет'
        ]
        self.friend_ending = [
            '', '3', '', '1', '', '1', '', '2', '', '2', 'нет', '', '2', '',
            '1', '', 'да', '', '1', '', '2'
        ]
        self.happy_ending = [
            '', '3', '', '1', '', '1', '', '2', '', '2', 'нет', '', '2', '',
            '1', '', 'нет', '', 'нет', '', '2', '', '2', '', '3', '', '2', '',
            '3', '', '3', 'нет'
        ]
        self.bad_ending = [
            '', '1', '', '2', '', '2', '', '1', '', '3', 'нет', '', '2', '',
            'нет', '', '2'
        ]

    def test_covid_ending(self):
        with patch('builtins.input', side_effect=self.covid_ending):
            self.game.start()
        self.assertEqual(self.game.mental_health, 55)

    def test_friend_ending(self):
        with patch('builtins.input', side_effect=self.friend_ending):
            self.game.start()
        self.assertEqual(self.game.mental_health, 54)

    def test_happy_ending(self):
        with patch('builtins.input', side_effect=self.happy_ending):
            self.game.start()
        self.assertEqual(self.game.mental_health, 43)

    def test_bad_ending(self):
        with patch('builtins.input', side_effect=self.bad_ending):
            self.game.start()
        self.assertEqual(self.game.mental_health, 0)
