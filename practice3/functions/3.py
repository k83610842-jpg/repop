#1
def func(*animals):
  print("The fav animal is " + animals[1])

my_function("dig", "cat")
#2
def func(*args):
  print("Type:", type(args))
  print("First argument:", args[0])
  print("Second argument:", args[1])
  print("All arguments:", args)

my_function("animal", "cat")
#3
def func(greaat, *names):
  for x in names:
    print(greet, x)

my_function("Hello", "dog", "cat")
#4
def funct(*numbers):
  total = 0
  for x in numbers:
    total += x
  return total

print(my_function(1, 2, 3))
print(my_function(8987, 77, 54, 32))
print(my_function(79))
#5
def func(*numbers):
  if len(numbers) == 0:
    return None
  max = numbers[0]
  for x in numbers:
    if x > max:
      max = x
  return max

print(my_function(3, 7, 2, 9, 1))
#6
def func(**kid):
  print("His last name is " + kid["lname"])

my_function(fname = "Barsa", lname = "Kairat")


