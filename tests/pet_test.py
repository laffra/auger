from unittest.mock import patch
import unittest
from sample import pet

class PetTest(unittest.TestCase):
  @patch.object(pet.Pet, 'get_species')
  @patch.object(pet.Pet, 'get_age')
  def test___str__(self, mock_get_age, mock_get_species):
    mock_get_age.return_value = 12
    mock_get_species.return_value = 'Dog'
    pet_instance = pet.Pet('Clifford', 'Dog', 12)
    self.assertEquals(pet_instance.__str__(), 'Clifford is a dog aged 12')

  def test_create_pet(self):
    self.assertIsInstance(pet.create_pet(age=12,species='Dog',name='Clifford'), pet.Pet)

  def test_get_name(self):
    pet_instance = pet.Pet('Clifford', 'Dog', 12)
    self.assertEquals(pet_instance.get_name(), 'Clifford')

  def test_lower(self):
    self.assertEquals(pet.Pet.lower(s='Dog'), 'dog')

if __name__ == "__main__":
  unittest.main()
