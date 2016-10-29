#-*- coding: utf-8 -*-
'''
扫描局域网联网设备及MAC地址
用于自动接入控制
winxos 2015-09-10
'''
import os
import threading
from Queue import Queue
import time


def ping_ip(ip):
    cmd = ["ping", "-n 2 -w 100", ip]
    output = os.popen(" ".join(cmd)).readlines()

    flag = False
    for line in output:
        if not line:
            continue
        if str(line).upper().find("TTL") >= 0:
            flag = True
            break
    return flag


def get_mac(ip):
    output = os.popen("arp -a").readlines()
    for i in output:
        cmds = i.split()
        if len(cmds) > 1:
            if cmds[0] == ip:
                return cmds[1]
    return None

class get_ip_t(threading.Thread):

    def __init__(self, ip):
        self.ip = ip
        threading.Thread.__init__(self)  # 初始化，必须

    def run(self):
        try:
            self.result = ping_ip(self.ip)
        except Exception as e:
            print ("!%s: %s" % (self.ip, e))
# 多线程文件下载，线程池


def get_ip_t_pools(ips):
    finished = []  # 用于存放结果
    ct = [0]

    def producer(q, ips):  # 用于产生线程
        for ip in ips:
            thread = get_ip_t(ip)
            thread.start()
            q.put(thread, True)

    def consumer(q, nums):  # 线程调用
        while ct[0] < nums:  # 线程未完成
            thread = q.get(True)
            thread.join()
            ct[0] += 1
            # print thread.ip,thread.result
            if thread.result:
                finished.append(thread.ip)  # 完成任务结果加入列表

    q = Queue(len(ips))  # 线程池大小
    prod = threading.Thread(target=producer, args=(q, ips))  # 线程使用
    cons = threading.Thread(target=consumer, args=(q, len(ips)))
    prod.start()
    cons.start()
    prod.join()
    cons.join()  # 等待完成
    return finished
iph = '192.168.0.'
ips = []
for i in range(100, 200):
    ips.append(iph + str(i))

flag = False
oldips = set()
timeout_times = 3
online_clients = {}
while True:
    res = get_ip_t_pools(ips)
    for i in res:
        if not i in online_clients:
            print("%s> [%2d]:[join] %s,%s" %
                  (time.strftime("%H:%M:%S"), len(online_clients) + 1, i, get_mac(i)))
        online_clients[i] = 1
    ds = []
    for i in online_clients:
        if not i in res:
            online_clients[i] -= 1
            if online_clients[i] < -2:
                ds.append(i)
    for i in ds:
        del online_clients[i]
        print("%s> [%2d]:[exit] %s" %
              (time.strftime("%H:%M:%S"), len(online_clients), i))
#    for ip in res:
#        get_mac(ip)
