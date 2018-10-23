import animal
from animal import Animal
from mock import patch
import pet
from pet import Pet
import random
import unittest


class AnimalTest(unittest.TestCase):
    def test_get_age(self):
        self.assertEqual(
            animal.get_age,
            12
        )


    @patch.object(random, '__init__')
    def test_get_complex_object(self, mock___init__):
        mock___init__.return_value = None
        self.assertIsInstance(
            animal.get_complex_object,
            random.Random
        )


    def test_get_species(self):
        self.assertEqual(
            animal.get_species,
            'Dog'
        )


if __name__ == "__main__":
    unittest.main()
