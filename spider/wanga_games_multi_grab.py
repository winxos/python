#-------------------------------------------------------------------------------
# Name:        wanga_Multi_grab
# Purpose:     wanga游戏id抓取
#
# Author:      winxos
# Created:     24/11/2011
# Modified:    19/10/2012
# Copyright:   (c) winxos 2011-2012
# Licence:     free
#-------------------------------------------------------------------------------
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2, threading,re,os
from Queue import Queue
from time import clock
from sqlite3 import *

DB_NAME="wanga_id.db"
TXT_NAME="wanga_id.txt"
ENTRY_PAGE="http://wanga.me/?s="
SUB_PAGE="http://wanga.me/page/%d"
RE_GAMES='data-thread\D*(\d+)"' #游戏页面改版，第一页内容不是游戏了。

#得到页面页数
def GetMaxPages(data):
    pos1=data.find("</a>",data.find("dots")) #简单匹配无需利用正则
    pos2=data.rfind(">",0,pos1)+1
    return int(data[pos2:pos1])
#得到单个游戏页面地址
def GetPageGames(uri):
    data=""
    try:
        page=urllib2.urlopen(uri,timeout=3)
        data=page.read()
        page.close()
    except Exception,e:#超时
        print "%s time out, retrying"%uri
        GetPageGames(uri)
    return re.findall(RE_GAMES,data) #正则匹配特殊标记
#文件线程类
class FileGetter(threading.Thread):
    def __init__(self, url):
        self.url = url
        self.result = None
        threading.Thread.__init__(self)#初始化，必须

    def get_result(self):
        return self.result

    def run(self):
        try:
            self.result = GetPageGames(self.url)
            while len(self.result)<1:
                self.result = GetPageGames(self.url)
        except Exception,e:
            print "!%s: %s" % (self.url,e)
#多线程文件下载，线程池
def get_files(files):
    startc=clock()
    finished=[] #用于存放结果
    def producer(q, files): #用于产生线程
        for url in files:
            thread = FileGetter(url)
            thread.start()
            q.put(thread, True)
    def consumer(q, total_files): #线程调用
        while len(finished)<total_files: #线程未完成
            thread = q.get(True)
            thread.join()
            finished.append(thread.get_result()) #完成任务结果加入列表
    q = Queue(5)#线程池大小
    prod = threading.Thread(target=producer, args=(q, files)) #线程使用
    cons = threading.Thread(target=consumer, args=(q, len(files)))
    prod.start()
    cons.start()
    prod.join()
    cons.join() #等待完成
    return finished
#得到游戏ID
def GetRawSeries():
    start=clock()#计时
    ans=get_files(GetPages(ENTRY_PAGE))
    print "total time collapsed:%f"%(clock()-start)
    output=open(TXT_NAME,'w')
    ret=[]
    for i in ans:
        output.writelines(' '.join(i)+' ')
        ret.extend(i)
    return ret
#建立子页面
def GetPages(url):
    print "getpages:",url
    ans=[]
    page=urllib2.urlopen(url)
    data=page.read()
    page.close()
    for i in range(2,GetMaxPages(data)+1):
        s_url=SUB_PAGE%i
        ans.append(s_url)
    print ans
    return ans
#建立游戏ID数据库
def CreateDatabase(mlist):
    mu=list(set(mlist))#去除重复元素
    if os.path.isfile(DB_NAME):#已经建立数据库
        os.remove(DB_NAME)
    conn=connect(DB_NAME)
    curs=conn.cursor()
    curs.execute('create table gamelist(id integer primary key)')
    for m in mu:
        curs.execute('insert into gamelist values('+str(m)+')')
    conn.commit()
    conn.close()
#main
CreateDatabase(GetRawSeries())