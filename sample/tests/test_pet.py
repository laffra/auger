import animal
from animal import Animal
import foo
from foo import Bar
from foo import Foo
from mock import patch
import pet
from pet import Pet
import properties
from properties import Language
import random
from random import Random
import unittest


class PetTest(unittest.TestCase):
    @patch.object(Animal, 'get_species')
    @patch.object(Animal, 'get_age')
    @patch.object(Animal, 'get_complex_object')
    def test___str__(self, mock_get_complex_object, mock_get_age, mock_get_species):
        mock_get_complex_object.return_value = Random()
        mock_get_age.return_value = 12
        mock_get_species.return_value = 'Dog'
        pet_instance = Pet('Clifford', 'Dog', 12)
        self.assertEqual(
            pet_instance.__str__(),
            'Random Clifford is a dog aged 12'
        )


    def test_create_pet(self):
        self.assertIsInstance(
            pet.create_pet,
            pet.Pet
        )


    def test_get_name(self):
        pet_instance = Pet('Clifford', 'Dog', 12)
        self.assertEqual(
            pet_instance.get_name(),
            'Clifford'
        )


    def test_lower(self):
        self.assertEqual(
            Pet.lower,
            'dog'
        )


if __name__ == "__main__":
    unittest.main()
