# coding:utf-8
class Taketen:
    board = []
    board_col = 9

    def add_num(self, n):
        s = str(n)
        for ss in s:
            self.board.append(ss)

    def show(self):
        for i, n in enumerate(self.board):
            if i > 0 and i % 9 == 0: print ""
            if n != 0:
                print "%2s" % n,
            else:
                print "%2s" % ".",

    def is_match(self, i1, i2):
        if i1 >= i2: return False
        if self.board[i1] != self.board[i2]: return False
        def is_continual_match(i1, i2):
            for i in xrange(i1 + 1, i2):
                if self.board[i] != 0: return False
            return True
        def is_vehiclel_match(i1,i2):
            if (i2-i1)% self.board_col!=0: return False
            for i in xrange(i1 + self.board_col, i2, self.board_col):
                if self.board[i] != 0: return False
            return True
        return is_continual_match(i1, i2)

    def __init__(self):
        for i in xrange(1, 20):
            if i != 10:
                self.add_num(i)
        print self.is_match(9, 9)
        self.show()


t = Taketen()
