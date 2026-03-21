#1
l=list(map(int,input().split()))
ev=list(map(lambda x:x*2,l))
print(ev)

l=list(map(int,input().split()))
ev1=list(filter(lambda x:x%2==0,l))
print(ev1)
#2
from functools import reduce
res=reduce(lambda acc, x: acc + x, l)
print(res)
#3
names=["Miras", "Bob"]
ages=[38, 73]
for a, b in zip(names, ages):
    print(a, b)
#4
x=10
print(type(x))
isinstance(x, int)
