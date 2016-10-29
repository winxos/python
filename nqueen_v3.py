__author__ = 'winxos'
import random
import time
size=8#the queens number
maxstep=100
seq=[0 for x in range(size)]#the queen sequence
seqc=[0 for x in range(size)]
am=[[0 for x in range(size)] for y in range(size)]#queen map
bm=[[0 for x in range(size)] for y in range(size)]#queen conflicts value

def init():
    for x in range(size):
        seq[x]=random.randint(0,size-1)
def isConflict(ix,iy,jx,jy): #judge the conflict of queen a, and b
    detx=ix-jx
    dety=iy-jy
    if detx*dety==0:
        return 1
    if detx==dety or detx+dety==0:
        return 1
    return 0
def singleVar(x,y):#fill a queen,calc the conflicts
    for i in range(size):
        bm[x][i]+=1
        bm[i][y]+=1
    bm[x][y]-=1
    det=1
    while x-det>0 and y-det>0:
        bm[x-det][y-det]+=1
        det+=1
    det=1
    while x+det<size and y+det<size:
        bm[x+det][y+det]+=1
        det+=1
    det=1
    while x-det>0 and y+det<size:
        bm[x-det][y+det]+=1
        det+=1
    det=1
    while x+det<size and y-det>0:
        bm[x+det][y-det]+=1
        det+=1
def conflicts():
    for i in range(size):
        for j in range(size):
            bm[i][j]=0
    for x in range(size):
        singleVar(x,seq[x])
    ret=[]
    for i in range(size):
        if bm[i][seq[i]]>1:ret.append(i)
    return ret
def replace(n):
    mi=min(bm[n])
    t=[]
    for i in range(size):
        if bm[n][i]==mi:t.append(i)
    seq[n]=t[random.randint(0,len(t)-1)]
def search():
    totalsteps=0
    for step in range(maxstep):
        c=conflicts()
        totalsteps+=1
        if len(c)==0:
            print("len:",totalsteps)
            return
        replace(c[random.randint(0,len(c)-1)])
def prt(n):#print the array
    for x in range(size):
        print(n[x])
    print("----end----")
def fillQ():#create the queen map am though seq
    for i in range(size):
        am[i][seq[i]]=1
#main loop
t1=time.time()*1000
init()
print(seq,"ok")
while len(conflicts())>0:
    search()
    print(len(conflicts()),seq)
print(seq)
t2=time.time()*1000
print(t2-t1)
