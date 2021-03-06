# coding:utf-8
# none repeated permutation algorithm
# winxos 2016-04-19
from fractions import Fraction


class Node(object):
    pass


class Operator(Node):

    def __init__(self, left, right):
        self.left = left
        self.right = right


class Number(Node):

    def __init__(self, value):
        self.value = Fraction(value)


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
        return node.value

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
ops=[Add,Sub,Div,Mul]
for op in ops:
    t=op(Number(3),Number(7))
    e=Eval()
    print e.visit(t)
def permutation_norepeat(li):
    '''create permutation without repeat
    input :list, output:list of all permutation
    eg. input [7,7,3], output [[3,7,7],[7,3,7],[7,7,3]]
    '''
    def _format_input(li):
        ans = {}
        for i in li:
            ans[i] = ans[i] + 1 if i in ans else 1
        return ans
    def _permutation_norepeat(dl, out, s=[]):
        if len(dl) == 0:
            out.append(s)
            return
        for d, x in dl.items():
            dt = dl.copy()
            sc = s[:]
            sc.append(d)
            x -= 1
            if x == 0:del dt[d]
            else:dt[d] = x
            _permutation_norepeat(dt, out, sc[:])
    o = []
    _permutation_norepeat(_format_input(li), o)
    return o
print permutation_norepeat([7,7,3,3]) 