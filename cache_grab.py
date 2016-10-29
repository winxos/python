#!/usr/bin/env python
# -*- coding: utf-8 -*-
# grab cache file to user path
# used for game factory, grab cached files
# winxos 2014-02-22
import os,sys
import fnmatch
import getpass  #get user name
import shutil   #copy
from time import sleep
rootdir = os.path.join('C:/Users',getpass.getuser(),'AppData\Local\Microsoft\Windows\INetCache\IE')
def copy_file(file,newpath):
    base_dir=os.path.join(sys.path[0],newpath)#get absolute path
    if not os.path.exists(base_dir): #不存在就建立
        os.mkdir(base_dir)
    simplename,suffix=os.path.splitext(os.path.basename(file))
    shutil.copy(file,os.path.join(base_dir,simplename[0:-3]+suffix)) #remove cache auto added [1]
def get_cachefile(name,newpath):
    for i in range(6): #max try times
        flag=False
        for parent,dirnames,filenames in os.walk(rootdir):
            for file in filenames:
                if fnmatch.fnmatch(file,name): #common match
                    copy_file(os.path.join(parent,file),newpath)
                    flag=True
        if flag:
            print("grab files successed.")
            return
        sleep(30) #延时
    print("grab files failed.")

from threading import Thread
#grab files
def grab_file(name,newpath):
    simplename,suffix=os.path.splitext(name)
    get_file=Thread(target=get_cachefile,args=(simplename+'*'+suffix,newpath))#parameter transin
    get_file.start() #异步抓取
if __name__ =='__main__':
    grab_file("*.jpg","tmp_jpgs")