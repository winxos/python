#!/usr/bin/python
import math
from itertools import product
from itertools import permutations
from copy import deepcopy

operands  = [8,8,3,3]
operators = ['+', '-', '*', '/']

def isOperator(op):
  return op in operators

def isOperand(op):
  return op in operands

def add(num1, num2):
  return float(num1)+float(num2)

def sub(num1, num2):
  return float(num1)-float(num2)

def mul(num1, num2):
  return float(num1)*float(num2)

def div(num1, num2):
  if (float(num2) != 0.0):
    return float(num1)/float(num2)
  else:
    return float('nan')

def evalOperator(op, num1, num2):
  if (op=='+'):
    return add(num1,num2)
  if (op=='-'):
    return sub(num1,num2)
  if (op=='*'):
    return mul(num1,num2)
  if (op=='/'):
    return div(num1,num2)
  return float('nan')

def eq( a, b, eps=0.0001 ):
  if a==b:
    return True
  elif a<=0.0 or b<=0.0:
    return False
  else:
    return abs(math.log(a) - math.log(b)) <= eps

def is24( num ):
  return eq(num, 24)
  
def evalPolishExp(polishexp):
  stack = []
  for op in polishexp:
    if (op in operators):
      if (len(stack)<2):
        print("Wrong Polish Expression")
        return float('nan')
      num2 = stack.pop()
      num1 = stack.pop()
      stack.append(evalOperator(op, num1, num2))
    elif (op in operands):
      stack.append(op)
    else:
      print("Wrong Polish Expression")
      return float('nan')
  if (len(stack)!=1):
    print("Wrong Polish Expression")
    return float('nan')
  return stack[0]

def addParenth(string):
  return '('+string+')'

def isPrecedent(op1, op2):
  preDict = {'+':1, '-':1, '*':2, '/':2, 'no_op':10}
  return preDict[op1]>preDict[op2]

def isInversible(op):
  invDict = {'+':True, '-':False, '*':True, '/':False, 'no_op':True}
  return invDict[op]

def genMathStr(exp1, exp2 = '', opt = 'no_op'):
  if (opt=='no_op'):
    return [str(exp1), opt]
  if (isPrecedent(opt, exp1[1])):
    exp1[0]=addParenth(exp1[0])
  if (isPrecedent(opt, exp2[1]) or
      ((not isInversible(opt)) and
       (exp2[1] != 'no_op') and
       (not isPrecedent(exp2[1],opt)))):
    exp2[0]=addParenth(exp2[0])
  return [exp1[0]+opt+exp2[0], opt]

def genSolvStr(polshExp):
  stack = []
  for op in polshExp:
    if (op in operators):
      if (len(stack)<2):
        print("Wrong Polish Expression")
        return
      exp2 = stack.pop()
      exp1 = stack.pop()
      stack.append(genMathStr(exp1, exp2, op))
    elif (op in operands):
      stack.append(genMathStr(op))
    else:
      print("Wrong Polish Expression")
      return
  if (len(stack)!=1):
    print("Wrong Polish Expression")
    return
  return stack[0][0]

def genOpSeq(operators):
  opSeqs = list(product(operators, repeat=3))
  return list(opSeqs)

def genNumSeq(operands):
  numSeqs = list(permutations(operands, r=4))
  return numSeqs

def polishCombos(seq1,seq2):
  out=[]
  stacks=[list(seq1),list(seq2)]
  for n in tuple(product(range(2),repeat=4)):
    seq=[]
    if (sum(n)==2 and n!=(1,1,0,0)):
      stacks_cp = deepcopy(stacks)
      for i in n:
        seq.append(stacks_cp[i].pop(0))
      out.append(seq)
  return out

def genPolish(numSeq, opSeq):
  polishSeq = []
  subexps=polishCombos(numSeq[-2:],opSeq[:2])
  for sub in subexps:
    exp=[]
    for n in numSeq[:2]:exp.append(n)
    for i in sub:exp.append(i)
    exp.append(opSeq[-1])
    polishSeq.append(exp)
  return polishSeq

###
###Polish Exp Printing Utilities
def addToLevel(prt,level,i,branch='none'):
  if (branch=='left'):
    string=str(i)+'  ';
  else:
    string=str(i)
  if (len(prt)<=level):
      prt.append([string])
  else:
      prt[level].insert(0,string)
def printLevels(prt,paddings):
  for level in range(len(prt)):
    string=''
    for i in range(paddings[level]):string+=' '
    for i in prt[level]:string+=i
    print(string)
