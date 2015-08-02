from mpdb import *
import ipdb
import pdb
import zpdb

class Cat():
    def __init__(self):
        self.name = 'kitty'
        self.color = 'black'
        self.size = 'large!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
        self.breed = 'lynx'
        self.tail = 'yes'

class Dog():
    def __init__(self):
        self.name = 'kitty'
        self.color = 'black'
        self.size = 'large!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
        self.breed = 'lynx'
        self.uuid = 'e30475ad-9444-49e7-bc48-e02b25bf7669'


class MyFunc():
    def __init__(self):
        pass

    def run(self):
        test_globals = globals()
        test_none = None
        test_list = [1,2,3,4,5,'birthday_cake']
        dogs = []
        cats = []
        empty_list = []

        num = 0
        for i in range(3):
            num += 1
            dog = Dog()
            dog.name = 'dog-' + str(num)
            dogs.append(dog)

        num = 0
        for i in range(5):
            num += 1
            cat = Cat()
            cat.name = 'kitty-' + str(num)
            cats.append(cat)

        # Call the modified ipd that includes mpdb
        # zpdb.set_trace(locals())

        # Call mpdb by itself, without pdb
        Mpdb.run(locals())


my_func = MyFunc()
my_func.run()
