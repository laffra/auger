import random
from sample.animal import Animal
import unittest


class AnimalTest(unittest.TestCase):
    def test_get_age(self):
        animal_instance = Animal('Dog', 12)
        self.assertEquals(
            animal_instance.get_age(),
            12
        )

        animal_instance = Animal('Dog', 12)
        self.assertEquals(
            animal_instance.get_age(),
            12
        )

        animal_instance = Animal('Dog', 12)
        self.assertEquals(
            animal_instance.get_age(),
            12
        )

    def test_get_species(self):
        animal_instance = Animal('Dog', 12)
        self.assertEquals(
            animal_instance.get_species(),
            'Dog'
        )

        animal_instance = Animal('Dog', 12)
        self.assertEquals(
            animal_instance.get_species(),
            'Dog'
        )

if __name__ == "__main__":
    unittest.main()