#-------------------------------------------------------------------------------
# Name:        it-ebooks grub
# Purpose:     ebooks grub multi thread py2.7
#
# Author:      winxos
# Created:     5/10/2014
# Copyright:   (c) winxos 2014
# Licence:     free
#-------------------------------------------------------------------------------
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re,threading,os,sys
import urllib2
from sqlite3 import *
from time import clock
from Queue import Queue
DB_NAME="it_ebooks.db"
class download(threading.Thread):
    def __init__(self, name,url):
        threading.Thread.__init__(self)#初始化，必须
        self.name = name
        self.url=url
    def run(self):
        try:
            headers = { #伪装为浏览器抓取
            'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
            }
            request = urllib2.Request(self.url,headers=headers)
            f = urllib2.urlopen(request)
            with open(self.name, "wb") as code:
               code.write(f.read())
        except Exception as e:
            print ("!%s: %s" % (self.name,e))
#多线程文件下载，线程池
def download_pools(files):
    finished=[] #用于存放结果
    def producer(q, files): #用于产生线程
        for name,url in files:
            thread = download(name,url)
            thread.start()
            q.put(thread, True)
    def consumer(q, total_files): #线程调用
        while len(finished)<total_files: #线程未完成
            thread = q.get(True)
            thread.join()
            finished.append(thread.id) #完成任务结果加入列表
    q = Queue(30)#线程池大小
    prod= threading.Thread(target=producer, args=(q, files)) #线程使用
    cons = threading.Thread(target=consumer, args=(q, len(files)))
    prod.start()
    cons.start()
    prod.join()
    cons.join() #等待完成
    return finished
#create sqlite datebase
def main():
    if os.path.isfile(DB_NAME):#已经建立数据库
        print('check update...')
        conn=connect(DB_NAME)
        curs=conn.cursor()
#        curs.execute('select name,src from booklist')
#      n=[(tmp[0],tmp[1]) for tmp in curs.fetchall()]
        curs.execute('select src from booklist')
        n=[tmp[0] for tmp in curs.fetchall()]
        #download_pools(n)
        print "\n".join(n)
    else:
        print ("database miss")
if __name__ == '__main__':
    print('download starting...')
    main()
    print("all done!")


