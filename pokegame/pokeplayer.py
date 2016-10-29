# coding:utf-8
'''
poker game player
python 2.7
winxos 2016-07-12
'''
import socket
from threading import Thread
import threading
from time import sleep
import os
import random

mutex = threading.Lock()
_DEBUG = False


class GameState:
    def __init__(self): pass

    def show_info(self): print("no show")

    def run(self): print("no run.")


class Idle(GameState):
    def show_info(self):
        os.system("cls")
        print("%40s" % "Welcome to play poker game\n\n")

    def run(self):
        self.show_info()
        try:
            print "Input player name > ",
            name = raw_input()
            POKE_PLAYER.init_player(name)
            POKE_PLAYER.start()
            self.__class__ = SearchRoom
        except Exception, e:
            print("[ERR] %s" % e)


class SearchRoom(GameState):
    def show_info(self):
        os.system("cls")
        print("\n\n\n")
        print("%30s" % "Online rooms")
        print("\n\n")

    def run(self):
        try:
            POKE_PLAYER.search_server()
            sleep(0.2)
            print "Found rooms:"
            print "%5s%10s%10s" % ("NUM", "NAME", "TYPE")
            print "-" * 25

            for id, room in enumerate(POKE_PLAYER.online_rooms):
                print "%5d%10s%10s" % (id + 1, room[1], room[2])
            self.__class__ = JoinGame
        except Exception, e:
            print("[ERR] %s" % e)


class JoinGame(GameState):
    def show_info(self):
        print("%30s" % "Join Game\n\n\n")

    def run(self):
        try:
            print "Select room number > ",
            room_num = int(raw_input()) - 1
            POKE_PLAYER.SERVER_ADDRESS = POKE_PLAYER.online_rooms[room_num][0]
            POKE_PLAYER.send_msg("join " + POKE_PLAYER.id)
            self.__class__ = Waiting
        except Exception, e:
            print("[ERR] %s" % e)


class Waiting(GameState):
    def run(self):
        print "Waiting..."
        while True:
            pass
        while not POKE_PLAYER.game_begin:
            pass
        self.__class__ = PlayState


game_finish = False


class PlayState(GameState):
    def playing(self):
        print "Input card number to play > ",
        c = int(raw_input())
        if 0 < c <= len(POKE_PLAYER.cards):
            POKE_PLAYER.send_msg("play %d" % POKE_PLAYER.cards[c - 1])
            POKE_PLAYER.get_answer = False
        else:
            print "Input out of range, Choose another one."

    def discarding(self):
        print "Oops, you have no card to play."
        print "Input card number to discard > ",
        c = int(raw_input())
        if 0 < c <= len(POKE_PLAYER.cards):
            POKE_PLAYER.send_msg("discard %d" % POKE_PLAYER.cards[c - 1])
            POKE_PLAYER.available_cards.append(POKE_PLAYER.cards[c - 1])
        else:
            print "Input out of range, Choose another one."

    def run(self):
        try:
            POKE_PLAYER.get_available_cards()
            if len(POKE_PLAYER.available_cards) > 0:
                self.playing()
            else:
                self.discarding()
            self.__class__ = Waiting
        except Exception, e:
            print("[ERR] %s" % e)


class Finished(GameState):
    def run(self):
        print "Game finished."
        print "You loss %d cards." % len(POKE_PLAYER.discard_cards)


class Player(Thread):
    udp_sock = None
    SERVER_ADDRESS = ""
    id = ""
    online_rooms = []
    cards = []
    game_begin = False
    print_lock = False
    table_cards = []
    game = Idle()
    get_answer = False
    is_turn = False
    available_cards = []
    discard_cards = []
    first_card = 6

    def begin(self):
        while True:
            self.game.run()

    def __init__(self):
        Thread.__init__(self)

    def init_player(self, id_):
        self.id = id_
        self.udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.player_port = random.randint(10000, 11000)
        self.udp_sock.bind(('0.0.0.0', self.player_port))

    def search_server(self):
        self.udp_sock.sendto("rooms", ("<broadcast>", SERVER_PORT))
        self.udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 0)

    def send_msg(self, msg):
        self.udp_sock.sendto(msg, self.SERVER_ADDRESS)

    def show_card(self, cards):
        c = [u"♠", u"♥", u"♣", u"♦"]
        n = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        last = 0
        mutex.acquire()
        for i, card in enumerate(cards):
            if card / 13 != last: print ""
            print "%2d.%s%-2s " % (i + 1, c[card / 13], n[card % 13]),
            last = card / 13
        print ""
        mutex.release()

    def is_valid_card(self, card):
        if len(self.table_cards) == 0:
            if card == self.first_card:
                return True
            else:
                return False
        if (card - self.first_card) % 13 == 0:
            return True
        if card % 13 == 0 and ((card + 1) not in self.table_cards):
            return False
        if (card + 1) % 13 == 0 and ((card - 1) not in self.table_cards):
            return False
        if (card + 1) not in self.table_cards and (card - 1) not in self.table_cards:
            return False
        return True

    def get_available_cards(self):
        self.available_cards = []
        for i, c in enumerate(self.cards):
            if self.is_valid_card(c):
                self.available_cards.append((i, c))
        return self.available_cards

    def show_available_cards(self):
        c = [u"♠", u"♥", u"♣", u"♦"]
        n = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        mutex.acquire()
        for sc in self.available_cards:
            print "%2d.%s%-2s " % (sc[0] + 1, c[sc[1] / 13], n[sc[1] % 13]),
        print ""
        mutex.release()

    def run(self):
        try:
            while True:
                data, addr = self.udp_sock.recvfrom(1024)
                if _DEBUG: print("[%s] get [%s] from %s" % (self.id, data, addr))
                datas = data.split()
                op = datas[0]
                if op == "room":
                    self.online_rooms.append((addr, datas[1], datas[2], data[3], data[4]))
                elif op == "card":
                    self.cards.append(int(datas[1]))
                elif op == "first":
                    self.cards = sorted(self.cards)
                    card = int(datas[1])
                    self.game_begin = True
                    print "Your cards:"
                    self.show_card(self.cards)
                    if card in self.cards:
                        print "It's your turn."
                        self.is_turn = True
                elif op == "valid":
                    card = int(datas[1])
                    self.cards.remove(card)
                    self.get_answer = True
                    self.is_turn = False
                    print "Your cards:"
                    self.show_card(self.cards)
                elif op == "table":
                    self.table_cards.append(int(datas[1]))
                    self.table_cards = sorted(self.table_cards)
                    print "Table cards:"
                    self.show_card(self.table_cards)
                elif op == "illegal":
                    print "Play illegal, Choose another one."
                    self.get_answer = True
                elif op == "turn":
                    print "It's your turn."
                    self.is_turn = True
                    self.get_available_cards()
                    print "You can play:"
                    self.show_available_cards()

        except KeyboardInterrupt:
            print("[ERR] user stop.")


SERVER_PORT = 9999
POKE_PLAYER = Player()


def main():
    POKE_PLAYER.begin()


if __name__ == '__main__':
    main()
