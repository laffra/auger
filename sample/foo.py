class Foo:            # Declare a class with a method
  def bar(self, x):
    return 2 * x

def test():
  foo = Foo()           # Create an instance of Foo
  print(foo.bar(32))    # Print 64

import auger
with auger.magic([Foo]):
  test()