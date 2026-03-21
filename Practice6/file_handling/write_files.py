#3
with open('zzz.txt','a') as f:
    f.write('skoro leto\n')
    f.write('yra\n')
with open('zzz.txt','r') as f:
    print(f.read())
