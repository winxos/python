#a fast sqrt program use ruby
#by winxos 2009-04-02
#移植到 python
#by winxos 2011-3-13
import math
st=987654321
n=str(st*st)
lens=len(n)
maxs=math.floor((math.log(lens)/math.log(2))-0.05) #get loop times
max2=2**(maxs+1)-lens
coef=2-lens%2 #odd ,even use two methods
print("calc (987654321^666)^2\n")
print("len:",len," max:",max,"\n")
print("source:     ",st,"\nsource^2: ",n,"\n")
a=int(math.sqrt(int(n[0,coef])))
remain=int(n[0,coef])-a*a
coef%=2
for i in range(1,maxs+1):
  steps=10**(2**(i-1))
  remain=remain*steps*steps+int(n[2**i-coef,2**i])
  b=remain/(2*steps*a)  #first b
  while (remain-2*steps*a*b)<b*b:b=b-1 #check b
  remain=remain-2*steps*a*b-b*b #get remain to continue calc
  a=a*steps+b
result=str(a)
result=int(result[0,result.length-max2/2])  #restore result,trim end's zero
print("ans :        ",result,"\nans^2:     ",result*result,"\n")
