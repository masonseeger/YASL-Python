'''
Created: 9/1/2018
By: Mason Seeger

This class does two things:
makes sure that correct grammar is used
prints expressions in postfix
'''
from Scanner import Scanner
from Token import Token

class Parser:
    def __init__(self, scanner):
        self.consts = {}
        self.stack = []
        self.state = 0
        self.id = ''
        self.states = ["program", "block", "valdecls", "valdecl", "sign", "stmts", \
                       "stmt", "expr", "term", "factor"] #list of all states
        self.p0 = ['PRINT']
        self.p1 = ['PLUS', 'MINUS', '+', '-']
        self.p2 = ['STAR', 'DIV', 'MOD', '*']
        self.inputChars = ['STAR', 'PLUS', 'MINUS']
        self.accepts = ['PROGRAM'] #determines what states can follow
        self.currentState = "PROG"
        self.ok = 1
        self.inStmt = False
        self.scanner = scanner

    #beginning of the language, only accepts program or errors out
    #currently only uses the postfix() and StmtStart() methods
    #right now it will store const and vals in a dictionary
    #and print Stmts in postfix as described in class
    #checks for undeclared identifiers only
    def S(self, token):
        #self.match(token)
        '''if self.ok:
            self.findPos(token)
        else:
            print("Error found. Exiting...")
        '''
        if (self.inStmt):
            if (token.type == "SEMI"):
                self.inStmt = False
                while bool(self.stack):
                    print(self.stack.pop())
            elif token.type == "END":
                self.inStmt = False
                while bool(self.stack):
                    print(self.stack.pop())
            else:
                self.postfix(token)
        else:
            self.StmtStart(token)

        if self.state == 2:
            if token.type == 'NUM':
                self.consts[self.id] = token.lexeme
            self.id = ''
            self.state = 0

        if token.type == 'ASSIGN':
            #print("found assign")
            self.state = 2

        if token.type == 'ID':
            #print("found ID")
            self.state = 1
            self.id = token.lexeme

    # this function helps store and print terms in postfix for stmts
    def postfix(self, token):
        tt = token.type
        if tt == 'NUM':
            print(token.lexeme)
        elif tt == 'ID':
            if token.lexeme in self.consts:
                print(self.consts[token.lexeme])
            else:
                self.ok = 0
        elif tt in self.p1:
            while self.stack[-1] in self.p1 or self.stack[-1] in self.p2:
                print(self.stack.pop())
            self.fixPrint(token)
        elif tt in self.p2:
            if self.stack[-1] in self.p2:
                print(self.stack.pop())
            self.fixPrint(token)

    def fixPrint(self, token):
        tt = token.type
        if tt == 'PLUS':
            self.stack.append('+')
        elif tt == 'STAR':
            self.stack.append('*')
        elif tt == 'MINUS':
            self.stack.append('-')
        else:
            self.stack.append(tt)

    #checks to see if a stmt is starting
    def StmtStart(self, token):
        if (token.type == 'PRINT'):
            self.inStmt = True
            self.stack.append(token.type)

    # determins if the current token is accepted by the grammar
    def match(self, type):
        if not(self.token.type == type):
            print(token.type)
            print(self.accepts)
            self.ok = -1

    # used to store a const or val when declared
    def store(self, token):
        if self.state == 1:
            if token.type == 'NUM':
                self.consts[self.id] = token.lexeme
            self.id = ''
            self.state = 0

        if token.type == 'ID':
            self.state = 1
            self.id = token.lexeme

    # accepts PROGRAM ID SEMI <BLOCK> PERIOD Sequence
    def parseProgram(self, token):
        return(1)
    # accepts <ConstDecls> BEGIN <Stmts> END Sequence
    def parseBlock(self, token):
        return(1)
    # accepts <ConstDecl> <ConstDecls> Sequence
    def parseValDecls(self, token):
        return(1)
    # accepts CONST ID ASSIGN NUM SEMI Sequence
    def parseValDecl(self, token):
        return(1)
    def parseSign(self, token):
        return(1)
    def parseVarDecls(self, token):
        return(1)
    # accepts CONST ID ASSIGN NUM SEMI Sequence
    def parseVarDecl(self, token):
        return(1)

    def parseType(self, token):
        return(1)

    def parseFunDecls():
        return(1)

    def parseFunDecl():
        return(1)

    def parseParamList():
        return(1)

    def parseParams():
        return(1)

    def parseParam():
        return(1)

    def parseStmtList():
        return(1)

    def parseStmts(self, token):
        return(1)

    def parseStmt(self, token):
        return(1)

    def parseItems():
        return(1)
    def parseItem():
        return(1)
    # accepts <Expr> PLUS <Term> or <Expr> MINUS <Term> or <Term>
    def parseExpr(self, token):
        return(1)
    def parseRelOp():
        return(1)
    def parseSimpleExpr():
        return(1)
    def parseAddOp():
        return(1)
    # accepts <Term> STAR <Factor> or <Term> DIV <Factor> or <Term> MOD <Factor>
    # or <Factor>
    def Term(self, token):
        return(1)
    def parseMulOp():
        return(1)
    #accepts NUM or ID
    def Factor(self, token):
        '''if (check(num)):
                Oldtoken = match(Num)
                return(num(oldtoken.lexeme))
            elif(check(id)):
                ot = match(id)
                return(id(ot.lexeme))
            elif(check(LPar)):
                match(LPar)
                expr = parseExpr()
                match(RPar)
                return(expr)
                '''
    def parseUnOp():
        return(1)
    def parseArgList():
        return(1)
    def parseArgs():
        return(1)
