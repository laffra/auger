import os

def func_one():
    return os.path.exists('C:/temp')

def func_two(a):
    return os.path.isdir(a)

def func_three(a):
    return func_two(a)

def main():
    print func_one()
    print func_two('C:/temp')
    print func_three('C:/temp')

if __name__ == '__main__':
    main()
