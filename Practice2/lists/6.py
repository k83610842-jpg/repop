#1
drop1=['gold','apple','mon']
new=[]
for x in drop1:
    if 'a' in x:
        new.append(x)
print(new)
#2
drop1=['gold','apple','mon']
new=[x for x in drop1 if 'a' in x]
print(new)
#newlist = [expression for item in iterable if condition == True]
#3
drop1=['gold','apple','mon']
new1=[x for x in drop1 if 'a' not in x]
print(new1)
#4
drop1=['gold','apple','mon']
new3=[x for x in drop1]
print(new3)
#5
newik=[x for x in range(10)]
print(newik)
#6
newww=[0*x for x in range(20) if x%2==0]
print(newww)
#7
mmm=[x.upper() for x in drop1]
print(mmm)
#8
eee=[x if x!='gold' else 'apple' for x in drop1]
print(eee)