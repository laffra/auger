import animal, pet

def main():
    clifford = pet.create_pet('Clifford', 'Dog', 12)
    print('This dog is %d years old.' % clifford.get_age())
    print(clifford)

if __name__ == '__main__':
    main()
