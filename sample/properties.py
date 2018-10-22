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
  with auger.magic([Language]):
    language = Language()
    print(language.name)
    print(language.age())

if __name__ == '__main__':
  main()