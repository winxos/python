'''
#python zipfile ¶ÁÐ´Ê¾·¶
#winxos 2011-3-13
'''
import zipfile
m="hello python, xxooxxoo!"
#write zip file
cm=zipfile.ZipFile(r'D:/h.zip','w')
cm.writestr('xx.txt',m)
cm.close()

#read the zip file
cm=zipfile.ZipFile(r'D:/h.zip')
cm.extract('xx.txt',r'D:/')
cm.close()
import os
os.system(r"notepad d:/xx.txt")
