import foo
from foo import Bar
from foo import Foo
import functions
from mock import patch
import os
import os.path
import properties
from properties import Language
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
        pass


    def test_name(self):
        language_instance = Language()
        self.assertEqual(
            language_instance.name,
            'Python'
        )


if __name__ == "__main__":
    unittest.main()
