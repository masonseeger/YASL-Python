'''
Created: 9/1/2018
By: Mason Seeger

YASL - Yet Another Simple Language

Interprets the tree from the parser and runs the code
'''
from NonTerminals import *
from Terminals import *

class Interpreter:
    def __init__(self, program):
        self.program = program
        self.vars = {}
        self.vals = {}
        self.functions = {}

    def valVarFunFinder(self):
        for var in self.program.block.vardecls.list:
            self.vars[var.id] = var.type

        for val in self.program.block.valdecls.list:
            self.vals[val.id] = val.num

        for fun in self.program.block.fundecls.list:
            self.functions[fun.id] = fun
