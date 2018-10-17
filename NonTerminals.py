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
        print(indent + 'Program ' + self.name)
        self.block.display(indent+1)

class Block:
    def __init__(self, vs, rs, fs, s):
        self.valdecls = vs
        self.vardecls = rs
        self.fundecls = fs
        self.stmt = s
    def display(self, indent):
        print(indent + "block")
        self.valdecls.display(indent+1)
        self.vardecls.display(indent+1)
        self.fundecls.display(indent+1)
        self.stmt.display(indent+1)

class ValDecl:
    def __init__(self, id, n):
        self.id = id
        self.num = n
    def display(self, indent):
        print(indent + 'Val ' + self.id + ' = ' + self.num)

class VarDecl:
    def __init__(self, id, t):
        self.id = id
        self.type = t
    def display(self, indent):
        print(indent + 'Var ' + self.id + ' : ' + self.type)

class FunDecl:
    def __init__(self, id, t, ps, b):
        self.id = id
        self.type = t
        self.paramList = ps
        self.block = b
    def display(self, indent):
        print(indent + 'Fun ' + self.id + ' : '+ self.type)
        if self.paramList:
            for i in self.paramList:
                i.display(indent+1)
        self.block.display(indent+1)

class Param:
    def __init__(self, id, t):
        self.id = id
        self.type = t
    def display(self, indent):
        print(indent + 'Val ' + self.id + ' : ' + self.type)

class Assign:
    def __init__(self, id, expr):
        self.id = id
        self.expr = expr
    def display(self, indent):
        print(indent + 'let ' + self.id + ' = ' + self.expr.binop.toString)
        #what??? look into this above and fix it somehow
class Sequence:
    def __init__(self, ss):
        self.stmtList = ss
    def display(self, indent):
        print(indent + 'Sequence')
        for i in self.stmtList:
            i.display(indent+1)

class IfThen:
    def __init__(self, expr, stmt):
        self.test = expr
        self.s1 = stmt
    def display(self, indent):
        print(indent + 'if ' + self.test.binop.toString + ' then')
        self.s1.display(indent+1)

class IfThenElse:
    def __init__(self, expr, stmt1, stmt2):
        self.test = expr
        self.s1 = stmt1
        self.s2 = stmt2
    def display(self, indent):
        print(indent + 'if ' + self.test.binop.toString + ' then')
        self.s1.display(indent+1)

class While:
    def __init__(self, expr, stmt):
        self.test = expr
        self.s1 = stmt
    def display(self, indent):

class Print:
    def __init__(self, items):
        self.its = items
    def display(self, indent):

class ExprStmt:
    def __init__(self, expr):
        self.expr = expr
    def display(self, indent):

class ExprItem:
    def __init__(self, expr):
        self.expr = expr
    def display(self, indent):

class BinOp:
    def __init__(self, simpleExL, relop, simpleExR):
        self.left = simpleExL
        self.op = relop
        self.right = simpleExR
    def display(self, indent):

class UnOp:
    def __init__(self, unop, expr):
        self.unop = unop
        self.expr = expr
    def display(self, indent):

class Call:
    def __init__(self, id, arglist):
        self.id = id
        self.args = argList
    def display(self, indent):

class StmtList:
    def __init__(self, list = []):
        self.list = list

    def add(self, stmt):
        self.list.append(stmt)

    def display(self, indent):

class ArgList:
    def __init__(self, list = []):
        self.list = list

    def add(self, arg):
        self.list.append(arg)

    def display(self, indent):

class ParamList:
    def __init__(self, list = []):
        self.list = list

    def add(self, param):
        self.list.append(param)

    def display(self, indent):

class VarDecls:
    def __init__(self, list = []):
        self.list = list

    def add(self, vardecl):
        self.list.append(vardecl)

    def display(self, indent):

class ValDecls:
    def __init__(self, list = []):
        self.list = list

    def add(self, valdecl):
        self.list.append(valdecl)

    def display(self, indent):

class FunDecls:
    def __init__(self, list = []):
        self.list = list

    def add(self, fundecl):
        self.list.append(fundecl)

    def display(self, indent):

class Expr:
    def __init__(self, binop):
        self.binop = binop
