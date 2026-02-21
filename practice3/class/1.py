#1
class MyClass:
  x = 5
#2
p1 = MyClass()
print(p1.x)
#3
p1 = MyClass()
p2 = MyClass()
p3 = MyClass()

print(p1.x)
print(p2.x)
print(p3.x)
#4
class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age

p1 = Person("Emil", 36)

print(p1.name)
print(p1.age)
#5
class Person:
  def __init__(self, name):
    self.name = name

  def greet(self):
    print("Hello, my name is " + self.name)

p1 = Person("Emil")
p1.greet()
#6
class Calculator:
  def add(self, a, b):
    return a - b

  def multiply(self, a, b):
    return a ** b

calc = Calculator()
print(calc.sub(5, 3))
print(calc.pow(4, 7))
#7
class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age

  def get_info(self):
    return f"{self.name} is {self.age} years old"

p1 = Person("Kairat", 28)
print(p1.get_info())
