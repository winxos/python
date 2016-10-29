#-------------------------------------------------------------------------------
# Name:        Hamilton
# Purpose:
#
# Author:      winxos
#
# Created:     30/01/2012
# Copyright:   (c) wzx 2012
# Licence:     free
#-------------------------------------------------------------------------------
#!/usr/bin/env python
import random
hd=[[1,2],[0,3,4],[0,5,6],[1,7],[1,5,8], \
    [2,4,10],[2,11],[3,8,12],[4,7,9],[8,10,13], \
    [5,9,11],[6,10,14],[7,13],[9,12,14],[11,13]]
visited=[0] * len(hd)
routh=[]
def isVisited(city):
    return visited[city]==1
def isAllVisited(city):
    citys=hd[city]
    Flag=True
    for c in citys:
        if visited[c]==0:
            Flag=False
            break
    return Flag

def visit(startcity):
    if len(routh)==len(visited):
        return
    if isVisited(startcity):
        return
    if isAllVisited(startcity):
        visited[startcity]=0
        routh.pop()
    visited[startcity]=1
    routh.append(startcity)


    city=hd[startcity][random.randint(0,len(hd[startcity])-1)]
    #for city in hd[startcity]:

    if not isVisited(city):
        visit(city)
    else:
        visit(startcity)
def main():
    visit(0)
    print routh

if __name__ == '__main__':
    main()
