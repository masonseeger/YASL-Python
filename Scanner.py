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
        next_token = self.s0()
        self.position[1]+=len(self.lexeme)
        self.lexeme = ''
        self.identifier=-1
        print(next_token)
        if self.state == -2: #comment of type //
            self.state = 0
            self.getNextLine()
            return(self.next())
        elif self.state==-3: #comment of type /*
            if next_token == -1: #end of line found
                self.state = -3
                self.getNextLine()
                return(self.next())
            else: #comment state in the middle of a line
                self.state = -3
                print("in comment state")
                return(self.next())
        elif next_token ==-1: #EOL found
            self.getNextLine()
            return(self.next())
        elif self.state == -10: #ctrl+Z found (EOF)
            print(" ")
        else: #token found outside of comments, needs to be returned
            print(next_token.information())
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
    def s0(self):
        if (self.current_char == 26): #EOF (ctrl+Z)
            if(self.state==-3): #in comment state
                print("error, no */ found before EOF")
                print(Token('EOF', ' ', self.position[0:2]).information())
                self.state = -10
            else:
                self.update_info()
                self.state = -10
                print(Token('EOF', ' ', self.position[0:2]).information())
        elif self.state == -3: #in comment state
            if self.current_char == 42: # *
                self.update_info()
                return(self.s6())
            elif self.current_char == 126: # ~
                return (-1)
            else:
                self.update_info()
                return(self.s0())
        elif 90>=self.current_char>=65 or 97<=self.current_char<=122: # A-Z, a-z
            self.update_info()
            self.identifier = 1
            return(self.s2())
        elif self.current_char == 32: # space
            self.update_info(True)
            return(self.s0())
        elif self.current_char ==48: # 0
            self.update_info()
            self.identifier = 0
            self.position[1]+=len(self.lexeme)
            return(Token(self.id[self.identifier], '0', self.position[0:2],
                         defined = False))
        elif 49<=self.current_char<=57: #1-9
            self.update_info()
            self.identifier = 0
            return(self.s1())
        elif self.current_char == 59 or self.current_char ==46: # ;, .
            return(self.s3())
        elif 42<=self.current_char<=43 or self.current_char == 45: # operators
            return(self.s4())
        elif self.current_char == 47: #/
            self.update_info()
            return(self.s5())
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
            return(self.s_string())
        elif self.current_char == 126: # ~
            return (-1)
        else: # error state
            self.update_info(True)
            return(self.s7())

    #method for numbers
    def s1(self):
        if 48<=self.current_char<=57:
            self.update_info()
            return(self.s1())
        else:
            #self.update_info()
            return(Token(self.id[self.identifier],self.lexeme, self.position[0:2],
                         defined = False))

    #method for IDs
    def s2(self):
        if 48<=self.current_char<=57 or 90>=self.current_char>=65\
            or 97<=self.current_char<=122:
            self.update_info()
            return(self.s2())
        else: # keyword
            if self.lexeme in self.keywords:
                return(Token(self.lexeme, self.lexeme, self.position[0:2]))
            return(Token('ID', self.lexeme, self.position[0:2], defined = False))

    #method for punctuation
    def s3(self):
        if self.current_char == 59:
            self.update_info()
            self.identifier = 2
            return(Token(self.id[self.identifier], self.lexeme, self.position[0:2]))
        else:
            self.update_info()
            self.identifier = 3
            return(Token(self.id[self.identifier], self.lexeme, self.position[0:2]))

    #method for computational operators
    def s4(self):
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
    def s5(self):
        if self.current_char == 47: #/
            self.state = -2
        elif self.current_char == 42: #*
            self.state = -3
            self.update_info()
            return(self.s0())
        else:
            self.state = 0
            return(self.s7())
        #until you see the ending or a NL char, keep going
        #comments will end tokens
        return(-2)

    #for ending comments, updates state so that it will print the next token
    def s6(self):
        if self.current_char == 47:#/
            self.state = 2
            self.update_info()
            self.position[1]+=len(self.lexeme)
            self.lexeme=''
            return(self.s0())
        else:
            self.update_info()
            return(self.s0())

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
    def s_string(self):
        if self.current_char == 34:#"
            self.update_info()
            if self.current_char == 34:
                self.update_info(True)
                return(self.s_string())
            else:
                return(Token('STRING', self.lexeme, self.position[0:2], defined = False))
        elif self.current_char==126:
            print("error, \" unmatched")
            return(Token('STRING', self.lexeme, self.position[0:2], defined = False))
        else:
            self.update_info()
            return(self.s_string())
    #error state
    def s7(self):
        print("error: unnacceptable character found in sequence.")
        #print(self.user_input)
        return(Token(self.id[self.identifier], self.lexeme, self.position[0:2]))
