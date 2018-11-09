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
        self.symbolTable = {}

    def setVal(self, id, val):
        if type(st[id]) == type(val[0]):
            st[id] = val
        elif st[id] == val[1]:
            st[id] == val[0]

    def interpProgram(self):
        print('in interpProgram')
        st = self.symbolTable
        st[self.program.name] = self.program.block
        self.interpBlock(st, self.program.block)

    def interpBlock(self, st, block):
        print('In interpBlock')
        for var in block.vardecls.list:
            if var.id not in st:
                st[var.id] = var.type

        for val in block.valdecls.list:
            if val.id not in st:
                st[val.id] = int(val.num)

        for fun in block.fundecls.list:
            if fun.id not in st:
                st[fun.id] = fun

        self.interpStmt(st, block.stmt)

    def interpStmt(self, st, stmt):
        print('In interpStmt')
        print(type(stmt))
        if type(stmt) == type(Assign(0,0)):
            print("Assign")
            x = self.interpExpr(st, stmt.expr)
            if type(st[stmt.id]) == type(x) or type(x) == type(int()) \
                                                    and st[stmt.id] == 'int':
                st[stmt.id] = x
            elif st[stmt.id] == x[1]:
                st[stmt.id] == x[0]

        elif type(stmt) == type(Sequence(0)):
            print("Sequence")
            for s in stmt.stmtList.list:
                self.interpStmt(st, s)
        elif type(stmt) == type(IfThen(0, 0)):
            print("IfThen")
            test = self.interpExpr(st, stmt.test)
            if test:
                self.interpStmt(st, stmt.s1)
        elif type(stmt) == type(IfThenElse(0,0,0)):
            print("IfThenElse")
            test = self.interpExpr(st, stmt.test)
            if test:
                self.interpStmt(st, stmt.s1)
            else:
                self.interpStmt(st, stmt.s2)
        elif type(stmt) == type(While(0, 0)):
            print("While")
            test = self.interpExpr(st, stmt.test)
            while(test):
                self.interpStmt(st, stmt.s1)
                test = self.interpExpr(st, stmt.test)
        elif type(stmt) == type(Input(0)):
            print("Input")
            print(stmt.lexeme)
            input()
        elif type(stmt) == type(Input2(0, 0)):
            print("Input2")
            print(stmt.lexeme + " ")
            x = input()
            try:
                x = int(x)
            except:
                print("Integer input required")
                exit()
            if type(st[stmt.id]) == type(int()) or st[stmt.id] == 'int':
                st[stmt.id] = x
            else:
                print("Error, attempted to assign int to a non-Int val")
                exit()
        elif type(stmt) == type(ItemList()):
            print("Print")
            for item in stmt.list:
                if type(item) == type(StringItem(0)):
                    print(item.lexeme)
                else:
                    value = self.interpExpr(st, item.expr)
                    print(value)
        elif type(stmt) == type(ExprStmt(0)):
            print("ExprStmt")
            self.interpExpr(st, stmt)
        elif type(stmt) == type(Call(0,0)):
            return self.interpFunction(st, stmt)
        else:
            print('Error, no correct type found')


    def interpFunction(self, st, stmt):
        print('In interpFucntion')
        ars = {}
        for e in stmt.arglist:
            ars[e.id] = e.type

        nst = {}
        nst.update(ars)
        nst.update(st)
        result = self.interpCall(stmt.arglist, stmt.block, nst, stmt.type)

        all(map(nst.pop, ars))
        st.update(nst)
        return result

    def interpCall(self, params, block, nst, type):
        print("In interpCall")
        return self.interpBlock(nst, block)

    def interpExpr(self, st, expr):
        print('In interpExpr')
        print(type(expr))
        if type(expr) == type(Id(0)):
            return st[expr.lexeme]
        elif type(expr) == type(Num(0)):
            return int(expr.lexeme)
        elif type(expr) == type(FALSE()):
            return False
        elif type(expr) == type(TRUE()):
            return True

        if type(expr.left) == type(UnOp(0,0)):
            lhs = self.interpUnOp(st, expr.left)
        else:
            lhs = self.interpSide(st, expr.left)

        print("pre lhs" , lhs)

        if expr.op.lexeme == "AND":
            if lhs:
                return self.interpSide(st, expr.right)
            else:
                return lhs
        elif expr.op.lexeme == "OR":
            if lhs:
                return lhs
            else:
                return self.interpSide(st, expr.right)
        elif expr.op.lexeme in ['EQUAL', 'NOTEQUAL', 'LESSEQUAL', 'GREATEREQUAL', \
                        'LESS', 'GREATER']:
            rhs = self.interpSide(st, expr.right)
            return self.interpRelOp(st, lhs, expr.op, rhs)
        elif expr.op.lexeme in ['-', '+', 'DIV', '*', 'MOD']:
            rhs = self.interpSide(st, expr.right)
            print("left hand side" , lhs)
            print("right hand side" , rhs)
            return self.interpMathOp(st, lhs, expr.op, rhs)
        else:
            print(expr.op.lexeme)
            print("broken in interpExpr")

    def interpSide(self, st,  expr):
        print('In interpSide')
        print(type(expr))
        #fix this to enter in vars from st
        if type(expr)==type(bool()) or type(expr)==type(int()):
            return expr
        elif type(expr)==type(Id(0)):
            return st[expr.lexeme]
        else:
            return self.interpExpr(st, expr)

    def interpRelOp(self, st, lhs, op, rhs):
        print('In interpRelop')
        #add code for vals in st
        if op.lexeme == "EQUAL":
            return lhs == rhs
        elif op.lexeme == "NOTEQUAL":
            return lhs != rhs
        elif op.lexeme == "LESSEQUAL":
            return lhs<=rhs
        elif op.lexeme == "LESS":
            return lhs<rhs
        elif op.lexeme == "GREATEREQUAL":
            return lhs>=rhs
        elif op.lexeme == "GREATER":
            return lhs>rhs

    def interpMathOp(self, st, lhs, op, rhs):
        print('In interpMathop')
        #add code for st
        if op.lexeme == "+":
            return lhs + rhs
        elif op.lexeme == "-":
            return lhs - rhs
        elif op.lexeme == "*":
            return lhs*rhs
        elif op.lexeme == "DIV":
            return lhs/rhs
        elif op.lexeme == "MOD":
            return lhs%rhs

    def interpUnOp(self, st, expr):
        print('In interpUnop')
        value = self.interpExpr(st, expr.factor)
        if expr.unop == 'NOT':
            return not(value)
        elif expr.unop == '-':
            return -value
