import auger
import foo
from foo import Foo
import unittest


class FooTest(unittest.TestCase):
    def test_bar(self):
        foo_instance = Foo()
        self.assertEquals(
            foo_instance.bar(x=32),
            64
        )


    def test_test(self):
        self.assertEquals(
            foo.test(),
            None
        )


if __name__ == "__main__":
    unittest.main()
