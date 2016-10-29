#-------------------------------------------------------------------------------
# Name:        import lcd model files.
# Author:      winxos
# Created:     28/03/2011
# Copyright:   (c) winxos 2011
# Licence:     GPL
#-------------------------------------------------------------------------------
#!/usr/bin/env python
import codecs
s=r"d:\lcd_en.txt"
f=codecs.open(s,"r","utf-8")
st=[]
st=f.readlines()
f.close()
print(len(st))
w=codecs.open("d:\lcd_en.dat","w","utf-8")
for i in range(len(st)):
	if len(st[i])>50:
		#ans[st[i].split(";")[-1][1:2]]=st[i].split(";")[0].split()[-1]
		w.write("%s %s\n"%(st[i].split(";")[-1][1:2],st[i].split(";")[0].split()[-1]))
w.close()



