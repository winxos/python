size=11
am=[[0 for x in range(size)] for y in range(size)]
bm=am
N=5
route=[]
def visit(x,y):
    #limit
    if(x<0 or x>=size or y<0 or y>=size):return
    #same value
    if(am[x][y]!=N):return
    #visited
    if(bm[x][y]==1):return
    route.append([x,y])
    bm[x][y]=1
    visit(x-1,y)
    visit(x+1,y)
    visit(x,y-1)
    visit(x,y+1)
        
for x in range(0,11):
    for y in range(4,6):
        am[x][y]=N
for x in range(2,5):
    for y in range(1,11):
        am[x][y]=N
visit(5,5)
for x in range(size):
    print(am[x])
print(route)
print(len(route))
