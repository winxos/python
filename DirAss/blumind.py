#-------------------------------------------------------------------------------
# Name:        BLUMind Maker
# Author:      winxos
# Created:     15/03/2011
# Copyright:   (c) winxos 2011
# License:     GPL
#-------------------------------------------------------------------------------
#!/usr/bin/env python
#coding:utf-8
import os
import codecs
from xml.dom.minidom import parse
'''
递归遍历文件夹,
path为绝对路径
list t用于存储目录描述表达式
'''
def getdir(path,dirstr):#
	x=os.listdir(path)
	if x==[]:return
	dirstr.append("(")
	for i in x:
		if os.path.isdir(path+"\\"+i):
			dirstr.append(i)
			getdir(path+"\\"+i,dirstr)
	dirstr.append(")")
	return dirstr
'''
将getdir生成的目录描述表达式转换为blumind 的 xml文件
s为目录描述表达式
'''
def toxml(s):
	r=""
	for i in range(len(s)-1):
		if s[i+1]=="(":#如果有子目录采用<node></node>结构
			r+='<node text="%s">'%s[i]
		else:
			if s[i]=="(":r+="<nodes>"
			elif s[i]==")":r+="</nodes></node>"
			else:r+='<node text="%s"/>'%s[i] #否则采用<node />
	r+="</nodes>"
	return r
'''
path为输入路径名，
返回blumind的xml格式文件，
保存为bmd格式就可以了
'''
def createBluMind(path):
	r=parse("template.bmd") #load xml 模板
	s=[]
	return r.toxml()%('<node text="%s">%s</node>'%(path,toxml(getdir(path,s))))
if __name__=="__main__":
	sd="o:\\computer"
	s=createBluMind(sd)
	f=codecs.open(sd.split('\\')[-1]+".bmd","w","utf-8") #写utf8格式,文件命名为目录最后一个文件夹
	f.write(s)
	f.close()
	print("Done!")
