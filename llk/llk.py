'''
Description:link link game auto solver algorithm.
Author:winxos 
Date:2011-05-18
'''
import random
size=10
m=[[0 for x in range(size)] for y in range(size)]
def createmap():
	def createpos():
		return [random.randint(0, size-1), random.randint(0, size-1)]
	def fillpair(n):
		a=createpos()
		while m[a[0]][a[1]]!=0:
			a=createpos()
		b=createpos()
		while m[b[0]][b[1]]!=0 or b==a:
			b=createpos()
		m[a[0]][a[1]]=n
		m[b[0]][b[1]]=n
	for i in range(20):
		fillpair(random.randint(1, 9))
	pass
def isdirectlink(a, b):
	#a,b is point
	#return 1 means can link directly
	if a[0]==b[0] and a[1]==b[1]: #same point return false
		return 0
	if a[0]==b[0]: #Vertical
		if a[0]==0 or a[0]==size-1: #bound is linkable
			return 1
		sa=a[1]
		sb=b[1]
		if sb < sa: #field from sa to sb, sa<sb
			sa=b[1]
			sb=a[1]
		for i in range(sa+1, sb-1):
			if m[a[0]][i]!=0:
				return 0
		return 1
	if a[1]==b[1]: #Horizon
		if a[1]==0 or a[1]==size-1: #bound is linkable
			return 1
		sa=a[0]
		sb=b[0]
		if sb < sa: #field from sa to sb, sa<sb
			sa=b[0]
			sb=a[0]
		for i in range(sa+1, sb-1):
			if m[i][a[1]]!=0:
				return 0
		return 1	
	pass
	return 0
def onelinepoint(a): #return the cross directly linkable points.
	r=[]
	i=a[0]-1
	while m[i][a[1]]==0 and i>0:
		r.append([i, a[1]])
		i-=1
	i=a[0]+1
	while m[i][a[1]]==0 and i<size:
		r.append([i, a[1]])
		i+=1	
	j=a[1]-1
	while m[a[0]][j]==0 and j>0:
		r.append([a[0], j])
		j-=1	
	j=a[1]+1
	while m[a[0]][j]==0 and j<size:
		r.append([a[0], j])
		j+=1	
	return r
def islinkable(a, b): #core function
	if isdirectlink(a, b):
		return 1
	sa=onelinepoint(a)
	sb=onelinepoint(b)
	for x in sa:
		if isdirectlink(x, b):
			return 2
	for x in sb:
		if isdirectlink(a, x):
			return 2
	for x in sa:
		for y in sb:
			if isdirectlink(x, y):
				return 3
	return 0
def prt(n):
	print("---begin---")
	for x in n:
		print(x)
createmap()
a=[5, 5]
b=onelinepoint(a)
prt(m)
print(b)
print("done!")
