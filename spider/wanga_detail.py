#-------------------------------------------------------------------------------
# Name:        WangaDetail
# Purpose:     Wanga游戏抓取
#
# Author:      winxos
#
# Created:     1/12/2011
# Copyright:   (c) winxos 2011
# Licence:     free
#-------------------------------------------------------------------------------
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
import re
from sqlite3 import *
import os
from time import clock
import sys

DB_NAME='wanga_detail.db'
SUB_PAGE="http://wanga.me/%d"

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
#进度保存类
class ProgressSaver:
    def Save(self,msg):
        ofile=open('config.txt','w')
        ofile.write(msg)
        ofile.close()
    def Load(self):
        ret=''
        if os.path.exists('config.txt'):#要判断文件是否存在
            ifile=open('config.txt')
            ret=ifile.read()
        return ret

def GetGameInfo(gameid):
    uri=SUB_PAGE%gameid
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

    p2=re.compile('([^>]*)</p>\s*<[^>]*><embed src="([^"]*)"') #得到介绍和地址
    m2=p2.search(data)


    if m2==None:#页面有的使用内嵌框架的
        p2=re.compile('([^>]*)</p>\s*<p><iframe src="([^"]*)"')
        m2=p2.search(data)
    elif m2.group(1)=='':
        p2=re.compile('([^>]*)</p>\s*<p><[^>]*>[^<]*</a></p>\s*<[^>]*><embed src="([^"]*)"')
        m2=p2.search(data)
    if m2!=None:
        g.src=m2.group(2)
        g.detail=m2.group(1)

    p3=re.compile('category tag">([^<]*)<') #得到type
    m3=p3.search(data)
    if m3!=None:
        g.type=m3.group(1)

    p4=re.compile('rel="tag">([^<]*)<')#得到tag
    m4=p4.findall(data)
    g.tag=' '.join(m4)
    return g

def

#建立详细游戏资料库，包含id，名字，标签，源地址，说明等
def CreateDetailLib():
    ifile=open("d:/wanga_id.txt").read()
    mu=list(set(ifile.split()))#去除重复元素
    if os.path.isfile(DB_NAME):#已经建立数据库
        conn=connect(DB_NAME)
        curs=conn.cursor()
    else:
        conn=connect(DB_NAME)
        curs=conn.cursor()
        curs.execute('create table gamelist(id integer primary key, name text, \
                        type text, src text, tag text, detail text)')
    ps=ProgressSaver()#用于自动恢复计算
    progress=ps.Load()
    if progress=='':
        progress=0
    else:
        progress=int(progress)+1

    for x in range(progress,len(mu)):
        a=GetGameInfo(int(mu[x]))
        while a==None: #访问失败，持续访问。
            print "Connection Error! ReConnecting..."
            a=GetGameInfo(mu[x])
        try:
            st='insert into gamelist values(%d,"%s","%s","%s","%s","%s")'%\
                (a.id,a.name,a.type,a.src,a.tag,a.detail)
            st=' '.join(st.split())#去除空白符和换行符
            print x,mu[x]
            curs.execute(st)
            conn.commit()
            ps.Save(str(x))
        except Exception,e:
            print e
    conn.close()
if __name__ == '__main__':
    CreateDetailLib()

