#-------------------------------------------------------------------------------
# Name:        core algorithm for art char
# Author:      winxos
# Created:     29/03/2011
# Copyright:   (c) winxos 2011
# Licence:     GPL
#-------------------------------------------------------------------------------
#!/usr/bin/env python
import loadChars

def hex2bin(n):
	s={\
	"0":"0000","1":"0001","2":"0010","3":"0011",\
	"4":"0100","5":"0101","6":"0110","7":"0111",\
	"8":"1000","9":"1001","A":"1010","B":"1011",\
	"C":"1100","D":"1101","E":"1110","F":"1111"}
	return s[n]
def ansen(x):
	s=x.split(",")
	st=""
	for i in range(0,15,2):
		t=("%s%s%s%s"%(hex2bin(s[i][0]),hex2bin(s[i][1]),\
		hex2bin(s[i+1][0]),hex2bin(s[i+1][1])))
		st+=t
	ans=[[0 for x in range(8)] for y in range(16)]
	for i in range(8):
		for j in range(16):
			ans[j][i]=int(st[i*16+j])
	return ans
def anscn(x):
	s=x.split(",")
	st=""
	for i in range(0,31,2):
		st+=("%s%s%s%s"%(hex2bin(s[i][0]),hex2bin(s[i][1]),\
		hex2bin(s[i+1][0]),hex2bin(s[i+1][1])))
	ans=[[0 for x in range(16)] for y in range(16)]
	for i in range(16):
		for j in range(16):
			ans[j][i]=int(st[i*16+j])
	return ans
def reCreate(n,bc="     ",fc="/qq"):
	ans=[[0 for x in range(len(n[0]))] for y in range(len(n))]
	for i in range(len(n)):
		for j in range(len(n[i])):
			if n[i][j]==0:
				ans[i][j]=bc
			else:
				ans[i][j]=fc
	return ans
def convertStr(n,l=1,f="/wx"):
	ns=[]
	for i in n:
		ns.append(convertChar(i,f))
	ans=[[] for y in range(16)]
	for i in range(16):
		for j in ns:
			ans[i]+=j[i]
	a=""
	for i in range(16):
		a+=("".join(ans[i]))+"\n"
	return a
def convertChar(n,f="/wx"):
	d={}
	d=loadChars.getDict()
	if ord(n)<128:
		return reCreate(ansen(d[n]),bc="     ",fc=f)
	else:
		return reCreate(anscn(d[n]),bc="     ",fc=f)
if __name__ == '__main__':
	print(convertStr("Good"))
