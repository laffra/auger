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
