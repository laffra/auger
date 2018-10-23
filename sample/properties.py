import auger

class Language(object):

  def __init__(self):
    pass

  @property
  def name(self):
    return "Python"

  def age(self):
    return 26

def main():
  language = Language()
  print("Language:", language.name)
  print("Language:", language.age())

if __name__ == '__main__':
  main()