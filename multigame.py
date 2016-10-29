# coding:utf-8
'''
multiplayer game test
python 2.7
winxos 2016-07-11
'''
import socket
from threading import Thread
from time import sleep
SERVERIP = 'localhost'
SERVERPORT = 9999


class Server(Thread):
    state = "idle"
    players = []
    player_num = 3
    udpsock = None

    def __init__(self):
        Thread.__init__(self)
        self.udpsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.udpsock.bind(('0.0.0.0', SERVERPORT))

    def sendall_except(self, msg, naddr):
        for a, n in self.players:
            if a != naddr:
                self.udpsock.sendto(msg, a)

    def get_players(self):
        msg = ""
        for a, n in self.players:
            msg += n+" "
        return msg

    def run(self):
        try:
            while True:
                data, addr = self.udpsock.recvfrom(1024)
                print("[SERVER] get [%s] from %s\n" % (data, addr))
                datas = data.split()
                if datas[0] == "join":
                    self.players.append((addr, datas[1]))
                    if len(self.players)==3:
                        state="ready"
                    elif len(self.players)<3:
                        state="waiting"

                    #print (self.players)
                    self.sendall_except(("%s %s") % (datas[1], "joined"), addr)
                elif datas[0] == "getplayers":
                    self.udpsock.sendto("players " + self.get_players(), addr)
                print "SERVER STATE %s" % state
        except KeyboardInterrupt:
            print("[sys err] user stop.")


class Player(Thread):
    udpsock = None

    def __init__(self, id_):
        Thread.__init__(self)
        self.id = id_
        self.udpsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def sendmsg(self, msg):
        self.udpsock.sendto(msg, (SERVERIP, SERVERPORT))

    def run(self):
        self.sendmsg(("%s %s") % ("join", self.id))
        try:
            while True:
                data, addr = self.udpsock.recvfrom(1024)
                print("[%s] get [%s] from %s\n" % (self.id, data, addr))
                datas = data.split()
        except KeyboardInterrupt:
            print("[sys err] user stop.")


def main():
    s = Server()
    s.start()
    p = Player('www')
    p.start()
    p.sendmsg("getplayers")
    p2 = Player('zzz')
    p2.start()
    sleep(0.5)
    p2.sendmsg("getplayers")
    p3=Player('ppp')
    p3.start()
    while True:
        pass
if __name__ == '__main__':
    main()
