import auger
from sample import pet


def main() -> object:
    clifford = pet.create_pet('Clifford', 'Dog', 12)
    print('Clifford is %d years old.' % clifford.get_age())
    print(clifford)


with auger.magic([pet]):
    main()
