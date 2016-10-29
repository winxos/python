# -*- coding: utf-8 -*-
'''
p2p server.
winxos 2015-12-04
'''
import socket
import threading
import os
import time
port = 9010
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # DGRAM -> UDP

is_exit = False

class getcmd(threading.Thread):
    global s, clients

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while not is_exit:
            try:
                cmd = raw_input()
                cmds = cmd.split()
                op = cmds[0]
                if op == "to":
                    if cmds[3].isdigit():#port range
                        for i in range(int(cmds[2]),int(cmds[3])):
                            s.sendto(" ".join(cmds[4:]), (cmds[1],i))
                            if i%1000==0:
                                time.sleep(1);
                    else:
                        s.sendto(" ".join(cmds[3:]), (cmds[1],int(cmds[2])))
            except Exception, e:
                print("[shell err] %s" % e)


class listener(threading.Thread):
    global s, clients

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while not is_exit:
            try:
                data, addr = s.recvfrom(1024)
                print("%s:%s" % (addr, data))
            except Exception, e:
                print("[listen err] %s" % e)

if __name__ == '__main__':
    port = raw_input("input port:")
    s.bind(('0.0.0.0', int(port)))
    t = getcmd()
    t.setDaemon(True)  # important
    t.start()
    l = listener()
    l.setDaemon(True)
    l.start()
    print("listening...")
    try:
        while t.isAlive() and l.isAlive():
            pass
    except KeyboardInterrupt:
        print("[sys err] user stop.")
    is_exit = True
    print("server exit.")
    os._exit(0)
