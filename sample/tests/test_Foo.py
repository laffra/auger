import animal
from animal import Animal
import foo
from mock import patch
import pet
from pet import Pet
import random
import unittest


class FooTest(unittest.TestCase):
    def test_bar_get(self):
        self.assertIsInstance(
            foo.bar_get,
            foo.Bar
        )


    def test_foo(self):
        self.assertEqual(
            foo.foo,
            64
        )


    def test_foo_get(self):
        self.assertIsInstance(
            foo.foo_get,
            foo.Bar
        )


    def test_main(self):
        self.assertEqual(
            foo.main,
            None
        )


if __name__ == "__main__":
    unittest.main()
