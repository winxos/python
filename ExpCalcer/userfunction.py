#-------------------------------------------------------------------------------
# Name:        calcer user functions
# Author:      winxos
# Created:     20/03/2011
# Copyright:   (c) winxos 2011
# Licence:     GPL
#-------------------------------------------------------------------------------
#!/usr/bin/env python
import math
def jie(n):
	s=1
	for x in range(1,n+1):
		s*=x
	return s
def isprime(n):
	if n==2 or n==3:return 1
	if n<2 or n%2==0:return 0
	for i in range(3,int(math.sqrt(n))+1,2):
		if n%i==0:return 0
	return 1
def prime(n):
	s=""
	for i in range(n+1):
		if isprime(i):
			s+=str(i)+' '
	return s
def dob(n):
	return n*2
if __name__ == '__main__':
	print("user functions of calcer.")
