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

    #beginning of the language, only accepts program or errors out
    #currently being used to test if the consts will store: they do
    def S(self, token):
        if self.state == 1:
            if token.type == 'NUM':
                self.consts[self.id] = token.lexeme
            self.id = ''
            self.state = 0

        if token.type == 'ID':
            self.state = 1
            self.id = token.lexeme

    # accepts PROGRAM ID SEMI <BLOCK> PERIOD Sequence
    def prog(self):
        return(1)

    # accepts <ConstDecls> BEGIN <Stmts> END Sequence
    def block(self):
        return(1)

    # accepts <ConstDecls> <ConstDecls> Sequence
    def ConstDecls(self):
        return(1)

    # accepts CONST ID ASSIGN NUM SEMI Sequence
    def ConstDecl(self):
        return(1)

    # accepts <Stmt> SEMI <Stmt> or <Stmt> Sequences
    def Stmts(self):
        return(1)

    # accepts PRINT <Expr> Sequence
    # This and its FOLLOW will be printed in postfix
    def Stmt(self):
        return(1)

    # accepts <Expr> PLUS <Term> or <Expr> MINUS <Term> or <Term>
    def Expr(self):
        return(1)

    # accepts <Term> STAR <Factor> or <Term> DIV <Factor> or <Term> MOD <Factor>
    # or <Factor>
    def Term(self):
        return(1)

    #accepts NUM or ID
    def Factor(self):
        return(1)
