import animal
from animal import Animal
import foo
from foo import Bar
from foo import Foo
from mock import patch
import pet
from pet import Animal
from pet import Pet
import properties
from properties import Language
import random
from random import Random
import unittest


class FooTest(unittest.TestCase):
    def test_bar_get(self):
        self.assertIsInstance(
            Bar.bar_get(),
            foo.Bar
        )


    def test_foo(self):
        foo_instance = Foo()
        self.assertEqual(
            foo_instance.foo(x=32),
            64
        )


    def test_foo_get(self):
        foo_instance = Foo()
        self.assertIsInstance(
            foo_instance.foo_get(),
            foo.Bar
        )


    def test_main(self):
        self.assertEqual(
            foo.main(),
            None
        )


if __name__ == "__main__":
    unittest.main()
