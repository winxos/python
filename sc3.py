#! /usr/bin/python
# coding=utf-8
'''
中文编码
功能：局域网内的IP和主机名。
多线程编程。实践表明，多线程比单线程要快好多好多~~
'''

import sys, os, socket, string
import threading

list_of_name=[]
list_of_ip=[]   #存放结果
thread_pool=[]

def showInfo():
    print """
     命令格式：LAN_ip_hostname -all startip
              LAN_ip_hostname -ip ipaddr
              LAN_ip_hostname -hostname hostname
     说明：-all 扫描局域网中所有IP对应的hostname,需要起始IP，如192.168.0.1
          -ip 获取指定IP的hostname
          -hostname 根据主机名，得到其IP地址
           """

def lanAll(startip):
    index=string.rfind(startip,'.')    #找最右边的.的索引
    ipfirstpart=startip[0:index+1]
    intstart=string.atoi(startip[index+1 :]) #点分十进制的最后的串转为int型

    f=range(intstart,255)
    #print f
    global g_mutex      #互斥量。不能定义称全局变量，否则，目标函数不认同
    g_mutex=threading.Lock()    #初始化互斥量
    
    for iplastpart in f:
        targetip=ipfirstpart + str(iplastpart)
        #创建线程对象，存为th。线程要执行的函数由target指定，args指定参数，可以是元组~。线程号从1开始
        th=threading.Thread(target=lanIp2Name,args=(iplastpart - intstart +1 ,targetip))
        thread_pool.append(th)
        th.start()
        
    #阻塞主线程。collect all threads
    pos=intstart
    for pos in f:
        threading.Thread.join(thread_pool[pos-intstart])

    #输出结果
    hosts=range(0,len(list_of_name))
    for host in hosts:
        print list_of_ip[host],'  ====>   ',list_of_name[host]
    print 'Find ',len(list_of_name),' Hosts.Done!'
        
def lanIp2Name(t_id,ip):
    try:
        (name,aliaslist,addresslist)=socket.gethostbyaddr(ip)
    except:
        return

    global g_mutex        #再次声明
    g_mutex.acquire() 
    ######################受互斥量保护区代码##################################
    list_of_name.append(name)
    list_of_ip.append(ip)
    ########################################################################
    g_mutex.release()

def lanIpToName(ip):
    try:
        (name,aliaslist,addresslist)=socket.gethostbyaddr(ip)
    except:
        return
    print name,"    ====>   ",addresslist   

    
def lanName2Ip(name):
    targetip=socket.gethostbyname(name)
    print name,"    ====>   ",targetip
     
'''
一个.py文件，如果是自身在运行，那么他的__name__值就是"__main__"；
如果它是被别的程序导入的（作为一个模块），则__name__就不是__main__
'''
if '__main__' == __name__:          
    '''
    sys.argv[]是用来获取命令行参数的，sys.argv[0]表示代码本身文件路径
    array.count(x)  返回出现的x的次数
    '''
    lanAll("192.168.0.1")
    while True:
        pass
    if len(sys.argv)< 3 :
         print "参数错误"
         showInfo()
         exit(1)
     
    cmds = ['-all', '-ip','-hostname']
     
    cmd = sys.argv[1]
    target=sys.argv[2]

    if 0 == cmds.count(cmd):  
        print cmd
        print "参数错误啊"
        showInfo()
        exit(1)
    else:
        print 'Start working,Please waiting...'
        if cmd == '-all':
            lanAll(target)
                            
        elif cmd == '-ip':
            lanIpToName(target)

        elif cmd=='-hostname':
            lanName2Ip(target)   