#-------------------------------------------------------------------------------
# Name:        lcd model loading
# Author:      winxos
# Created:     29/03/2011
# Copyright:   (c) winxos 2011
# Licence:     GPL
#-------------------------------------------------------------------------------
#!/usr/bin/env python
import codecs #deal the Chinese chars
enstr="lcd_en.dat"
cnstr="lcd_cn.dat"
def getDict():
	f=open(enstr,"r") #open english lcd data
	s=f.readlines()
	f.close()
	f=codecs.open(cnstr,"r","utf-8") #open Chinese lcd data
	s+=f.readlines()
	f.close()
	dic={}
	for x in s:
		dic[x.split()[0]]=x.split()[1]
	return dic
if __name__ == '__main__':
	print("loading data")
