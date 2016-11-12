from animal import Animal

class Pet(Animal):
  def __init__(self, name, *args):
    Animal.__init__(self, *args)
    self._name = name

  def getName(self):
    return self._name

  def __str__(self):
    return '%s is a %s aged %d' % (self.getName(), self.getSpecies(), self.getAge())


def createPet(name, species, age=0):
  return Pet(name, species, age)

if __name__ == '__main__':
	print(Pet('Polly', 'Parrot'))
	print(createPet('Clifford', 'Dog', 32))
