#-------------------------------------------------------------------------------
# Name:        it-ebooks grub
# Version:     1.1
# Purpose:     ebooks grub multi thread py2.7
#
# Author:      winxos
# Created:     5/10/2014
# Updated:     7/12/2014
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

DB_NAME='s:/it_ebooks.db'
ENTRY_PAGE="http://it-ebooks.info"
SUB_PAGE="http://it-ebooks.info/book/%s"

#得到最大页数
def GetMaxPages(data):
    pos1=data.find("book/",data.find("Last Upload eBooks"))+5 #简单匹配无需利用正则
    pos2=data.find("/",pos1)
    return int(data[pos1:pos2])

#得到ID
def GetRawSeries():
    page=urllib2.urlopen(ENTRY_PAGE)
    data=unicode(page.read(),encoding='utf8')
    page.close()
    return range(1,GetMaxPages(data)+1)

#数据结构,通过动态方式设置属性
class bookinfo:
    def __str__(self): #overload print 
        return '\n'.join(k+":"+getattr(self,k) for k in self.__dict__) #dynamic get attribute
#得到详细项内容
def GetSubInfo(id):
    uri=SUB_PAGE%id
    try:
        page=urllib2.urlopen(uri,timeout=3) #超时
        data=page.read()
        page.close()
    except Exception as e: #捕捉访问异常，一般为timeout，信息在e中
        return None
    try:
        data=unicode(data,encoding='utf-8')#网页编码为utf-8
    except UnicodeError:
        print ("%s decode error"%id)
    b=bookinfo()
    b.id=id
    RULES={"name":'itemprop="name">([\s\S]*)</h1>',\
          "description":'itemprop="description">([\s\S]*)</span>',\
          "publisher":'itemprop="publisher">([^<]*)</a>',\
          "author":'itemprop="author"[^>]*>([^<]*)</b>',\
          "isbn":'itemprop="isbn">([^<]*)</b>',\
          "dataPublished":'itemprop="datePublished">([^<]*)</b>',\
          "pages":'itemprop="numberOfPages">([^<]*)</b>',\
          "format":'itemprop="bookFormat">([^<]*)</b>',\
          "src":"Download:</td><td><a href='([^']*)'"} #特殊单引号
    for key in RULES:
        p=re.compile(RULES[key])#得到名称
        m=p.search(data)
        if m!=None:
            t=m.group(1).replace("\"","\"\"")
            t=t.replace("'","''")
            setattr(b,key,t) # dynamic set attribute
        else:
            #print ("%d error at %s"%(id,key))
            return None
    return b
#文件线程类
class get_detail_t(threading.Thread):
    def __init__(self, id):
        self.id = id
        self.result = None
        self.retry=3 #retry times
        threading.Thread.__init__(self)#初始化，必须
    def get_result(self):
        return self.result
    def run(self):
        try:
            self.result = GetSubInfo(self.id)
            while self.result==None and self.retry>0:
                self.retry-=1
                self.result = GetSubInfo(self.id)
        except Exception as e:
            print ("!%s: %s" % (self.id,e))
#多线程文件下载，线程池
def get_detail_t_pools(files):
    finished=[] #用于存放结果
    fail=[]
    def producer(q, files): #用于产生线程
        for id in files:
            thread = get_detail_t(id)
            thread.start()
            q.put(thread, True)
    def consumer(q, total_files): #线程调用
        while len(finished)+len(fail)<total_files: #线程未完成
            thread = q.get(True)
            thread.join()
            if thread.get_result()!=None:
                finished.append(thread.get_result()) #完成任务结果加入列表
                if len(finished)%50==0:
                    print ("already grab %d"%len(finished))
            else:
                print("%s not exist anymore"%thread.id)
                fail.append(thread.id)

    q = Queue(30)#线程池大小
    prod= threading.Thread(target=producer, args=(q, files)) #线程使用
    cons = threading.Thread(target=consumer, args=(q, len(files)))
    prod.start()
    cons.start()
    prod.join()
    cons.join() #等待完成
    return (finished,fail)
#create sqlite datebase 
def CreateDetailLib(mu):
    print ("total load %d items"%len(mu))
    if os.path.isfile(DB_NAME):#已经建立数据库
        print('check update...')
        conn=connect(DB_NAME)
        curs=conn.cursor()
        curs.execute('create table if not exists failed(id integer primary key)') #record failed
        curs.execute('select id from booklist')
        n=[tmp[0] for tmp in curs.fetchall()]
        print('already %d'%len(n))
        mu=list(set(mu).difference(n)) #集合操作去除重复元素
        curs.execute('select id from failed') #skip failed already know
        n=[tmp[0] for tmp in curs.fetchall()]
        print('not exists %d'%len(n))
        mu=list(set(mu).difference(n)) #集合操作去除重复元素
        print('found %d new added'%len(mu))       
    else:
        print ("create new database:%s"%DB_NAME)
        conn=connect(DB_NAME)
        curs=conn.cursor()
        curs.execute('create table booklist(id integer primary key, name text,publisher text, \
                        author text, isbn text, dataPublished text, pages text, format text, \
                         src text, description text)')
        curs.execute('create table failed(id integer primary key)') #failed record
    if len(mu)>0:
        print("start detail grab...")
        start=clock()#计时
        ans,fail=get_detail_t_pools(mu) #
        print ("total time collapsed:%2f"%(clock()-start))
        print ("success fetched %d books, %d not exist any more."%(len(ans),len(fail)))
        for a in ans:
            try:
                st='insert into booklist values(%d,"%s","%s","%s","%s","%s","%s","%s","%s","%s")'%\
                    (int(a.id),a.name,a.publisher,a.author,a.isbn,a.dataPublished,a.pages,\
                     a.format,a.src ,a.description)
                st=' '.join(st.split())#去除空白符和换行符
                #print (st)
                print ("insert:"+str(a.id)+","+a.name)
                curs.execute(st)
            except Exception as e:
                print (e)
        for a in fail:#modify 2014-07-11
            try:
                st='insert into failed values(%d)'%int(a)
                st=' '.join(st.split())#去除空白符和换行符
                curs.execute(st)
            except Exception as e:
                print (e)
        conn.commit()
    conn.close()
    print ("datebase %s saved"%DB_NAME)
if __name__ == '__main__':
    print('grab process starting...')
    CreateDetailLib(GetRawSeries())
    print("all done!")


