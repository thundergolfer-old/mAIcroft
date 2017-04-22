import unittest
from maicroft.text_parser import TextParser

class TestTextParser(unittest.TestCase):

    def setUp(self):
        self.TP = TextParser()

    def test_normalize(self):
        assert "gathering" == self.TP.normalize("gatherings")

    def test_pet_animal(self):
        animal_test_list = [
            'dog', 'cat', 'hamster', 'fish', 'pig', 'snake',
            'rat', 'parrot'
        ]
        assert all(self.TP.pet_animal(w) for w in animal_test_list)

    def test_family_member(self):
        family_test_list = [
            'mom', 'mother', 'dad', 'brother', 'sister'
        ]
        assert all(self.TP.family_member(w) for w in family_test_list)
