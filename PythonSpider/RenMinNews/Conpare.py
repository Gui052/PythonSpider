import os
import sys



old=open(os.path.join(sys.path[0]+'/URLold','健康.txt'),'r')
oldurls=old.readlines()
new=open(os.path.join(sys.path[0]+'/URL','健康.txt'),'r')
newurls=new.readlines()


for l in newurls:
    for k in oldurls:
        if l==k:
            newurls.remove(l)
            break;

new.close()
old.close()

f=old=open(os.path.join(sys.path[0],'健康.txt'),'w')
text=""
for i in newurls:
    text=text+i
f.write(text)
f.close()

