__author__ = 'WeoLee'
import random
size=49#the queens number
seq=[0 for x in range(size)]#the queen sequence
am=[[0 for x in range(size)] for y in range(size)]#queen map
bm=[[0 for x in range(size)] for y in range(size)]#queen conflicts value

def prt(n):#print the array
    for x in range(size):
        print(n[x])
    print("----end----")
def clear(b):#clear the 2d array
    for i in range(size):
        for j in range(size):
            b[i][j]=0
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
def qVar():#fill the all queens
    clear(bm)
    for x in range(size):
        singleVar(x,seq[x])
def replaceQ(n):#replace the n row queen to the min value
    mi=min(bm[n])
    tmp=[]
    for i in range(size):
        if bm[n][i]==mi:
            tmp.append(i)
    seq[n]=tmp[random.randint(0,len(tmp)-1)]
    return
def fillQ():#create the queen map am though seq
    clear(am)
    for i in range(size):
        am[i][seq[i]]=1
def getConflicts():#return the conflicts numbers of queens
    clear(bm)
    qVar()
    total=0
    for i in range(size):
        if bm[i][seq[i]]>1:
            total+=1
    return total
def init():#initial the vars
    for x in range(size):
        r=random.randint(0,size-1)
        seq[x]=r
    fillQ()

def do():#the main loop
    for s in range(200):#the max step is 200
        if getConflicts()==0:return#if found a solution, then return
        clear(bm)
        qVar()
        tmp=[]
        for i in range(size):
            if bm[i][seq[i]]>1:
                tmp.append(i)
        r=tmp[random.randint(0,len(tmp)-1)]
        replaceQ(r)
        fillQ()
init()
prt(am)
print(getConflicts())#开始的冲突数
do()
prt(am)
print(getConflicts())#如果为0则找到解了

