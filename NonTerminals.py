'''
Created: 10/16/2018
By: Mason Seeger

YASL - Yet Another Simple Language

As of now this program is a lexicon for a simple programming language.
Need to go back through this and change the prints to print in the ast tree
'''

from Terminals import *

class Program:
    def __init__(self, name, b):
        self.name = name
        self.block = b
    def display(self, indent):
        print(indent*' ' + 'Program ' + self.name)
        self.block.display(indent+1)
    def run():
        print('Running program...')

class Block:
    def __init__(self, s, vs, rs, fs):
        self.valdecls = vs
        self.vardecls = rs
        self.fundecls = fs
        self.stmt = s
    def display(self, indent):
        print(indent*' ' + "Block")
        self.valdecls.display(indent+1)
        self.vardecls.display(indent+1)
        self.fundecls.display(indent+1)
        self.stmt.display(indent+2)

class ValDecl:
    def __init__(self, id, n):
        self.id = id
        self.num = n
    def display(self, indent):
        print(indent*' ' + 'Val ' + self.id + ' = ' + str(self.num))

class VarDecl:
    def __init__(self, id, t):
        self.id = id
        self.type = t
    def display(self, indent):
        print(indent*' ' + 'Var ' + self.id + ' : ' + self.type)

class FunDecl:
    def __init__(self, id, t, b, ps):
        self.id = id
        self.type = t
        self.paramList = ps
        self.block = b
    def display(self, indent):
        print(indent*' ' + 'Fun ' + self.id + ' : '+ self.type)
        self.paramList.display(indent+1)
        self.block.display(indent+1)

class Param:
    def __init__(self, id, t):
        self.id = id
        self.type = t
    def display(self, indent):
        print(indent*' ' + 'Val ' + self.id + ' : ' + self.type)

class Assign:
    def __init__(self, id, expr):
        self.id = id
        self.expr = expr
    def display(self, indent):
        print(indent*' ' + 'Assign ' + self.id)
        self.expr.display(indent+1)
        #what??? look into this above and fix it somehow
class Sequence:
    def __init__(self, ss):
        self.stmtList = ss
    def display(self, indent):
        print(indent*' ' + 'Sequence')
        for i in self.stmtList.list:
            i.display(indent+1)

class IfThen:
    def __init__(self, expr, stmt):
        self.test = expr
        self.s1 = stmt
    def display(self, indent):
        print(indent*' ' + 'IfThen')
        self.test.display(indent+1)
        self.s1.display(indent+1)

class IfThenElse:
    def __init__(self, expr, stmt1, stmt2):
        self.test = expr
        self.s1 = stmt1
        self.s2 = stmt2
    def display(self, indent):
        print(indent*' ' + 'IfThenElse')
        self.test.display(indent+1)
        self.s1.display(indent+1)
        self.s2.display(indent+1)

class While:
    def __init__(self, expr, stmt):
        self.test = expr
        self.s1 = stmt
    def display(self, indent):
        print(indent*' ' + 'While')
        self.test.display(indent+1)
        self.s1.display(indent+1)

class Print:
    def __init__(self, items):
        self.its = items
    def display(self, indent):
        print(indent*' ' + 'Print')
        for itm in self.its.list:
            itm.display(indent + 1)

class ExprStmt:
    def __init__(self, expr):
        self.expr = expr
    def display(self, indent):
        print(indent*' ' + 'ExprStmt')
        self.expr.display(indent+1)

class ExprItem:
    def __init__(self, expr):
        self.expr = expr
    def display(self, indent):
        print(indent*' ' + 'ExprItem')
        self.expr.display(indent+1)

class Expr:
    def __init__(self, simpleExL, relop = None, simpleExR = None):
        self.left = simpleExL
        self.op = relop
        self.right = simpleExR
    def display(self, indent):
        if self.op == None:
            self.left.display(indent)
        else:
            self.op.display(indent)
            self.left.display(indent+1)
            self.right.display(indent+1)

class SimpleExpr:
    def __init__(self, term, relop = None, simpleExR = None):
        self.term = term
        self.op = relop
        self.right = simpleExR
    def display(self, indent):
        if self.op == None:
            self.term.display(indent)
        else:
            self.op.display(indent)
            self.term.display(indent+1)
            self.right.display(indent+1)

class Term:
    def __init__(self, factor, relop = None, term = None):
        self.factor = factor
        self.op = relop
        self.term = term
    def display(self, indent):
        if self.op == None:
            self.factor.display(indent)
        else:
            self.op.display(indent)
            self.factor.display(indent+1)
            self.term.display(indent+1)

class UnOp:
    def __init__(self, unop, factor):
        self.unop = unop
        self.factor = factor
    def display(self, indent):
        print(indent*' ' + 'UnOp ' + self.unop)
        self.factor.display(indent + 1)

class Call:
    def __init__(self, id, arglist):
        self.id = id
        self.args = arglist
    def display(self, indent):
        print(indent*' ' + "Call " + self.id)
        self.args.display(indent+1)

class StmtList:
    def __init__(self):
        self.list = []

    def add(self, stmt):
        self.list.append(stmt)

    def display(self, indent):
        for stmt in self.list:
            stmt.display(indent + 1)

class ItemList:
    def __init__(self):
        self.list = []

    def add(self, item):
        self.list.append(item)

    def display(self, indent):
        print(indent*' ' + 'Print')
        for item in self.list:
            item.display(indent + 1)

class ArgList:
    def __init__(self):
        self.list = []

    def add(self, arg):
        self.list.append(arg)

    def display(self, indent):
        for arg in self.list:
            arg.display(indent + 1)

class ParamList:
    def __init__(self):
        self.list = []

    def add(self, param):
        self.list.append(param)

    def display(self, indent):
        for param in self.list:
            param.display(indent + 1)

class VarDecls:
    def __init__(self):
        self.list = []

    def add(self, vardecl):
        self.list.append(vardecl)

    def display(self, indent):
        for var in self.list:
            var.display(indent + 1)

class ValDecls:
    def __init__(self):
        self.list = []

    def add(self, valdecl):
        self.list.append(valdecl)

    def display(self, indent):
        for val in self.list:
            val.display(indent + 1)

class FunDecls:
    def __init__(self):
        self.list = []

    def add(self, fundecl):
        self.list.append(fundecl)

    def display(self, indent):
        for fun in self.list:
            fun.display(indent + 1)
