import foo
from foo import Bar
from foo import Foo
import functions
from mock import patch
import os
import os.path
from random import Random
import unittest


class FunctionsTest(unittest.TestCase):
    @patch.object(os.path, 'exists')
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


    @patch.object(os.path, 'isdir')
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
