# coding:utf-8
'''
multiplayer game test
python 2.7
winxos 2016-07-11
'''
import socket
from threading import Thread
from time import sleep
import os

SERVER_PORT = 9999
PLAYER_PORT = 10001
POKE_SERVER = None
POKE_PLAYER =None

class game_state:

    def show_info(self): print("no show")

    def run(self): print("no run.")


class Idle(game_state):

    def show_info(self):
        os.system("cls")
        print("%40s" % "welcome to play poker game\n\n")
        print("%30s" % "1. create game")
        print("%30s" % "2.   join game")
        print "input number to select > ",

    def run(self):
        try:
            cmd = raw_input()
            if cmd == "1":
                self.__class__ = ServerSetting
            elif cmd == "2":
                self.__class__ = PlayerSelectRoom
        except Exception, e:
            print("[ERR] %s" % e)


class ServerSetting(game_state):

    def show_info(self):
        os.system("cls")
        print("\n\n\n")
        print("%30s" % "game setting")
        print("\n\n")

    def run(self):
        try:
            print "please input room name > ",
            room_name = raw_input()
            print "please input player numbers > ",
            player_number = int(raw_input())
            poke_server = Server(room_name, player_number)
            poke_server.start()
            self.__class__ = GameBoard
        except Exception, e:
            print("[ERR] %s" % e)


class PlayerSelectRoom(game_state):

    def show_info(self):
        print("\n\n\n")
        print("%30s" % "room live")

    def run(self):
        try:
            print "please input your name > ",
            name = raw_input()
            POKE_PLAYER = Player(name)
            POKE_PLAYER.start()
            POKE_PLAYER.search_server()
            self.__class__ = GameBoard
        except Exception, e:
            print("[ERR] %s" % e)


class GameBoard(game_state):
    pass


class Server(Thread):
    state = "idle"
    players = []
    player_num = 3
    udpsock = None
    room_name = ""

    def __init__(self, rname, pnum):
        Thread.__init__(self)
        self.room_name = rname
        self.player_num = pnum
        self.udpsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.udpsock.bind(('0.0.0.0', SERVER_PORT))

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
                print("[server] get [%s] from %s\n" % (data, addr))
                datas = data.split()
                if datas[0] == "join":
                    self.players.append((addr, datas[1]))
                    if len(self.players) == 3:
                        self.state = "ready"
                    elif len(self.players) < 3:
                        self.state = "waiting"

                    # print (self.players)
                    self.sendall_except(("%s %s") % (datas[1], "joined"), addr)
                elif datas[0] == "getplayers":
                    self.udpsock.sendto("players " + self.get_players(), addr)
                print "server state %s" % self.state
        except KeyboardInterrupt:
            print("[ERR] user stop.")


class Player(Thread):
    udpsock = None
    serverip=""
    id=""
    def __init__(self, id_):
        Thread.__init__(self)
        self.id = id_
        self.udpsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udpsock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.udpsock.bind(('0.0.0.0', PLAYER_PORT))
    def search_server(self):
        self.udpsock.sendto("JOIN "+self.id,("<broadcast>",SERVER_PORT))
    def sendmsg(self, msg):
        self.udpsock.sendto(msg, (self.serverip, SERVER_PORT))

    def run(self):
        try:
            while True:
                data, addr = self.udpsock.recvfrom(1024)
                print("[%s] get [%s] from %s\n" % (self.id, data, addr))
                datas = data.split()
        except KeyboardInterrupt:
            print("[ERR] user stop.")
is_exit = False


class PokeGame:
    game = Idle()

    def test(self):
        oldstate = None
        while oldstate != self.game.__class__:
            oldstate = self.game.__class__
            self.game.show_info()
            self.game.run()
            sleep(0.05)


def main():
    # s = server()
    # s.start()
    # p = player('www')
    # p.start()
    # p.sendmsg("getplayers")
    # p2 = player('zzz')
    # p2.start()
    # sleep(0.5)
    # p2.sendmsg("getplayers")
    # p3 = player('ppp')
    # p3.start()
    pg = PokeGame()
    pg.test()
if __name__ == '__main__':
    main()
