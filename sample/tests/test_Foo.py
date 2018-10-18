import foo
from foo import Foo
import unittest


class FooTest(unittest.TestCase):
    def test_foo(self):
        foo_instance = Foo()
        self.assertEquals(
            foo_instance.foo(x=32),
            64
        )


    def test_foo_get(self):
        foo_instance = Foo()
        self.assertIsInstance(
            foo_instance.foo_get(),
            foo.Bar
        )


if __name__ == "__main__":
    unittest.main()
