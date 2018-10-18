import __main__
import auger
from properties import Language
import unittest


class PropertiesTest(unittest.TestCase):
    def test_age(self):
        language_instance = Language()
        self.assertEquals(
            language_instance.age(),
            26
        )


    def test_name(self):
        language_instance = Language()
        self.assertEquals(
            language_instance.name,
            'Python'
        )


if __name__ == "__main__":
    unittest.main()
