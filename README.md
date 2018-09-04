# Auger
Auger is a project to automatically generate unit tests for Python code.

See
[these slides](http://goo.gl/PuZsgX)
or
[this blog](http://chrislaffra.blogspot.com/2016/12/auger-automatic-unit-test-generation.html)
entry for more information.

# Installation

Install auger with:

    pip install auger-python

# Running Auger
    
To generate a unit test for any class or module, for Python 2 or 3, do this:

    import auger

    with auger.magic([ <any list of modules or classes> ]):
        <any code that exercises your application>

# A Simple Example

Here is a simple example that does not rely on Auger at all:

    class Foo:                # Declare a class with a method
        def bar(self, x):
            return 2 * x .    # Duplicate x and return it

    def main():
        foo = Foo()           # Create an instance of Foo
        print(foo.bar(32))    # Call the bar method and print the result

    main()

Inside the `main` function we call the `bar` method and it will print 64.

# Running Auger on our Simple Example

To generate a unit test for this class, we run the code again, but this time in the context of Auger:

    import auger

    with auger.magic([Foo]):
        main()

This will print out the following:

    64
    Auger: generated test: tests/test_Foo.py

The test that is generated looks like this, with some imports and test for main removed:

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

# Running Auger in verbose mode

Rather than emit tests in the file system, Auger can also print out the test to the console,
by using the `verbose` parameter:

    import auger

    with auger.magic([Foo], verbose=True):
        main()

In that case, Auger will not generate any tests, but just print them out.

# A larger example

Consider the following example, `pet.py`, included in the `sample` folder, that lets us create a `Pet` with a name and a species:

    from animal import Animal

    class Pet(Animal):
      def __init__(self, name, species):
        Animal.__init__(self, species)
        self.name = name

      def getName(self):
        return self.name

      def __str__(self):
        return "%s is a %s" % (self.getName(), self.getSpecies())

    def createPet(name, species):
      return Pet(name, species)

A `Pet` is really a special kind of `Animal`, with a name, which is defined in `animal.py`:

    class Animal(object):
      def __init__(self, species):
        self.species = species

      def getSpecies(self):
        return self.species

With those two definitions, we can create a `Pet` instance and print out some details:

    import animal
    import pet

    def main():
      p = pet.createPet("Polly", "Parrot")
      print(p, p.getName(), p.getSpecies())
      
    main()      

This produces:

    Polly is a Parrot Polly Parrot

# Calling Auger on our larger example

With Auger, we can record all calls to all functions and methods defined in `pet.py`,
while also remembering the details for all calls going out from `pet.py` to other modules,
so they can be mocked out.

Instead of saying:

    if __name__ == "__main__":
      main()

We would say:

    import auger
    
    if __name__ == "__main__":
      with auger.magic([pet]):   # this is the new line and invokes Auger
        main()

This produces the following automatically generated unit test for `pet.py`:

    from mock import patch
    from sample.animal import Animal
    import sample.pet
    from sample.pet import Pet
    import unittest


    class PetTest(unittest.TestCase):
        @patch.object(Animal, 'get_species')
        @patch.object(Animal, 'get_age')
        def test___str__(self, mock_get_age, mock_get_species):
            mock_get_age.return_value = 12
            mock_get_species.return_value = 'Dog'
            pet_instance = Pet('Clifford', 'Dog', 12)
            self.assertEquals(pet_instance.__str__(), 'Clifford is a dog aged 12')

        def test_create_pet(self):
            self.assertIsInstance(sample.pet.create_pet(age=12,species='Dog',name='Clifford'), Pet)

        def test_get_name(self):
            pet_instance = Pet('Clifford', 'Dog', 12)
            self.assertEquals(pet_instance.get_name(), 'Clifford')

        def test_lower(self):
            self.assertEquals(Pet.lower(s='Dog'), 'dog')

    if __name__ == "__main__":
        unittest.main()

Note that auger detects object creation, method invocation, and static methods. It automatically
generate mocks for `Animal`. The mock for `get_species` returns 'Dog' and `get_age` returns 12. 
Namely, those were the values Auger recorded when we ran our sample code the last time.

# Benefits of Auger

By automatically generating unit tests, we dramatically cut down the cost of software
development. The tests themselves are intended to help developers get going on their unit testing
and lower the learning curve for how to write tests.

# Known limitations of Auger

Auger does not do try to substitue parameters with synthetic values such as `-1`, `None`, or `[]`. 
Auger also does not act well when code uses exceptions. Auger also does not like methods that have a decorator.

Auger only records a given execution run and saves the run as a test. Auger does not know if the code actually
works as intended. If the code contains a bug, Auger will simply record the buggy behavior. There is no free
lunch here. It is up to the developer to verify the code actually works.
