#1
goldapple = ["dior", "mmm", "cherry"]
for x in goldapple:
  print(x)
#2
for x in "goldapple":
  print(x)
#3
goldapple = ["dior", "mmm", "cherry"]
for x in goldapple:
  print(x)
  if x == "mmm":
    break
#4
goldapple = ["dior", "mmm", "cherry"]
for x in goldapple:
  if x == "mmm":
    break
  print(x)
#5
goldapple = ["dior", "mmm", "cherry"]
for x in goldapple:
  if x == "mmm":
    continue
  print(x)
#6
for x in range(9):
  print(x)
#7
for x in range(1,8):
  print(x)
#8
for x in range(6, 30, 3):
  print(x)
#9
for x in range(9):
  print(x)
else:
  print("Finally finished!")
#10
for x in range(11):
  if x == 3: break
  print(x)
else:
  print("Finally finished!")
#11
e = ["ff", "byy", "qq"]
t = ["dior", "gold", "apple"]

for x in e:
  for y in t:
    print(x, y)
#12
for x in [0, 1, 2]:
  pass