def printPolish(polishExp):
  prt=[]
  child=[]
  paddings = [10]*len(polishExp)
  for i in reversed(polishExp):
    if (len(child)!=0):
      node=child.pop()
      level=node[0]
      branch=node[1]
    else:
      level=0
      branch='none'
    if (isOperator(i)):
      addToLevel(prt,level,'\''+i+'\'',branch)
      if (branch=='right'):
        paddings[level]=paddings[level-1]+4
      elif (branch=='left'):
        paddings[level]=paddings[level-1]-1
      level+=1
      addToLevel(prt,level,'/   \\')
      paddings[level]=paddings[level-1]-1
      level+=1
      child.append([level,'left'])
      child.append([level,'right'])
    else:
      addToLevel(prt,level,' '+str(i)+' ',branch)
      if (branch=='right'):
        paddings[level]=paddings[level-1]+4
      elif (branch=='left'):
        paddings[level]=paddings[level-1]-1
  if(len(prt)==5):
    paddings[4]-=2
  printLevels(prt,paddings)
"""
                '*' 
               /   \        (-1)
              '-'  '-'      (-2)(3)
             /   \/   \     (-3)(2)
          '8'  '2''8'  '2'  (-5)(2)

          '+' 
         /   \  (-1)
        '*'  '8'(-2)
       /   \    (-3)
      '-'  '8'  (-4)
     /   \      (-5)
    '4'  '2'    (-6)

    Printing Utilities
"""

class Node:
  nodeCnt=0
  def __init__(self, op, parent='null',dummy=False):
    if (parent == 'null'):
      self.parent='null'
    else:
      self.parent=parent
    self.name=op
    self.dummy=dummy
    self.left=None
    self.right=None
    self.id=Node.nodeCnt
    Node.nodeCnt+=1

  def isHead(self):
    if (self.parent=='null'):
      return True
    else:
      return False

  def isFull(self):
    if (self.left is not None):
      return True
    else:
      return False

  def addLeaf(self, newNode):
    if (self.right is None):
      self.right = newNode
    elif (self.left is None):
      self.left = newNode

  def printme(self):
    if (self.left is None or self.right is None):
      print ('Node name: ', self.name, ', Leaves Error!')
    else:
      print('Node name: ', self.name, ', Left: ',self.left.name,
            ', right: ', self.right.name)

  def isReverse(self):
    if (not isInversible(self.name)):
      return False
    if (isOperand(self.left.name) and isOperator(self.right.name)):
      return True
    if (isOperand(self.left.name) and isOperand(self.right.name)):
      if (self.left.name < self.right.name):
        return True
    if (isOperator(self.left.name) and isOperator(self.right.name)):
      if (self.left.name < self.right.name):
        return True
    return False

  def swapChildren(self):
    self.left, self.right=self.right, self.left

  def rightNodeMoveLeft(self):
    oldleft=self.left
    self.left=self.right
    self.right=self.right.right
    self.right.parent=self
    self.left.right=self.left.left
    self.left.left=oldleft
    self.left.left.parent=self.left

  def value(self):
    if (self.dummy):
      return self.right.value()
    else:
      left=self.left.value()
      right=self.right.value()
      return evalOperator(self.name,left,right)

class Leaf:
  def __init__(self, num, parent):
    self.name=num
    self.parent=parent
    self.neg=False
    self.inv=False
  
  def printme(self):
    print('Leaf name: ',self.name,', parent ' , self.parent.name)

  def value(self):
    a=float(1)
    b=float(1)
    if self.neg:
      a=float(-1)
    if self.inv:
      b=float(-1)
    return a*(float(self.name)**b)

  def setInv(self):
    self.inv=not self.inv
  def isInv(self):
    return self.inv
  def setNeg(self):
    self.neg=not self.neg
  def isNeg(self):
    return self.neg

