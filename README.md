# auger
Auger is a project to automatically generate unit tests for Python code. 

See
[these slides](http://goo.gl/PuZsgX) 
or
[this blog](http://chrislaffra.blogspot.com/2016/12/auger-automatic-unit-test-generation.html)
entry for more information.

Consider the following example, pet.py, that lets us create a Pet with a name and a species:

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

A Pet is really a special kind of animal, with a name, defined in animal.py.

    class Animal(object):
      def __init__(self, species):
        self.species = species
    
      def getSpecies(self):
        return self.species   
    
With those two definitions, we can create a Pet and print it out:
    
    import animal
    import pet
    
    def main():
      p = pet.createPet("Polly", "Parrot")
      print(p, p.getName(), p.getSpecies())
    
This produces:

    Polly is a Parrot Polly Parrot
    
With auger, we can record all calls to all functions and methods defined in pet.py,
while trapping all calls going out from pet.py to other modules.

Instead of saying:

    if __name__ == "__main__":
      main() 

We would say:

    import auger
    if __name__ == "__main__":
      with auger.magic([pet]):
        main() 

This produces the following automatically generated unit test for pet.py:

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

Note that auger detects object creation, method invocation, and static methods. As
the getSpecies method is defined by the superclass, we mock it out, and make it return
'Parrot', as that is what our test execution produced.

By automatically generating unit tests, we dramatically cut down the cost of software 
development this way. 
