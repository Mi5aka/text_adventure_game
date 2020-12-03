import unittest
from unittest.mock import patch

from game.scenarios import Scenario
from game.scenarios import States


class TestBasicScenario(unittest.TestCase):

    def setUp(self):
        self.game = Scenario()

    def test_start_method(self):
        self.game.start()
        self.assertEqual(self.game.state, States.BIRTHDAY)

    def test_happy_birthday_method(self):
        self.game.state = States.BIRTHDAY
        with patch('builtins.input', return_value='1'):
            self.game.happy_birthday()
        self.assertEqual(self.game.mental_health, 99)
        self.assertEqual(self.game.state, 'win')