class BTree:
  def __init__(self, polishExp):
    self.nodes = []
    self.leaves = []
    self.nodes.append(Node(polishExp[-1]))
    nodeId=0
    for i in reversed(polishExp[:-1]):
      currNode=self.nodes[nodeId]
      if isOperator(i):
        newNode = Node(i,currNode)
        self.nodes.append(newNode)
        currNode.addLeaf(newNode)
        nodeId=len(self.nodes)-1
      else:
        newLeaf = Leaf(i,currNode)
        self.leaves.append(newLeaf)
        currNode.addLeaf(newLeaf)
        while (currNode.isFull() and nodeId>0):
          nodeId-=1
          currNode=self.nodes[nodeId]

  def printme(self):
    for n in self.nodes:
      n.printme()
    for l in self.leaves:
      l.printme()

  #This method relies on the leaves list sorted in the revers polish order
  #Since leaves list order is now obsolete, this method is deprecated
  def genPolish_deprecate(self):
    polish = self.nodes+self.leaves
    polish.reverse()
    lindex=len(self.leaves)-1
    nindex=len(self.nodes)+len(self.leaves)-1
    for i in range(len(self.nodes)):
      toindex=nindex
      if (nindex == lindex+1):
        break
      if (polish[nindex].right == polish[lindex]):
        toindex=nindex-1
        polish.insert(toindex, polish.pop(lindex))
        lindex-=1
        if (polish[nindex].left == polish[lindex]):
          toindex=nindex-2
          polish.insert(toindex, polish.pop(lindex))
          lindex-=1
      nindex=toindex-1
    exp = []
    for p in polish:
      exp.append(p.name)
    return exp 

  def genPolish(self):
    polish = []
    stack = []
    stack.append(self.nodes[0])
    while(stack):
      n=stack.pop()
      polish.insert(0,n.name)
      if isinstance(n, Node):
        stack.append(n.left)
        stack.append(n.right)
    return polish

  def regulate(self):
    #remove neg and inv nodes
    moved=True
    while (moved):
      for n in self.nodes:
        moved=True
        if n.name == n.right.name == '/':
          n.name='*'
          n.right.swapChildren()
        elif n.name==n.right.name=='-':
          n.name='+'
          n.right.swapChildren()
        elif n.name=='/' and isinstance(n.right, Leaf):
          n.name='*'
          n.right.setInv()
        elif n.name=='-' and isinstance(n.right, Leaf):
          n.name='+'
          n.right.setNeg()
        else:
          moved=False
        if moved:
          break

    assert(is24(self.nodes[0].value()))
    
    #Form a left unbalanced tree
    moved=True
    while (moved):
      for n in self.nodes:
        moved=True
        if n.name==n.right.name=='*' or n.name==n.right.name=='+':
          n.rightNodeMoveLeft()
        else:
          moved=False
        if moved:
          break

    assert(is24(self.nodes[0].value()))

    #Add dummy nodes to replace left children
    for n in self.nodes:
      if n.name=='*' and isinstance(n.left, Leaf):
        dummy=Node('*',n,dummy=True)
        dummy.left=1
        dummy.right=n.left
        dummy.right.parent=dummy
        n.left=dummy
        self.nodes.append(dummy)
      elif n.name=='+' and isinstance(n.left, Leaf):
        dummy=Node('+',n,dummy=True)
        dummy.left=0
        dummy.right=n.left
        dummy.right.parent=dummy
        n.left=dummy
        self.nodes.append(dummy)

    assert(is24(self.nodes[0].value()))

    #sort right children on inversible nodes
    moved=True
    while(moved):
      moved=False
      for n in self.nodes:
        if isinstance(n.left, Node) and (n.name==n.left.name=='+' or
            n.name==n.left.name=='*'):
          if (n.right.value() > n.left.right.value()):
            n.right, n.left.right = n.left.right, n.right
            n.right.parent = n
            n.left.right.parent = n.left
            moved=True
            break

    assert(is24(self.nodes[0].value()))

    #Remove dummy nodes
    for n in reversed(self.nodes):
      if n.dummy:
        n.parent.left=n.right
        n.right.parent=n.parent
        self.nodes.pop()

    assert(is24(self.nodes[0].value()))

    #Revert neg & inv leaves
    for l in self.leaves:
      if l.isNeg():
        assert(l.parent.name=='+')
        l.parent.name='-'
        l.setNeg()
      if l.isInv():
        assert(l.parent.name=='*')
        l.parent.name='/'
        l.setInv()

    assert(is24(self.nodes[0].value()))

    for n in self.nodes:
      if n.isReverse():
        n.swapChildren()

    assert(is24(self.nodes[0].value()))

###Main program
known24s = []
nums=sorted(operands)
ops=operators
opSeqs = genOpSeq(ops)
numSeqs = genNumSeq(nums)
for opSeq in opSeqs:
  for numSeq in numSeqs:
    polishSeqs = genPolish(numSeq, opSeq)
    for polishExp in polishSeqs:
      if (is24(evalPolishExp(polishExp))):
        tree = BTree(polishExp)
        assert (tree.genPolish()==polishExp)
        tree.regulate()
        polishExp = tree.genPolish()
        assert(is24(evalPolishExp(polishExp)))
        if (polishExp not in known24s):
          known24s.append(polishExp)
          print(len(known24s),polishExp,genSolvStr(polishExp))
          printPolish(polishExp)
if not known24s:
  print("No solution found")