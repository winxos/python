#coding:utf-8
#-------------------------------------------------------------------------------
# Name:½øÖÆ×ª»»µÝ¹éÊµÏÖ
# Author:      winxos
# Created:     10/03/2011
# Copyright:   (c) winxos 2011
# Licence:     GPL
#-------------------------------------------------------------------------------
#!/usr/bin/env python
def BaseAtoB(n,a=10,b=3):
	return n if n<b else BaseAtoB(n//b,a,b)*a+n%b
def main():
	print(BaseAtoB(10))
if __name__ == '__main__':
    main()
