# auger
Auger is a project to automatically generate unit tests for Python code. 

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
      with auger.UnittestGenerator(pet):
        main() 

This produces the following automatically generated unit test for pet.py:

      from pet import Pet
      from unittest.mock import patch
      import animal
      import pet
      import unittest

      class PetTest(unittest.TestCase):
        @patch.object(Pet, 'getSpecies')
        def test___str__(self, mock_getSpecies):
          mock_getSpecies.return_value = 'Parrot'
          _pet = Pet(species='Parrot',name='Polly')
          self.assertEquals(_pet.__str__(), 'Polly is a Parrot')

        def test_createPet(self):
          self.assertIsInstance(pet.createPet(species='Parrot',name='Polly'), Pet)

        def test_getName(self):
          _pet = Pet(species='Parrot',name='Polly')
          self.assertEquals(_pet.getName(), 'Polly')

      if __name__ == "__main__":
        unittest.main()

Note that auger detects object creation, method invocation, and static methods. As
the getSpecies method is defined by the superclass we mock it out, and make it return
'Parrot', as that is what our test execution produced.

By automatically generating unit tests, we dramatically cut down the cost of software 
development this way. 
