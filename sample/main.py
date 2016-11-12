import pet

def main():
  clifford = pet.createPet('Clifford', 'Dog', 12)
  print('Clifford is %d years old.' % clifford.getAge())
  print(clifford)

import auger
with auger.magic(pet):
  main()
