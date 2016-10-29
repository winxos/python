# coding:utf-8
'''
poker game server
python 2.7
winxos 2016-07-12
'''
import socket
from threading import Thread
from time import sleep
import os
import random


class game_state:
    def show_info(self): print("no show")

    def run(self): print("no run.")


class Idle(game_state):
    def show_info(self):
        os.system("cls")
        print("%40s" % "Welcome to play poker game\n\n")
        print("%30s" % "1. Create game")

    def run(self):
        try:
            self.show_info()
            print "Input operation > ",
            cmd = raw_input()
            if cmd == "1":
                self.__class__ = CreateRoom
        except Exception, e:
            print("[ERR] %s" % e)


class CreateRoom(game_state):
    def show_info(self):
        os.system("cls")
        print("\n\n\n")
        print("%30s" % "Poke Room Creating")
        print("\n\n")

    def run(self):
        try:
            self.show_info()
            print "Please input room name > ",
            room_name = raw_input()
            print "Please input player numbers > ",
            player_number = int(raw_input())
            G_SEV.init_server(room_name, player_number)
            G_SEV.start()
            self.__class__ = WaitJoin
        except Exception, e:
            print("[ERR] %s" % e)


class WaitJoin(game_state):
    def show_info(self):
        os.system("cls")
        print("\n\n\n")
        print("%30s" % "Wait player join")
        print("\n\n")

    def run(self):
        self.show_info()
        while True:
            if len(G_SEV.players) == G_SEV.player_num:
                break
        print "\nGame start"
        self.__class__ = SendCard


class SendCard(game_state):
    def init_card(self):
        G_SEV.cards = [i for i in range(G_SEV.total_cards)]
        random.shuffle(G_SEV.cards)

    def run(self):
        self.init_card()
        print "Sending card..."
        index = 0
        while len(G_SEV.cards) > 0:
            c = G_SEV.cards.pop()
            a, n = G_SEV.players[index]
            G_SEV.send_to_player("card %d" % c, index)
            index += 1
            if index == len(G_SEV.players):
                index = 0

        self.__class__ = Playing


class Playing(game_state):
    def run(self):
        print "Game playing"
        G_SEV.send_to_all("first %d" % G_SEV.first_card)
        while True:
            pass


class Server(Thread):
    players = []
    player_num = 3
    udpsock = None
    room_name = ""
    cards = []
    game_type = "bie7"
    first_card = 6
    total_cards = 12
    game = CreateRoom()
    playing_index = 0

    def test(self):
        while True:
            self.game.run()

    def init_server(self, rname, pnum):
        self.room_name = rname
        self.player_num = pnum
        self.udpsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.udpsock.bind(('0.0.0.0', SERVER_PORT))

    def send_to_all_except(self, msg, naddr):
        for a, n in self.players:
            if a != naddr:
                self.udpsock.sendto(msg, a)

    def send_to_all(self, msg):
        print "send to all < %s" % msg
        for a, n in self.players:
            self.udpsock.sendto(msg, a)

    def send_to_player(self, msg, index):
        print "send to player %d < %s" % (index, msg)
        self.udpsock.sendto(msg, self.players[index][0])

    def send_to(self, msg, addr):
        print "send to %s < %s" % (str(addr), msg)
        self.udpsock.sendto(msg, addr)

    def get_players(self):
        msg = ""
        for a, n in self.players:
            msg += n + " "
        return msg

    def is_valid_card(self, card):
        if len(self.cards) == 0:
            if card == self.first_card:
                return True
            else:
                return False
        if (card - 6) % 13 == 0:
            return True
        if card % 13 == 0 and ((card + 1) not in self.cards):
            return False
        if (card + 1) % 13 == 0 and ((card - 1) not in self.cards):
            return False
        if (card + 1) not in self.cards and (card - 1) not in self.cards:
            return False
        return True

    def run(self):
        try:
            while True:
                data, addr = self.udpsock.recvfrom(1024)
                print("[server] get [%s] from %s" % (data, addr))
                datas = data.split()
                op = datas[0]
                if op == "rooms":
                    self.udpsock.sendto(
                            "room %s %s %d %d" % (
                                G_SEV.room_name, G_SEV.game_type, len(G_SEV.players), G_SEV.player_num),
                            addr)
                elif op == "join":
                    G_SEV.players.append((addr, datas[1]))
                    print ("Current player %d, Total need %d" % (len(G_SEV.players), G_SEV.player_num))
                    self.send_to_all(("%s %s") % (datas[1], "joined"))
                elif op == "play":
                    card = int(datas[1])
                    if self.is_valid_card(card):
                        if card == self.first_card:
                            for i, p in enumerate(self.players):
                                if addr in p:
                                    self.playing_index = i
                        self.cards.append(card)
                        self.send_to("valid %d" % card, addr)
                        self.playing_index += 1
                        if self.playing_index >= len(self.players):
                            self.playing_index = 0
                        self.send_to_player("turn", self.playing_index)
                        self.send_to_all("table %s" % card)
                    else:
                        self.send_to("illegal", addr)

                elif op == "getplayers":
                    self.send_to("players " + self.get_players(), addr)
        except KeyboardInterrupt:
            print("[ERR] user stop.")


SERVER_PORT = 9999
G_SEV = Server()


def main():
    G_SEV.test()


if __name__ == '__main__':
    main()
