#4
import shutil
shutil.copy('zzz.txt','bbb.txt')
#5
import os
if os.path.exists('zzz.txt'):
    os.remove('zzz.txt')
else:
    print('file does not exist')
