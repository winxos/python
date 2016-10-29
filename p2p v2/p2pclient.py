# -*- coding: utf-8 -*-
'''
p2p client. 
version:2.0
winxos 2015-12-05
'''
import socket
import threading
import os
import random
import time
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # DGRAM -> UDP
server_addr = ('121.41.45.145', 9000)
#server_addr = ('10.0.0.5', 9000)
s.bind(('0.0.0.0', random.randint(10000, 50000)))
nick_name = "somiar"
password = "112211"
clients_addr = {}
is_exit = False


def get_addr(name):
    if name in clients_addr:
        return clients_addr[name]
    return None


def get_user(addr):
    for name, ad in clients_addr.items():
        if addr == ad:
            return name
    return None


class heartpack(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while not is_exit:
            try:
                s.sendto("client heart %s" % nick_name, server_addr)
                time.sleep(10)
            except Exception, e:
                print("[heart err] %s" % e)


class getcmd(threading.Thread):
    global s, clients

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while not is_exit:
            try:
                cmd = raw_input()
                cmds = cmd.split()
                if cmds == None:
                    continue
                op = cmds[0]
                if op == "p":
                    print(clients_addr)
                elif op == "link":
                    if len(cmds) > 1:
                        s.sendto("client getaddr %s" % cmds[1], server_addr)
                        time.sleep(0.3)  # wait getaddr return
                        s.sendto("", get_addr(cmds[1]))
                        s.sendto("client link %s" % cmds[1], server_addr)

                elif op == "to":
                    addr = get_addr(cmds[1])
                    if addr:
                        s.sendto(" ".join(cmds[2:]), addr)
                elif op == "connect":  # login
                    s.sendto("client connect %s %s" %
                             (nick_name, password), server_addr)
                elif op == "getaddr":
                    if len(cmds) > 1:
                        s.sendto("client getaddr %s" % cmds[1], server_addr)
                elif op == "getusers":
                    s.sendto("client getusers", server_addr)

            except Exception, e:
                print("[shell err] %s" % e)
                # break


class listener(threading.Thread):
    global s, clients

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while not is_exit:
            data, addr = s.recvfrom(1024)
            t = get_user(addr)
            if t:
                print("%s -> %s" % (t, data))
            else:
                print("[log] [%s] %s" % (str(addr), data))
            try:
                if data != "":
                    datas = data.split()
                    cmdflag = datas[0]
                    if cmdflag == "server":
                        cmd = datas[1]
                        if cmd == "retaddr":
                            if datas[2] == "offline":
                                pass
                            else:
                                clients_addr[datas[2]] = (
                                    datas[3], int(datas[4]))
                        elif cmd == "retaddrs":
                            pass
                        elif cmd == "link":
                            s.sendto("answer from %s" %
                                     nick_name, (datas[2], int(datas[3])))

                    elif cmdflag == "client":  # client from name
                        cmd = datas[1]
                        if cmd == "from":
                            clients_addr[datas[2]] = addr
                            print("%s connected" % datas[2])
                    elif cmdflag == "answer":  # answer from name
                        cmd = datas[1]
                        if cmd == "from":
                            s.sendto("client from %s" % nick_name, addr)
                            print("connected to %s" % datas[2])

            except Exception, e:
                print("[listen err] %s" % e)


if __name__ == '__main__':
    nick_name = raw_input("input your name:")
    s.sendto("client connect %s %s" %
             (nick_name, password), server_addr)
    h = heartpack()
    h.setDaemon(True)  # important
    h.start()
    t = getcmd()
    t.setDaemon(True)  # important
    t.start()
    l = listener()
    l.setDaemon(True)
    l.start()
    try:
        while h.isAlive() and t.isAlive() and l.isAlive():
            time.sleep(1)
    except KeyboardInterrupt:
        print("[sys err] user stop.")
    is_exit = True
    print("app exit.")
    os._exit(0)
