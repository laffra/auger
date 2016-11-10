import animal
import pet

import auger

def main():
  p = pet.createPet("Polly", "Parrot")
  print(p, p.getName(), p.getSpecies())

  p = pet.createPet("Clifford", "Dog")
  print(p, p.getName(), p.getSpecies())

if __name__ == "__main__":
  with auger.UnittestGenerator(pet):
    main() 
