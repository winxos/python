# coding:utf-8
# none repeated permutation algorithm
# winxos 2016-04-19


class Node(object):
    pass


class Operator(Node):

    def __init__(self, left, right):
        self.left = left
        self.right = right


class Number(Node):

    def gcd(self, x, y):
        if y == 0:
            return x
        return self.gcd(y, x % y)

    def norm(self):
        a = self.gcd(self.numerator, self.denominator)
        self.numerator /= a
        self.denominator /= a

    def __init__(self, nume, deno=1):
        self.numerator = nume
        self.denominator = deno
        self.norm()

    def __add__(self, other):
        return Number(self.numerator * other.denominator + self.denominator * other.numerator, self.denominator * other.denominator)

    def __sub__(self, other):
        return Number(self.numerator * other.denominator - self.denominator * other.numerator, self.denominator * other.denominator)

    def __mul__(self, other):
        return Number(self.numerator * other.numerator, self.denominator * other.denominator)

    def __div__(self, other):
        return Number(self.numerator * other.denominator, self.denominator * other.numerator)

    def __str__(self):
        if self.denominator == 1:
            return "%d" % self.numerator
        else:
            return "%d/%d" % (self.numerator, self.denominator)


class Add(Operator):
    pass


class Sub(Operator):
    pass


class Mul(Operator):
    pass


class Div(Operator):
    pass


class Visitor:

    def visit(self, node):
        mn = "visit_" + type(node).__name__
        m = getattr(self, mn, None)
        if m is None:
            m = self.generic_visit
        return m(node)

    def generic_visit(self, node):
        raise RuntimeError('Miss {}'.format('visit_' + type(node).__name__))


class Eval(Visitor):

    def visit_Number(self, node):
        return node

    def visit_Add(self, node):
        return self.visit(node.left) + self.visit(node.right)

    def visit_Sub(self, node):
        return self.visit(node.left) - self.visit(node.right)

    def visit_Mul(self, node):
        return self.visit(node.left) * self.visit(node.right)

    def visit_Div(self, node):
        return self.visit(node.left) / self.visit(node.right)

t1 = Div(Number(3), Number(7))
t2 = Add(t1, Number(3))
t3 = Mul(t2, Number(7))
e = Eval()
e.visit(t3)

def format_input(li):
    ans = {}
    for i in li:
        ans[i] = ans[i] + 1 if i in ans else 1
    return ans
def permutation_norepeat_num(dl):
    if len(dl) == 1:
        return 1
    ans = 0
    for d, x in dl.items():
        dt = dl.copy()
        # print d,x,"->",
        x -= 1
        if x == 0:del dt[d]
        else:dt[d] = x
        # print dt
        ans += permutation_norepeat_num(dt)
    return ans
print permutation_norepeat_num(format_input([7, 7, 2, 2]))
