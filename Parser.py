'''
Created: 9/1/2018
By: Mason Seeger

This class does two things:
makes sure that correct grammar is used
prints expressions in postfix
'''
from Scanner import Scanner
from Token import Token
from Terminals import *
from NonTerminals import *

class Parser:
    def __init__(self, scanner):
        self.consts = {}
        self.stack = []
        self.state = 0
        self.id = ''
        self.states = ["program", "block", "valdecls", "valdecl", "sign", "stmts", \
                       "stmt", "expr", "term", "factor"]  # list of all states
        self.p0 = ['PRINT']
        self.p1 = ['PLUS', 'MINUS', '+', '-']
        self.p2 = ['STAR', 'DIV', 'MOD', '*']
        self.inputChars = ['STAR', 'PLUS', 'MINUS']
        self.accepts = ['PROGRAM']  # determines what states can follow
        self.currentState = "PROG"
        self.ok = 1
        self.inStmt = False
        self.scanner = scanner
        self.token = self.scanner.next()

    # beginning of the language, only accepts program or errors out
    # currently only uses the postfix() and StmtStart() methods
    # right now it will store const and vals in a dictionary
    # and print Stmts in postfix as described in class
    # checks for undeclared identifiers only
    def S(self):
        #print(self.match([self.token.type]))
        program = self.parseProgram()
        program.display(0)
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
    '''

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
    def match(self, accepts):
        if self.token.type in accepts:
            oldToken = self.token
            self.token = self.scanner.next()
            return(oldToken.lexeme)
        print("Error, Expected type(s):" , *(accepts),'->' , "Type found:" \
                , self.token.type)
        exit()
        return(False)

    def check(self, accepts):
        if self.token.type in accepts:
            return(True)
        return(False)

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
    def parseProgram(self):
        if self.check(['PROGRAM']):
            self.match(['PROGRAM'])
            name = self.match(['ID'])
            self.match(['SEMI'])
            #print('finding a block')
            #print("START PROGRAM BLOCK")
            sblock = self.parseBlock()
            #print('program block', sblock)
            return(Program(name, sblock))
    # accepts <ConstDecls> BEGIN <Stmts> END Sequence
    def parseBlock(self):
        #print('finding valdecls')
        vals = self.parseValDecls()
        #print('finding vardecls')
        vars = self.parseVarDecls()
        #print('START FUNDECLS')
        funs = self.parseFunDecls()
        stmt = self.parseStmt()
        return(Block(stmt, vals, vars, funs))
    # accepts <ConstDecl> <ConstDecls> Sequence
    def parseValDecls(self):
        #print('In parseValDecls')
        valdecls = ValDecls()
        while self.check(['VAL']):
            valdecls.add(self.parseValDecl())
        return(valdecls)
    # accepts CONST ID ASSIGN NUM SEMI Sequence

    def parseValDecl(self):
        #print('In parseValDecl')
        self.match(['VAL'])
        id = self.match(['ID'])
        self.match(['ASSIGN'])
        if self.check(['MINUS']):
            self.match(['MINUS'])
            num = -(int(self.match(['NUM'])))
        elif self.check(['NUM']):
            num = self.match(['NUM'])
        self.match(['SEMI'])
        return(ValDecl(id, num))

    def parseVarDecls(self):
        #print('In parseVarDecls')
        vardecls = VarDecls()
        while self.check(['VAR']):
            vardecls.add(self.parseVarDecl())
        return(vardecls)
    # accepts CONST ID ASSIGN NUM SEMI Sequence
    def parseVarDecl(self):
        #print('In parseVarDecl')
        self.match(['VAR'])
        id = self.match(['ID'])
        self.match(['COLON'])
        type = self.match(['INT', 'BOOL', 'VOID'])
        self.match(['SEMI'])
        return(VarDecl(id, type))

    def parseFunDecls(self):
        #print('In parseFunDecls')
        fundecls = FunDecls()
        #print(fundecls)
        while self.check(['FUN']):
            fundecls.add(self.parseFunDecl())
        return(fundecls)

    def parseFunDecl(self):
        #print('In parseFunDecl')
        self.match(['FUN'])
        id = self.match(['ID'])
        self.match(['LPAREN'])
        paramlist = self.parseParamList()
        self.match(['RPAREN'])
        self.match(['COLON'])
        type = self.match(['INT', 'BOOL', 'VOID'])
        self.match(['SEMI'])
        fblock = self.parseBlock()
        #print('function block', id, fblock)
        #print("  ", fblock.fundecls)
        self.match(['SEMI'])
        return(FunDecl(id, type, fblock, paramlist))

    def parseParamList(self):
        #print('In parseParamList')
        paramlist = ParamList()
        while self.check(['ID']):
            paramlist.add(self.parseParam())
            if self.check(['COMMA']):
                self.match(['COMMA'])
        return(paramlist)

    def parseParam(self):
        #print('In parseParam')
        id = self.match(['ID'])
        self.match(['COLON'])
        type = self.match(['INT', 'BOOL', 'VOID'])
        return(Param(id, type))

    def parseStmtList(self):
        #print('In parseStmtList')
        stmtlist = StmtList()
        accepts = ['LET', 'BEGIN', 'IF', 'WHILE', 'INPUT', 'PRINT', 'STRING',\
                   'NUM', 'ID', 'TRUE', 'FALSE', 'MINUS', 'NOT', 'LPAREN']
        while self.check(accepts):
            stmtlist.add(self.parseStmt())

            if self.check(['SEMI']):
                self.match(['SEMI'])
        return(stmtlist)

    def parseStmt(self):
        #print('In parseStmt')
        accepts = ['LET', 'BEGIN', 'IF', 'WHILE', 'INPUT', 'PRINT', 'STRING',\
                   'NUM', 'ID', 'TRUE', 'FALSE', 'MINUS', 'NOT', 'LPAREN']
        if self.check(accepts):
            if self.check(['LET']):
                self.match(['LET'])
                id = self.match(['ID'])
                self.match(['ASSIGN'])
                expr = self.parseExpr()
                return(Assign(id, expr))
            elif self.check(['BEGIN']):
                self.match(['BEGIN'])
                stmtlist = self.parseStmtList()
                self.match(['END'])
                return(Sequence(stmtlist))
            elif self.check(['IF']):
                self.match(['IF'])
                test = self.parseExpr()
                self.match(['THEN'])
                stmt1 = self.parseStmt()
                if self.check(['ELSE']):
                    self.match(['ELSE'])
                    stmt2 = self.parseStmt()
                    return(IfThenElse(test, stmt1, stmt2))
                else:
                    return(IfThen(test,stmt1))
            elif self.check(['WHILE']):
                self.match(['WHILE'])
                test = self.parseExpr()
                self.match(['DO'])
                stmt1 = self.parseStmt()
                return(While(test, stmt1))
            elif self.check(['INPUT']):
                self.match(['INPUT'])
                msg = self.match(['STRING'])
                if self.check(['COMMA']):
                    self.match(['COMMA'])
                    id = self.match(['ID'])
                    return(Input2(msg, id))
                else:
                    return(Input(msg))
            elif self.check(['PRINT']):
                self.match(['PRINT'])
                return(self.parseItems())
            else:
                expr = self.parseExpr()
                return(ExprStmt(expr))

        print("ERROR, looking for type"+accepts+', found ' + self.token.type)
        exit()

    def parseItems(self):
        #print('In parseItems')
        itemlist = ItemList()
        accepts = ['STRING','NUM', 'ID', 'TRUE', 'FALSE', 'MINUS', 'NOT', 'LPAREN']
        while self.check(accepts):
            itemlist.add(self.parseItem())
            if self.check(['COMMA']):
                self.match(['COMMA'])
            else:
                return(itemlist)

    def parseItem(self):
        #print('In parseItem')
        if self.check(['STRING']):
            msg = self.match(['STRING'])
            return(StringItem(msg))
        else:
            expr = self.parseExpr()
            return(ExprItem(expr))
    # accepts <Expr> PLUS <Term> or <Expr> MINUS <Term> or <Term>
    def parseExpr(self):
        #print('In parseExpr')
        left = self.parseSimpleExpr()
        relop = ['ASSIGN','EQUAL', 'NOTEQUAL', 'LESSEQUAL', 'GREATEREQUAL', \
        'LESS', 'GREATER']
        if self.check(relop):
            op = self.match(relop)
            right = self.parseSimpleExpr()
            return(Expr(left, Op(op), right))
        return(left)

    def parseSimpleExpr(self):
        #print('In parseSimpleExpr')
        left = self.parseTerm()
        addop = ['PLUS', 'MINUS', 'OR']
        if self.check(addop):
            op = self.match(addop)
            right = self.parseSimpleExpr()
            return(SimpleExpr(left, Op(op), right))
        return(left)
    # accepts <Term> STAR <Factor> or <Term> DIV <Factor> or <Term> MOD <Factor>
    # or <Factor>
    def parseTerm(self):
        #print('In parseTerm')
        left = self.parseFactor()
        if self.check(['STAR', 'DIV', 'MOD', 'AND']):
            op = self.match(['STAR', 'DIV', 'MOD', 'AND'])
            right = self.parseTerm()
            return(Term(left, Op(op), right))
        return(left)

    def parseFactor(self):
        #print('In parseFactor')
        accepts = ['NUM', 'ID', 'TRUE', 'FALSE', 'MINUS', 'NOT', 'LPAREN']
        if self.check(accepts):
            if self.check(['NUM']):
                num = self.match(['NUM'])
                return(Num(num))
            elif self.check(['ID']):
                id = self.match(['ID'])
                if self.check(['LPAREN']):
                    self.match(['LPAREN'])
                    arglist = self.parseArgList()
                    self.match(['RPAREN'])
                    return(Call(id,arglist))
                return(Id(id))
            elif self.check(['TRUE']):
                self.match(['TRUE'])
                return(TRUE())
            elif self.check(['FALSE']):
                self.match(['FALSE'])
                return(FALSE())
            elif self.check(['MINUS', 'NOT']):
                op = self.match(['MINUS', 'NOT'])
                factor = self.parseFactor()
                return(UnOp(op, factor))
            elif self.check(['LPAREN']):
                self.match(['LPAREN'])
                expr = self.parseExpr()
                self.match(['RPAREN'])
                return(expr)

    def parseArgList(self):
        #print('In parseArgList')
        arglist = ArgList()
        accepts = ['NUM', 'ID', 'TRUE', 'FALSE', 'MINUS', 'NOT', 'LPAREN']
        while self.check(accepts):
            arglist.add(self.parseExpr())
            if self.check(['COMMA']):
                self.match(['COMMA'])
        return(arglist)
