#1
x = lambda a : a + 10
print(x(90))
#2
x=lambda a,b:a*b
print(x(3,7))
#3
x = lambda a, b, c : a + b + c
print(x(8, 65, 43))
#4
def myfunc(n):
  return lambda a : a * n

mydoubler = myfunc(2)

print(mydoubler(11))
#5
numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 3, numbers))
print(tripled)
#6
numbers = [1, 2, 3, 4, 5, 6, 7, 8]
odd_numbers = list(filter(lambda x: x % 2 != 0, numbers))
print(odd_numbers)
#7
students = [("Emil", 25), ("Tobias", 22), ("Linus", 28)]
sorted_students = sorted(students, key=lambda x: x[1])
print(sorted_students)
