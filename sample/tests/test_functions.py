import animal
from animal import Animal
import functions
import genericpath
from genericpath import unicode
from mock import patch
import os
import pet
from pet import Animal
from pet import Pet
import properties
from properties import Language
import random
from random import Random
import unittest


class FunctionsTest(unittest.TestCase):
    @patch.object(genericpath, 'exists')
    def test_func_one(self, mock_exists):
        mock_exists.return_value = False
        self.assertEqual(
            functions.func_one(),
            False
        )


    def test_func_three(self):
        self.assertEqual(
            functions.func_three(a='C:/temp'),
            False
        )


    @patch.object(genericpath, 'isdir')
    def test_func_two(self, mock_isdir):
        mock_isdir.return_value = False
        self.assertEqual(
            functions.func_two(a='C:/temp'),
            False
        )


    def test_main(self):
        self.assertEqual(
            functions.main(),
            None
        )


if __name__ == "__main__":
    unittest.main()
