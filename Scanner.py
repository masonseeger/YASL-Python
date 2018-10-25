'''
Created: 9/1/2018
By: Mason Seeger

Scanner class takes in line(s) of strings and returns tokens until the string is
"empty" (has a ~ at the end) or a EOF token is found.
'''
from Token import Token

class Scanner:
    def __init__(self, user_input, line=1, state=0):
        self.user_input = user_input
        self.state = state
        self.identifier = -1
        self.position = [line,1,1] #line, start pos of current lexem, current pos
        self.current_char = ord(self.user_input[0])
        self.lexeme = ''
        self.keywords = ['program', 'val', 'begin', 'print', 'end', 'div', 'mod',\
                        'const', 'var', 'int', 'bool', 'void', 'fun', 'let', 'if',\
                        'then', 'else', 'while', 'do', 'input', 'and', 'or',\
                        'not', 'true', 'false']
        self.id = ['NUM', 'ID', 'SEMI', 'PERIOD','STAR','PLUS','MINUS',\
                  'COLON', 'LPAREN', 'RPAREN', 'COMMA', 'ERROR']
        self.punctChar = [59, 44, 40, 41, 58, 46]
        self.ops = ['ASSIGN','EQUAL', 'NOTEQUAL', 'LESSEQUAL', 'GREATEREQUAL', \
        'LESS', 'GREATER']

    def getNextLine(self):
        self.position = [self.position[0]+1,1,1]
        #print(self.position)
        user_input = input()
        self.user_input = user_input +'~'
        self.current_char = ord(self.user_input[0])

    #Returns the next token in the sequence and handles the input for new lines
    def next(self):
        next_token = self.S()
        self.position[1]+=len(self.lexeme)
        self.lexeme = ''
        self.identifier=-1
        if self.state == -2: #comment of type //
            if next_token == -1: #end of line found
                self.state = 0
                self.getNextLine()
                return(self.next())
            else:
                return(self.next())
        elif self.state==-3: #comment of type /**/
            if next_token == -1: #end of line found
                self.state = -3
                self.getNextLine()
                return(self.next())
            elif self.state == -10: #ctrl+Z found (EOF)
                return(-10)
            else: #comment state in the middle of a line
                self.state = -3
                #print("in comment state")
                return(self.next())
        elif next_token ==-1: #EOL found
            self.getNextLine()
            return(self.next())
        elif self.state == -10: #ctrl+Z found (EOF)
            return(-10)
        else: #token found outside of comments, needs to be returned
            #print(next_token.information())
            return(next_token)

    #return type, lexeme, position

    def update_info(self, space=False):
        if self.user_input != '~': #if not EOL
            if not(space):
                self.lexeme+=self.user_input[0]
            else:
                self.position[1]+=1

            self.user_input = self.user_input[1:]
            self.current_char = ord(self.user_input[0])
            self.position[2]+=1
        else:
            self.current_char = 126

    #start of every new scan
    def S(self):
        if self.current_char == 26: #EOF (ctrl+Z)
            if self.state==-3: #in comment state
                print("error, no */ found before EOF")
                print(Token('EOF', ' ', self.position[0:2]).information())
                self.state = -10
                return(Token('EOF', self.lexeme, self.position[0:2]).information())
            else:
                self.update_info()
                self.state = -10
                print(Token('EOF', ' ', self.position[0:2]).information())
                return(Token('EOF', self.lexeme, self.position[0:2]).information())
        elif self.state == -3: #in comment state
            if self.current_char == 42: # *
                self.update_info()
                return(self.sEndComment())
            elif self.current_char == 126: # ~
                return (-1)
            else:
                self.update_info()
                return(self.S())
        elif 90>=self.current_char>=65 or 97<=self.current_char<=122: # A-Z, a-z
            self.update_info()
            self.identifier = 1
            return(self.sID())
        elif self.current_char == 32: # space
            self.update_info(True)
            return(self.S())
        elif self.current_char ==48: # 0
            self.update_info()
            self.identifier = 0
            self.position[1]+=len(self.lexeme)
            return(Token(self.id[self.identifier], '0', self.position[0:2],
                         defined = False))
        elif 49<=self.current_char<=57: #1-9
            self.update_info()
            self.identifier = 0
            return(self.sNum())
        elif self.current_char in self.punctChar: # ;, ., :, (, ), or ,
            return(self.sPunctuation())
        elif 42<=self.current_char<=43 or self.current_char == 45: # operators
            return(self.sComputationalOpp())
        elif self.current_char == 47: #/
            self.update_info()
            return(self.sComment())
        elif self.current_char == 60 or self.current_char == 61 or\
                self.current_char == 62: #/<, =, >
            return(self.s_operators())
        elif self.current_char == 44:#,
            self.update_info()
            self.identifier = 10
            return(Token(self.id[self.identifier], self.lexeme, self.position[0:2]))
        elif self.current_char == 40:#(
            self.update_info()
            self.identifier = 8
            return(Token(self.id[self.identifier], self.lexeme, self.position[0:2]))
        elif self.current_char == 41:#)
            self.update_info()
            self.identifier = 9
            return(Token(self.id[self.identifier], self.lexeme, self.position[0:2]))
        elif self.current_char == 58:#:
            self.update_info()
            self.identifier = 7
            return(Token(self.id[self.identifier], self.lexeme, self.position[0:2]))
        elif self.current_char == 34:#"
            self.update_info()
            return(self.sString())
        elif self.current_char == 126: # ~
            return (-1)
        else: # error state
            self.update_info(True)
            return(self.sError())

    #method for numbers
    def sNum(self):
        if 48<=self.current_char<=57:
            self.update_info()
            return(self.sNum())
        else:
            #self.update_info()
            return(Token(self.id[self.identifier],self.lexeme, self.position[0:2],
                         defined = False))

    #method for IDs
    def sID(self):
        if 48<=self.current_char<=57 or 90>=self.current_char>=65\
            or 97<=self.current_char<=122:
            self.update_info()
            return(self.sID())
        else: # keyword
            if self.lexeme in self.keywords:
                return(Token(self.lexeme, self.lexeme, self.position[0:2]))
            return(Token('ID', self.lexeme, self.position[0:2], defined = False))

    #method for punctuation
    def sPunctuation(self):
        if self.current_char == 59:
            self.update_info()
            self.identifier = 2
            return(Token(self.id[self.identifier], self.lexeme, self.position[0:2]))
        elif self.current_char == 44:#,
            self.update_info()
            self.identifier = 10
            return(Token(self.id[self.identifier], self.lexeme, self.position[0:2]))
        elif self.current_char == 40:#(
            self.update_info()
            self.identifier = 8
            return(Token(self.id[self.identifier], self.lexeme, self.position[0:2]))
        elif self.current_char == 41:#)
            self.update_info()
            self.identifier = 9
            return(Token(self.id[self.identifier], self.lexeme, self.position[0:2]))
        elif self.current_char == 58:#:
            self.update_info()
            self.identifier = 7
            return(Token(self.id[self.identifier], self.lexeme, self.position[0:2]))
        else:
            self.update_info()
            self.identifier = 3
            return(Token(self.id[self.identifier], self.lexeme, self.position[0:2]))

    #method for computational operators
    def sComputationalOpp(self):
        if self.current_char == 42:
            self.update_info()
            self.identifier = 4
            return(Token(self.id[self.identifier], self.lexeme, self.position[0:2]))
        elif self.current_char == 43:
            self.update_info()
            self.identifier = 5
            return(Token(self.id[self.identifier], self.lexeme, self.position[0:2]))
        else:
            self.update_info()
            self.identifier = 6
            return(Token(self.id[self.identifier], self.lexeme, self.position[0:2]))

    #method for comments and beginning block comments
    def sComment(self):
        if self.current_char == 47: #/
            self.state = -2
            self.update_info()
        elif self.current_char == 42: #*
            self.state = -3
            self.update_info()
            #print("starting new comment")
            return(self.S())
        else:
            self.state = 0
            return(self.sError())
        #until you see the ending or a NL char, keep going
        #comments will end tokens
        return(-2)

    #for ending comments, updates state so that it will print the next token
    def sEndComment(self):
        if self.current_char == 47:#/
            self.state = 2
            self.update_info()
            self.position[1]+=len(self.lexeme)
            self.lexeme=''
            return(self.S())
        else:
            #self.update_info()
            return(self.S())

    #for determining equality operators
    def s_operators(self):
        if self.current_char == 61:#=
            self.update_info()
            if self.current_char == 61:
                self.update_info()
                self.identifier = 1
                return(Token(self.ops[self.identifier], self.lexeme, self.position[0:2]))
            else:
                self.identifier = 0
                return(Token(self.ops[self.identifier], self.lexeme, self.position[0:2]))
        elif self.current_char == 60:#<
            self.update_info()
            if self.current_char == 62:#not
                self.update_info()
                self.identifier = 2
                return(Token(self.ops[self.identifier], self.lexeme, self.position[0:2]))
            elif self.current_char == 61:#leq
                self.update_info()
                self.identifier = 3
                return(Token(self.ops[self.identifier], self.lexeme, self.position[0:2]))
            else:#less
                self.identifier = 5
                return(Token(self.ops[self.identifier], self.lexeme, self.position[0:2]))
        else:#>
            self.update_info()
            if self.current_char == 61:#geq
                self.update_info()
                self.identifier = 4
                return(Token(self.ops[self.identifier], self.lexeme, self.position[0:2]))
            else:#greater
                self.identifier = 6
                return(Token(self.ops[self.identifier], self.lexeme, self.position[0:2]))

    #for defining strings
    def sString(self):
        if self.current_char == 34:#"
            self.update_info()
            if self.current_char == 34:
                self.update_info(True)
                return(self.sString())
            else:
                return(Token('STRING', self.lexeme[1:-1], self.position[0:2], defined = False))
        elif self.current_char==126:
            print("error, \" unmatched")
            return(Token('STRING', self.lexeme, self.position[0:2], defined = False))
        else:
            self.update_info()
            return(self.sString())
    #error state
    def sError(self):
        print("error: unnacceptable character found in sequence.")
        #print(self.user_input)
        return(Token(self.id[self.identifier], self.lexeme, self.position[0:2]))
