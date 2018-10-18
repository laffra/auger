class Foo:            # Declare a class with a method
  def foo(self, x):
    return 2 * x

  def foo_get(self):
    return Bar.bar_get()


class Bar:
  @staticmethod
  def bar_get():
    return Bar()


def main():
  foo = Foo()           # Create an instance of Foo
  print(foo.foo(32))    # 64
  print(foo.foo_get())  # Bar instance


if __name__ == '__main__':
  main()