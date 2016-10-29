#coding:utf-8
c = [u"♠", u"♥", u"♣", u"♦"]
n = [" A", " 2", " 3", " 4", " 5", " 6", " 7", " 8", " 9", "10", " J", " Q", " K"]
for i, card in enumerate([0,5,10,20,30,22]):
    print c[card / 13], n[card % 13], " ",
print ""