#-------------------------------------------------------------------------------
# Name:        read
# Purpose:
#
# Author:      weolee
#
# Created:     16/05/2012
# Copyright:   (c) weolee 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
data=''
def init():
	f=open("3754.txt")
	global data
	data=f.read()
	f.close()

def judge(s):
	pos=data.find(s.encode('gbk'))
	if pos==-1:
		print 'Error input:'
		return
	if pos%4==0:
		print 'input tradition Chinese return simple Chinese'
		return data[pos+2]+data[pos+3]
	print 'input simple Chinese return tradition Chinese'
	return data[pos-2]+data[pos-1]
def main():
	init()
	print 'loaded:%s'%len(data)
	a=raw_input()
	print judge(a)
if __name__ == '__main__':
	main()