# coding:utf-8
# 二分取样算法
# winxos 2016-11-09
det = 0.1


def fy(current, need, taken=0, discard=0):
    print("taken:%.1f, discard:%.1f" % (taken, discard))
    if abs(taken - need) <= det * need:  # finished
        discard += current
        print("taken:%.1f, discard:%.1f" % (taken, discard))
        return
    if current / 2.0 + taken <= need:
        fy(current / 2.0, need, taken + current / 2.0, discard)
    else:
        fy(current / 2.0, need, taken, discard + current / 2.0)


fy(1000, 70)
