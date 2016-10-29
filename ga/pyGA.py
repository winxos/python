#-------------------------------------------------------------------------------
# Name:        GeneAlgorithm module
# Purpose:     A framework for GA, for test.
#
# Author:      WeoLee
#
# Created:     03/03/2011
# Copyright:   (c) WeoLee 2011
# Licence:     <GNU>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
import random
class WsPyGA:
    __group=[]
    function=""
    def __init__(self,size,len):
        self.__group=[]
        for x in range(size):
            r=[]
            for x in range(len):
                r.append(random.randint(0,1))
            self.__group.append(r)
        print("Group init ok! size",size,"len",len)
    def __fun(self,n):
        return self.function(n)
    def __exchangeGene(self,g1,g2):
        loc=random.randint(0,len(g1)-2)+1
        a=g1[0:loc]+g2[loc:]
        b=g2[0:loc]+g1[loc:]
        return a,b
    def __mutateGene(self,g):
        i=random.randint(0,len(g)-1)
        g[i]=1-g[i]
    def getMaxGene(self):
        m=self.__group[0]
        for x in self.__group:
            if self.__fun(x)>self.__fun(m):
                m=x
        return m
    def getMaxValue(self):
        return self.__fun(self.getMaxGene())
    def __rollGene(self):
        adapt=[]
        ct=[0 for x in range(len(self.__group))]
        sum=0
        for x in self.__group:
            sum+=self.__fun(x)
            adapt.append(sum)
        for x in range(len(self.__group)):
            r=random.random()*sum
            j=0
            while j<len(adapt) and adapt[j]<r:j+=1
            if j!=len(adapt):ct[j]+=1
        gm=self.getMaxGene()
        for x in range(len(ct)):
            if ct[x]==0 and random.randint(0,3)==0:
                self.__group[x]=gm
                break
    def getNextGene(self):
        self.__rollGene()
        for x in range(0,len(self.__group),2):
            if random.randint(0,5)==0:
                self.__group[x+1],self.__group[x]=\
                self.__exchangeGene(self.__group[x],self.__group[x+1])
        if random.randint(0,200)==23:
            self.__mutateGene(self.__group[random.randint(0,len(self.__group))])
    def show(self):
        for x in self.__group:print(x)
    if __name__ == '__main__':
        print("Hello GA module!")