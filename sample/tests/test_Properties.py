import animal
from animal import Animal
from mock import patch
import properties
from properties import Language
import random
from random import Random
import unittest


class PropertiesTest(unittest.TestCase):
    def test_age(self):
        language_instance = Language()
        self.assertEqual(
            language_instance.age(),
            26
        )


    def test_main(self):
        nonetype_instance = NoneType()
        self.assertEqual(
            nonetype_instance.main,
            None
        )


    def test_name(self):
        language_instance = Language()
        self.assertEqual(
            language_instance.name,
            'Python'
        )


if __name__ == "__main__":
    unittest.main()
