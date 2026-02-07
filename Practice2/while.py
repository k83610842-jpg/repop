#1
i = 1
while i <8:
  print(i)
  i += 1
#2
i = 1
while i <8:
  print(i)
  if i == 3:
    break
  i += 1
#3
i = 0
while i <9:
  i += 1
  if i == 3:
    continue
  print(i)
#4
i = 4
while i < 10:
  print(i)
  i += 1
else:
  print("i is no longer less than 10")