#-------------------------------------------------------------------------------
# Name:        import lcd model files.
# Author:      winxos
# Created:     28/03/2011
# Copyright:   (c) winxos 2011
# Licence:     GPL
#-------------------------------------------------------------------------------
#!/usr/bin/env python
import codecs
s=r"d:\lcd_cn.txt"
f=codecs.open(s,"r","utf-8")
st=[]
st=f.readlines()
f.close()
print(len(st))
w=codecs.open("d:\lcd_cn.dat","w","utf-8")
for i in range(len(st)):
	if len(st[i])==69:
		tmp=st[i].split(";")[0].split()[1]+","+st[i+1].split(";")[0].split()[1]
		w.write("%s %s\n"%(st[i+1].split(";")[-1][1:2],tmp))
		i+=1
w.close()



