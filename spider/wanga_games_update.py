#-------------------------------------------------------------------------------
# Name:        wanga_update
# Purpose:     wanga游戏update
#
# Author:      winxos
#
# Created:     31/12/2011
# Copyright:   (c) winxos 2011
# Licence:     free
#-------------------------------------------------------------------------------
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2, threading,re,os
from Queue import Queue
from time import clock
from sqlite3 import *

DB_NAME="wanga_id.db"
DB_DETAIL_NAME="wanga_detail.db"
ENTRY_PAGE="http://wanga.me/?s="
SUB_PAGE="http://wanga.me/page/%d"
GAME_PAGE="http://wanga.me/%d"
RE_GAMES='entry-title\D*(\d+)"'
#Vars
conn=connect(DB_NAME)
curs=conn.cursor()
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
        while len(data)<3:
            GetPageGames(uri)
        page.close()
    except Exception,e:#超时
        print "%s time out, retrying"%uri
        GetPageGames(uri)
    return re.findall(RE_GAMES,data) #正则匹配特殊标记

#得到游戏ID
def isHad(n):
    ans=curs.execute('SELECT * FROM gamelist WHERE id=%d'%n).fetchall()
    if ans==[]:
        return False
    return True
#建立子页面
def GetPages(url):
    ans=[]
    data=""
    try:
        page=urllib2.urlopen(url,timeout=3)
        data=page.read()
        page.close()
    except:
        GetPages(url)

    for i in range(1,GetMaxPages(data)+1):
        s_url=SUB_PAGE%i
        ans.append(s_url)
    return ans

#游戏数据结构
class gameinfo:
    def __init__(self):
        self.name=''#名称
        self.id=0#页面ID
        self.type=''#类型
        self.tag=''#标签
        self.detail=''#详情
        self.src=''
    def ToString(self):
        return str(self.id)+self.name+self.type+self.src+self.tag+self.detail


def GetGameInfo(gameid):
    uri=GAME_PAGE%gameid
    try:
        page=urllib2.urlopen(uri,timeout=3) #超时
        data=page.read()
        page.close()
    except Exception,e: #捕捉访问异常，一般为timeout，信息在e中
        return None

    g=gameinfo()
    g.id=int(gameid)
    data=unicode(data,'utf-8')#网页编码为utf-8

    p1=re.compile('entry-title">([^<]*)') #得到名称
    m1=p1.search(data)
    if m1!=None:
        g.name=m1.group(1)

    p2=re.compile('embed src="([^"]*)"') #得到地址
    m2=p2.search(data)
    if m2==None:#页面有的使用内嵌框架的
        p2=re.compile('iframe src="([^"]*)"')
        m2=p2.search(data)
    if m2!=None:
        g.src=m2.group(1) #地址
        #中文介绍
        p5=re.compile('([^\x00-\xff]+[^<]*)<[\x00-\xff]*<embed')#还是有点问题
        m5=p5.search(data)
        if m5==None:
            p5=re.compile('([^\x00-\xff]+[^<]*)<[\x00-\xff]*<iframe')#还是有点问题
            m5=p5.search(data)
            if m5.group(1).find(u'\u8fd9\u91cc\u5168\u5c4f')!=-1:#去除全屏模式
                p5=re.compile('([^\x00-\xff]+[^<]*)<[\x00-\xff]+[^\x00-\xff]+[\x00-\xff]+<iframe')
                m5=p5.search(data)
        elif m5.group(1).find(u'\u8fd9\u91cc\u5168\u5c4f')!=-1:#去除全屏模式
                p5=re.compile('([^\x00-\xff]+[^<]*)<[\x00-\xff]+[^\x00-\xff]+[\x00-\xff]+<embed')
                m5=p5.search(data)
        if m5!=None:
            g.detail=m5.group(1)
        else:
            print gameid,"no content"
    else:#没有插入游戏的情况
        print gameid,"no src"

    p3=re.compile('category tag">([^<]*)<') #得到type
    m3=p3.search(data)
    if m3!=None:
        g.type=m3.group(1)

    p4=re.compile('rel="tag">([^<]*)<')#得到tag
    m4=p4.findall(data)
    g.tag=' '.join(m4)

    return g
#文件线程类
class FileGetter(threading.Thread):
    def __init__(self, gameid):
        self.id = gameid
        self.result = None
        threading.Thread.__init__(self)#初始化，必须

    def get_result(self):
        return self.result

    def run(self):
        try:
            self.result = GetGameInfo(self.id)
            while self.result==None:
                self.result = GetGameInfo(self.id)
        except Exception,e:
            print "!%s: %s" % (self.id,e)
#多线程文件下载，线程池
def get_files(files):
    finished=[] #用于存放结果
    def producer(q, files): #用于产生线程
        for gameid in files:
            thread = FileGetter(int(gameid))
            thread.start()
            q.put(thread, True)
    def consumer(q, total_files): #线程调用
        while len(finished)<total_files: #线程未完成
            thread = q.get(True)
            thread.join()
            finished.append(thread.get_result()) #完成任务结果加入列表
            print len(finished)
    q = Queue(5)#线程池大小
    prod= threading.Thread(target=producer, args=(q, files)) #线程使用
    cons = threading.Thread(target=consumer, args=(q, len(files)))
    prod.start()
    cons.start()
    prod.join()
    cons.join() #等待完成
    return finished
#游戏id更新
def IdUpdate():
    ans=[]
    judge=0
    for l in GetPages(ENTRY_PAGE):
        gs=GetPageGames(l)
        for g in gs:
            if isHad(int(g)):
                judge+=1
            else:
                ans.append(g)
        if judge>30:#说明重复了
            break
    for a in ans:
        try:
            curs.execute('insert into gamelist values('+str(a)+')')
        except Exception,e:
            print e
    print len(ans)
    return ans
#建立详细游戏资料库，包含id，名字，标签，源地址，说明等
def DetailDBUpdate(mu):
    start=clock()#计时
    ans=get_files(mu)
    print "total time collapsed:%f"%(clock()-start)

    dconn=connect(DB_DETAIL_NAME)
    dcurs=dconn.cursor()
    for a in ans:
        try:
            print a.id
            st='insert into gamelist values(%d,"%s","%s","%s","%s","%s")'%\
                (a.id,a.name,a.type,a.src,a.tag,a.detail)
            st=' '.join(st.split())#去除空白符和换行符
            dcurs.execute(st)
        except Exception,e:
            print e
    print ','.join(mu)," updated!"
    dconn.commit()
    dconn.close()
    conn.commit()
    conn.close()
#main
DetailDBUpdate(IdUpdate())