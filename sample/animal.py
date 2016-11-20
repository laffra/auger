import random


class Animal(object):
  def __init__(self, species, age=0):
    self._species = species
    self._age = age or random.randint(1, 100)

  def get_species(self):
    return self._species

  def get_age(self):
    return self._age

  def __str__(self):
    return '%s:%s' % (self._species, self._age)


if __name__ == '__main__':
  print(Animal('Dog'))
  print(Animal('Bird', 5))
  print(Animal('Cat').get_species())
