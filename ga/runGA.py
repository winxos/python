#-------------------------------------------------------------------------------
# Name:        GA run
# Purpose:
#
# Author:      WeoLee
#
# Created:     04/03/2011
# Copyright:   (c) WeoLee 2011
# Licence:     <GNU>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
from pyGA import *
import math
def bin2dec(n):
    s=0
    for x in range(len(n)):s+=2**(len(n)-x-1)*n[x]
    return s
def f1(n):
    a=n/30000.0
    return -a*a+2*a
def f(n):
    a=bin2dec(n)
    return f1(a)
def main():
    a=WsPyGA(size=40,len=16)
    a.show()
    a.function=f
    print(a.getMaxGene(),a.getMaxValue())
    for x in range(200):a.getNextGene()
    print(a.getMaxGene(),a.getMaxValue())
    print("done")
if __name__ == '__main__':
    main()
