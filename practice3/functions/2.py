#1
def func(num):
  print(num + " gpa")

my_function("3.5")
my_function("2.3")
my_function("4.0")
#2
def unct(name): # name is a parameter
  print("Hello", name)

my_function("Kmaila") # "Emil" is an argument
#3
def func(surname, name):
  print(surname + " " + name)

my_function("Kairat", "Barsa")
#4
def func(name = "friend"):
  print("Hello", name)

my_function("Kairat")
my_function("Tom")
my_function()
#5
def func(a, b):
  print("I have a", a)
  print("My", a + "'s name is", b)

my_function(b = "Buddy", a = "dog")
