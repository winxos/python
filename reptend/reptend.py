# -*- coding: cp936 -*-
#素数循环节算法
#winxos 2012-06-25

import math
import rho #引入快速整数分解

#组合数字递归序列生成
#输入n为整数列表,例如输入[1,2]
#则输出['00', '01', '02', '10', '11', '12']
def combination(n):
    if len(n)==1:
        return range(0,n[0]+1)
    ret=[] #存放组合结果
    for i in range(0,n[0]+1):
        for li in combination(n[1:]):
            ret.append(str(i)+str(li))
    return ret

#由整数质因子及其数目求该整数的全部因子
#例如 36=2^2 x 3^2
#本质上是根据指数[2 2]的全部可能序列与底数运算得到
def allfactors(c,n):
    if len(n)==1:
        ret=[]
        for i in range(0,n[0]+1):
            ret.append(c[0]**i)
        return ret
    ret=[] #每次迭代，将会扩充列表
    for i in range(0,n[0]+1): #求c^a次方，a为0-n范围内的整数
        for li in allfactors(c[1:],n[1:]):
            ret.append(c[0]**i*li) #扩充列表大小
    ret.sort()
    return ret

# from http://www.haogongju.net/art/750012
# by wander@xjtu copyleft
def montgomery(n,p,m):
    if (p==0):
        return 1
    k=montgomery(n,p>>1,m)
    if (p & 0x01 == 0):
        return k*k % m
    else:
         return n*k*k % m

#小素数准备
#http://caterpillar.onlyfun.net/Gossip/AlgorithmGossip/GCDPNumber.htm
primes=[] #小素数表
startnum=10001
def prepare_factor():
    max=startnum-1
    prime = [1] * max
    for i in range(2, int(math.sqrt(max))):
        if prime[i] == 1:
            for j in range(2 * i, max):
                if j % i == 0:
                    prime[j] = 0
    global primes
    primes = [i for i in range(2, max) if prime[i] == 1]
    
#因子分解,先过滤小素数因子
def factor(num):
    if len(primes)==0:
        prepare_factor()
        print "initial small primes:",len(primes)
    list = []
    i = 0
    while i<len(primes):
        if num<primes[i]:break
        if num % primes[i] == 0:
            list.append(primes[i])
            num //= primes[i]
        else:
            i += 1
    if num<startnum: #没有大因子，返回
        return list
    upnum=math.sqrt(num)+1
    i=startnum #最小的因子都要比
    while i<=upnum:
        if num<i:break
        if num%i==0:
            list.append(i)
            num//=i
        else:
            i+=2
    if num!=1:
        list.append(num)
    return list
def isprime(num):
    if len(factor(num))==1:return True
    return False
#将质因子表转换成底数，指数表
def normfactor(li):
    dict={}
    for i in li:
        if dict.has_key(i):
            dict[i]+=1
        else:
            dict[i]=1
    l_c=[]
    l_e=[]
    for key in dict:
        l_c.append(key)
        l_e.append(dict[key])
    return (l_c,l_e)
#素循环节长
def reptend(n):
    #if isprime(n)==False:return -1
    maxr=n-1
    lc,le=normfactor(rho.factor(maxr)) #采用rho文件中的因子分解
    lif= allfactors(lc,le)#返回该整数全部因子
    for i in lif:
        if montgomery(10,i,n)==1:
            return i
#长素数寻找（全长度循环节素数)
def test():
    startbit=40
    searchw=3
    i=10**startbit+1 #查找范围开始
    while i<10**startbit+10**searchw:
        if rho.rabin_miller(i): #素性测试
            print i,":",reptend(i)
        i+=2
    print ""
#main 
if __name__ == '__main__':
    from timeit import Timer
    t=Timer("test()","from __main__ import test")
    print t.timeit(1) #计时
    
    
