#-------------------------------------------------------------------------------
# Name:        dir batch creater using python and blumind
# Author:      winxos
# Created:     14/03/2011
# Copyright:   (c) winxos 2011
# Licence:     GPL
#.Description:.
#this script create directories using blumind files.
#-------------------------------------------------------------------------------
#!/usr/bin/env python
from xml.dom import minidom
import os
def visit(xml,r):
	if xml.localName=="node":
		r.append("creat",xml.attributes["text"].value)
		os.mkdir(xml.attributes["text"].value)
	for x in xml.childNodes:
		if x.localName=="none":return
		if x.localName=="nodes":
			#print("into:",x.parentNode.attributes["text"].value)
			os.chdir(x.parentNode.attributes["text"].value)
			visit(x)
			print("out",x.parentNode.attributes["text"].value)
			os.chdir(os.pardir)
		if x.localName=="node":
			visit(x)
	return

xml="D:/blumind/box2d.bmd"   #change to your blumind files
os.chdir("e:/")     #change to where you want to create.
visit(minidom.parse(xml).getElementsByTagName("node")[0])