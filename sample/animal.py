import random

class Animal(object):
  def __init__(self, species):
    self.species = species
    self.key = random.randint(0, 100)

  def getSpecies(self):
    return '%s:%s' % (self.species, self.key)

