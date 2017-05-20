from mock import patch
import random
from sample.animal import Animal
import sample.pet
from sample.pet import Pet
import unittest


class PetTest(unittest.TestCase):
    @patch.object(Animal, 'get_species')
    @patch.object(Animal, 'get_age')
    def test___str__(self, mock_get_age, mock_get_species):
        mock_get_age.return_value = 12
        mock_get_species.return_value = 'Dog'
        pet_instance = Pet('Clifford', 'Dog', 12)
        self.assertEquals(
            pet_instance.__str__(),
            'Clifford is a dog aged 12'
        )

    def test_create_pet(self):
        self.assertIsInstance(
            sample.pet.create_pet(age=12,name='Clifford',species='Dog'),
            Pet
        )

    def test_get_name(self):
        pet_instance = Pet('Clifford', 'Dog', 12)
        self.assertEquals(
            pet_instance.get_name(),
            'Clifford'
        )

    def test_lower(self):
        self.assertEquals(
            Pet.lower(s='Dog'),
            'dog'
        )

if __name__ == "__main__":
    unittest.main()