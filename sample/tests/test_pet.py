import animal
from animal import Animal
import foo
from foo import Foo
from mock import patch
import pet
from pet import Pet
import random
from random import Random
import unittest


class PetTest(unittest.TestCase):
    @patch.object(Animal, 'get_age')
    @patch.object(Animal, 'get_complex_object')
    @patch.object(Animal, 'get_species')
    def test___str__(self, mock_get_species, mock_get_complex_object, mock_get_age):
        mock_get_species.return_value = 'Dog'
        mock_get_complex_object.return_value = Random()
        mock_get_age.return_value = 12
        pet_instance = Pet('Clifford', 'Dog', 12)
        self.assertEquals(
            pet_instance.__str__(),
            'Random Clifford is a dog aged 12'
        )


    def test_get_name(self):
        pet_instance = Pet('Clifford', 'Dog', 12)
        self.assertEquals(
            pet_instance.get_name(),
            'Clifford'
        )


if __name__ == "__main__":
    unittest.main()
