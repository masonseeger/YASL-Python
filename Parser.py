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
    def __init__(self):
        self.consts = {}
        self.stack = []
        self.state = 0
        self.id = ''
        self.states = ["prog", "block", "constdecls", "constdecl", "stmts", \
                       "stmt", "expr", "term", "factor"] #list of all states
        self.p0 = ['PRINT']
        self.p1 = ['PLUS', 'MINUS']
        self.p2 = ['STAR', 'DIV', 'MOD']
        self.accepts = ['PROGRAM'] #determines what states can follow
        self.currentState = "PROG"
        self.ok = 1
        self.inStmt = False

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
            self.stack.append(tt)
        elif tt in self.p2:
            if self.stack[-1] in self.p2:
                print(self.stack.pop())
            self.stack.append(tt)


    #checks to see if a stmt is starting
    def StmtStart(self, token):
        if (token.type == 'PRINT'):
            self.inStmt = True
            self.stack.append(token.type)

    #uses the parsers state to move into what current position its at
    def findPos(self, token):
        cs = self.currentState
        if (cs == 'PROG'):
            self.Prog(token)
        elif(cs == "BLOCK"):
            self.Block(token)
        elif(cs == "CONSTDECLS"):
            self.ConstDecls(token)
        elif(cs == "CONSTDECL"):
            self.ConstDecl(token)
        elif(cs == "STMTS"):
            self.Stmts(token)
        elif(cs == "STMT"):
            self.Stmt(token)
        elif(cs == "EXPR"):
            self.Expr(token)
        elif(cs == "TERM"):
            self.Term(token)
        elif(cs == "FACTOR"):
            self.Factor(token)

    # determins if the current token is accepted by the grammar
    def match(self, token):
        if not(token.type in self.accepts):
            print(token.type)
            print(self.accepts)
            self.ok = 0

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
    def Prog(self, token):
        if token.type == 'PROGRAM':
            self.accepts = ['ID']
        elif token.type == 'ID':
            self.accepts = ['SEMI']
        elif token.type == ['SEMI']:
            print('found semi in prog')
            self.currentState = 'BLOCK'
            self.accepts = ['CONST', 'BEGIN']
        elif token.type == 'PERIOD':
            self.ok = 2
            print("end of program.")

    # accepts <ConstDecls> BEGIN <Stmts> END Sequence
    def Block(self, token):
        tt = token.type
        if tt == 'CONST':
            self.accepts = 'ID'
            self.currentState = 'CONSTDECL'
        elif tt == 'BEGIN':
            self.accepts = ['PRINT']
        elif tt == 'END':
            self.currentState = 'PROG'
            self.accepts = ['PERIOD']

    # accepts <ConstDecl> <ConstDecls> Sequence
    def ConstDecls(self, token):
        tt = token.type
        if tt == 'CONST':
            self.accepts = ['ID']
        elif tt == 'BEGIN':
            self.accepts = ['PRINT']
            self.currentState = 'STMT'

    # accepts CONST ID ASSIGN NUM SEMI Sequence
    def ConstDecl(self, token):
        tt = token.type
        if tt == 'CONST':
            self.accepts = ['ID']
        elif tt == 'ID':
            self.accepts = ['ASSIGN']
        elif tt == 'ASSIGN':
            self.accepts = ['NUM']
        elif tt == 'SEMI':
            self.accepts = ['CONST', 'BEGIN']
            self.currentState = 'CONSTDECLS'

    # accepts <Stmt> SEMI <Stmt> or <Stmt> Sequences
    def Stmts(self, token):
        tt = token.type
        if tt == 'PRINT':
            self.accepts = ['NUM', 'ID']
            self.currentState = 'STMT'
        elif tt == 'END':
            self.accepts = ['PERIOD']
            self.currentState = 'PROG'

    # accepts PRINT <Expr> Sequence
    # This and its FOLLOW will be printed in postfix
    def Stmt(self, token):
        tt = token.type
        if tt == 'NUM' or tt == 'ID':
            self.accepts = ['PLUS', 'MINUS', 'STAR', 'DIV', 'MOD', 'SEMI']
        elif tt in ['PLUS', 'MINUS', 'STAR', 'DIV', 'MOD']:
            self.accepts == ['ID', 'NUM']
        elif tt == 'SEMI':
            self.accepts = ['PRINT', 'END']
            self.currentState = 'STMTS'

    # accepts <Expr> PLUS <Term> or <Expr> MINUS <Term> or <Term>
    def Expr(self, token):
        tt = token.type
        return(1)

    # accepts <Term> STAR <Factor> or <Term> DIV <Factor> or <Term> MOD <Factor>
    # or <Factor>
    def Term(self, token):
        tt = token.type
        return(1)

    #accepts NUM or ID
    def Factor(self, token):
        tt = token.type
        return(1)
