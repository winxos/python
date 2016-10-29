#coding:utf-8
'''
幂级数和函数python求解
原始算法采用：http://hi.baidu.com/lwgea/item/1be605ace1f619f615329b9b
利用递归进行实现
winxos2012-10-9
'''
import numpy as np
from fractions import Fraction as F
tb={0:np.poly1d([F(1),F(0)])}
def binomialCoeff(n, k): #计算二项式展开
    result = 1
    for i in range(1, k+1):
        result = result * (n-i+1) / i
    return result
def getDiff(n): #得到高次级差
    return map(lambda i:-binomialCoeff(n,i)*(-1)**i,range(1,n+1))
def powsum(n):
    if tb.has_key(n):return tb[n] #动态规划
    g=getDiff(n+1)
    an=np.poly1d([F(1)]+[0]*(n+1)) #初始构造
    for i in range(1,len(g)):
        an-=powsum(len(g)-1-i)*g[i]
    tb[n]=an/g[0]
    return tb[n]
if __name__ == "__main__":
    for i in range(10):
        g=powsum(i)
        print "sum x^%d="%i,g.coeffs
        print g
    print "sum x^30=",powsum(30).coeffs