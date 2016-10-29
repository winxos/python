#!/usr/bin/python
# Author: Yan Li
# Licence: BSD-like licence
from copy import deepcopy
import sys
import time
import argparse


class Record:
    def __init__(self):
        self.check = [False] * 9
        self.value = -1
        self.feasible = 9

    def set(self, v):
        if self.value != -1 and self.value != v:
            raise ValueError

        if self.check[v - 1]:
            raise ValueError
        self.value = v
        self.feasible = 1

    def eliminate(self, v):
        if self.value != -1:
            return

        if not self.check[v - 1]:
            self.check[v - 1] = True
            self.feasible -= 1
        if self.feasible == 0:
            raise ValueError


class SolveBuffer:
    def __init__(self):
        self.buf = [[None for i in xrange(9)] for j in xrange(9)]
        for i in xrange(9):
            for j in xrange(9):
                self.buf[i][j] = Record()

    def solved(self):
        for i in xrange(9):
            for j in xrange(9):
                if self.buf[i][j].value == -1:
                    return False
        return True

    def populate(self, i, j, v):
        self.buf[i][j].set(v)
        # row elimination
        for tj in xrange(9):
            self.buf[i][tj].eliminate(v)

        # column elimination
        for ti in xrange(9):
            self.buf[ti][j].eliminate(v)

        # block elimination
        for ti in xrange(i / 3 * 3, i / 3 * 3 + 3):
            for tj in xrange(j / 3 * 3, j / 3 * 3 + 3):
                self.buf[ti][tj].eliminate(v)

    def find_one(self):
        # trivial solution first
        for i in xrange(9):
            for j in xrange(9):
                if self.buf[i][j].value == -1 and self.buf[i][j].feasible == 1:
                    for k in xrange(9):
                        if not self.buf[i][j].check[k]:
                            return i, j, k + 1
        # non-trivial solution
        for x in xrange(1, 10):
            # row check
            for i in xrange(9):
                cnt, a, b = 0, 0, 0
                for j in xrange(9):
                    if self.buf[i][j].value == x:
                        cnt = 0
                        break
                    elif self.buf[i][j].value == -1 and not self.buf[i][j].check[x - 1]:
                        cnt += 1
                        a, b = i, j
                if cnt == 1:
                    return a, b, x

            # column check
            for j in xrange(9):
                cnt, a, b = 0, 0, 0
                for i in xrange(9):
                    if self.buf[i][j].value == x:
                        cnt = 0
                        break
                    elif self.buf[i][j].value == -1 and not self.buf[i][j].check[x - 1]:
                        cnt += 1
                        a, b = i, j
                if cnt == 1:
                    return a, b, x

            # block
            for block in xrange(9):
                cnt, a, b = 0, 0, 0
                for i in xrange(block / 3 * 3, block / 3 * 3 + 3):
                    done = False
                    for j in xrange(block % 3 * 3, block % 3 * 3 + 3):
                        if self.buf[i][j].value == x:
                            cnt = 0
                            done = True
                            break
                        elif self.buf[i][j].value == -1 and not self.buf[i][j].check[x - 1]:
                            cnt += 1
                            a, b = i, j
                    if done:
                        break
                if cnt == 1:
                    return a, b, x
        return -1, -1, None

    def find_first_feasible(self):
        l = []
        for i in xrange(9):
            for j in xrange(9):
                if self.buf[i][j].value == -1 and self.buf[i][j].feasible > 0:
                    for k in xrange(9):
                        if not self.buf[i][j].check[k]:
                            l.append(k + 1)
                    return i, j, l
        return -1, -1, []


class Sudoku:
    def __init__(self, b):
        self.board = b
        self.sb = SolveBuffer()

    def dump(self):
        ans=""
        for i in xrange(9):
            for j in xrange(9):
                v = self.sb.buf[i][j].value
                if v == -1:
                    ans+='-',
                else:
                    ans+= "%d"%v
        return ans

    def do_solve(self, sb):
        try:
            while True:
                i, j, v = sb.find_one()
                if not v:
                    break
                sb.populate(i, j, v)
        except ValueError:
            return False

        if sb.solved():
            return True

        ti, tj, l = sb.find_first_feasible()
        if ti == -1:
            return False

        tsb = SolveBuffer()
        solved = False
        for tv in l:
            tsb.buf = deepcopy(sb.buf)
            tsb.populate(ti, tj, tv)
            if self.do_solve(tsb):
                solved = True
                break

        if solved:
            sb.buf = deepcopy(tsb.buf)
            return True
        return False

    def solve(self):
        self.sb = SolveBuffer()

        for i in xrange(9):
            for j in xrange(9):
                if self.board[i][j] > 0:
                    self.sb.populate(i, j, self.board[i][j])

        return self.do_solve(self.sb)


def load_args(data):
    a = [None] * 9
    for i, d in enumerate(data.split()):
        a[i] = [int(c) for c in d]
    return a

if __name__ =="__main__":
    board = load_args("030007004 602041000 050030967 040003006 087000350 900700020 718020040 000160809 400500030")
    print board
    s = Sudoku(board)

    print "********* SOLVE BEGIN *********\n\n\n"
    print "\n\n\nThe solution is ...\n"
    begin = time.time()
    if not s.solve():
        print "The problem can not be solved"
        sys.exit(0)

    timeCost = (time.time() - begin) * 1000
    print s.dump()
    print "********* SOLVE DONE*********"
    print "Total Cost: ", timeCost, "Mili Seconds"
