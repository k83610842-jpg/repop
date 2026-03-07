#1
import re
s=input()
x=re.search(r"^ab*$",s)
print(x)
#2
import re
s=input()
x=re.search(r"^ab{2,3}$",s)
print(x)
#3
import re
s=input()
x=re.search(r"[a-z]+_[a-z]+",s)
print(x)
#4
import re
s=input()
x=re.search(r"[a-z][A-Z]+",s)
print(x)
#5
import re
s=input()
x=re.search(r"^a.*b$",s)
print(x)
#6
import re
s=input()
x=re.sub(r"[,.]",":",s)
print(x)
#7
import re
s=input()
x=re.sub(r"_[a-z]","")
#8
import re
s=input()
x=re.split(r"[A-Z]",s)
print(x)
#9
import re
s=input()
x=re.sub(r"[A-Z]"," \1",s)
print(x[1:])
#10
import re
s=input()
x=re.sub(r"[A-Z]","_\1",s)
print(x.lower())
