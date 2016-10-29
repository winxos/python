#!/usr/bin/env python
#coding:utf-8
#author:observer
#http://obmem.com
import urllib,urllib2,cookielib
import re,time,random
 
username = 'winxos'  #改成自己的用户名
passwd = 'saint1122' #改成自己的密码
#这个就是发帖内容，任意改，会随机选择一条发帖
msg = [ '多谢楼主',
        'Mark',
        '正在找这个，谢谢',
        '谢谢分享',
	'感谢大大的分享',
	'好资源，占位留名',
	'谢谢分享！！！！ ',
	'呵呵！支持个！ ',
	'谢谢发布',
	'非常感謝以無私精神供大家分享！'
    ]
 
def login():
    '''这个就是登录脚本'''
    print 'try to login...'
 
    #登录需要准备cookie
    cookie=cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie), urllib2.HTTPHandler)
    urllib2.install_opener(opener)
 
    #先获取verycd的fk串，用于填表
    print '...getting login form...'
    loginform = urllib2.urlopen('http://secure.verycd.com/signin/*/http://www.verycd.com/').read()
    fk = re.compile(r'id="fk" value="(.*)"').findall(loginform)[0]
 
    #好的，现在填表
    postdata=urllib.urlencode({'username':username,
                           'password':passwd,
                           'continueURI':'http://www.verycd.com/',
                           'fk':fk,
                           'login_submit':'登录',
    })
    req = urllib2.Request(
        url = 'http://secure.verycd.com/signin/*/http://www.verycd.com/',
        data = postdata
    )
 
    #填header，伪装成正常浏览访问，这是一种写法，也可以用我之前那篇文章的写法，更有条理一点
    req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6')
    req.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    req.add_header('Accept-Encoding','gzip,deflate')
 
    #交登录表，然后就登录成功了
    print '...login form submitted'
    result = urllib2.urlopen(req).read()
    print '...login succeed!'
 
def farm():
    '''这个就是灌水函数了'''
    #读取主页，获得主页的所有资源id
    res = urllib.urlopen('http://www.verycd.com').read()
    topics = re.compile(r'/topics/(\d+)').findall(res)
    topics = set(topics)
    print topics
 
    #对每一个获取的资源，回一贴支持楼主：）
    #语法和刚才交登录表差不多
    for topic in topics:
        url = 'http://www.verycd.com/topics/'+str(topic)+'/reply#fast-replay'
        print url
        postData = {
            'contents':random.choice(msg),
            'use_bbcode':'1',
            'tid':str(topic),
            'Action':'FolderCommentOperate:doReplyFolder'
        }
        postData = urllib.urlencode(postData)
        req = urllib2.Request(url = url, data = postData )
        kk = urllib2.urlopen(req).read()
        time.sleep(random.randint(1,5)) #随机等待一会再发贴
 
if __name__ == '__main__':
    login()
    farm()
