import animal
from animal import Animal
from mock import patch
import pet
from pet import Pet
import unittest


class PetTest(unittest.TestCase):
    @patch.object(animal, 'get_age')
    @patch.object(animal, 'get_complex_object')
    @patch.object(animal, 'get_species')
    def test___str__(self, mock_get_species, mock_get_complex_object, mock_get_age):
        mock_get_species.return_value = 'Dog'
        mock_get_complex_object.return_value = Random()
        mock_get_age.return_value = 12
        self.assertEqual(
            pet.__str__,
            'Random Clifford is a dog aged 12'
        )


    def test_create_pet(self):
        self.assertIsInstance(
            pet.create_pet,
            pet.Pet
        )


    def test_get_name(self):
        self.assertEqual(
            pet.get_name,
            'Clifford'
        )


    def test_lower(self):
        self.assertEqual(
            pet.lower,
            'dog'
        )


if __name__ == "__main__":
    unittest.main()
