#1
class Person:
  def __init__(self, fname, lname):
    self.firstname = fname
    self.lastname = lname

  def printname(self):
    print(self.firstname, self.lastname)
x = Person("Kairat", "Barsa")
x.printname()
#2
class Student(Person):
  def __init__(self, fname, lname):
    super().__init__(fname, lname)
# 3
class Animal:
    def speak(self):
        print("Some sound")
class Dog(Animal):
    pass
Dog().speak()  

# 4
class Vehicle:
    def wheels(self):
        print("4 wheels")
class Car(Vehicle):
    pass
Car().wheels()  
#5
class Fruit:
    def color(self):
        print("Unknown")
class Apple(Fruit):
    pass
Apple().color()  
#6
class Animal:
    def __init__(self, name):
        self.name = name
class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)
        self.breed = breed
Dog("Buddy", "Beagle")

# 7
class Vehicle:
    def __init__(self, brand):
        self.brand = brand
class Car(Vehicle):
    def __init__(self, brand, model):
        super().__init__(brand)
        self.model = model


