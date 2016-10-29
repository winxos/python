# -*- coding: utf-8 -*-
'''
p2p server.
version:2.0
winxos 2015-12-05
'''
import socket
import threading
import os
import time
port = 9000
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # DGRAM -> UDP
s.bind(('0.0.0.0', port))

clients_addr = {}
clients_timeout = {}
clients_pwd = {}
is_exit = False


def get_addr(name):
    if name in clients_addr:
        return clients_addr[name]
    return None


def login(name, pwd):
    if name in clients_pwd:
        if clients_pwd[name] == pwd:
            return 0  # success
        else:
            return 1  # error password
    else:
        return 2  # new user


def response(msg, addr, paras=""):
    s.sendto("server %s %s" % (msg, paras), addr)


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
                    print(clients_pwd)
                elif op == "to":
                    print("send to")
                    addr = get_addr(cmds[1])
                    if addr:
                        s.sendto(cmds[2], addr)
            except Exception, e:
                print("[shell err] %s" % e)


class listener(threading.Thread):
    global s, clients

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while not is_exit:
            data, addr = s.recvfrom(1024)
            print("%s:%s" % (addr, data))
            try:
                datas = data.split()
                if len(datas) == 0:
                    continue
                if datas[0] == "client":
                    op = datas[1]
                    if op == "heart":
                        useraddr = get_addr(datas[2])
                        if useraddr == addr:
                            clients_timeout[datas[2]] = 0
                        else:
                            response("disconnect", addr)
                    elif op == "connect":
                        nick = datas[2]
                        pwd = datas[3]
                        n = login(nick, pwd)
                        if n == 0:
                            clients_addr[nick] = addr
                            clients_timeout[nick] = 0
                        elif n == 1:
                            response("connect", addr, "failed")
                        elif n == 2:
                            clients_pwd[nick] = pwd
                            clients_addr[nick] = addr
                            clients_timeout[nick] = 0
                            response("connect", addr, "newuser")
                    elif op == "getaddr":
                        if len(datas) < 3:
                            pass
                        else:
                            dest = datas[2]
                            useraddr = get_addr(dest)
                            if useraddr:
                                response("retaddr", addr, "%s %s" %
                                         (dest, "%s %s" % useraddr))
                            else:
                                response("retaddr", addr, "offline")
                    elif op == "getusers":
                        response("retusers", addr, "%s" %
                                 " ".join(clients_addr))
                    elif op == "link":  # a ask b
                        dest = datas[2]
                        useraddr = get_addr(dest)
                        response("link", useraddr, "%s %s" % addr)
            except Exception, e:
                print("[listen err] %s" % e)

if __name__ == '__main__':
    print("server running...")
    t = getcmd()
    t.setDaemon(True)  # important
    t.start()
    l = listener()
    l.setDaemon(True)
    l.start()
    try:
        while t.isAlive() and l.isAlive():
            tmp=clients_timeout.copy()
            for key in tmp:
                clients_timeout[key] += 1
                if clients_timeout[key] > 35: #35 seconds timeout
                    del clients_addr[key]
                    del clients_timeout[key]
                    print("%s offline"%key)
            time.sleep(1)
    except KeyboardInterrupt:
        print("[sys err] user stop.")
    is_exit = True
    print("server exit.")
    os._exit(0)
