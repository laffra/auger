import __main__
from foo import Foo
import auger
import unittest


class FooTest(unittest.TestCase):
    def test_bar(self):
        foo_instance = Foo()
        self.assertEquals(
            foo_instance.bar(x=32),
            64
        )


if __name__ == "__main__":
    unittest.main()
