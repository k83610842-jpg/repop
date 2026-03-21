#1
with open("zzz.txt","w") as f:
    f.write('kapets teplo na ulitse\n')
    f.write('vchera bylo kholodno\n')
#2
with open('zzz.txt','r') as f:
    print(f.read())
