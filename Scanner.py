'''
Created: 9/1/2018
By: Mason Seeger

Scanner class takes in line(s) of strings and returns tokens until the string is
empty or a EOF token is found.
'''
from Token import Token

class Scanner:
    def __init__(self, user_input, line):
        self.user_input = user_input
        self.state = 0
        self.identifier = -1
        self.position = [line,0,0] #line, start pos of current lexem, current pos
        self.current_char = ord(self.user_input[0])
        self.lexeme = ''
        self.keywords = ['program', 'val', 'begin', 'print', 'end', 'div', 'mod']
        self.id = ['NUM', 'ID', 'SEMI', 'PERIOD','STAR','PLUS','MINUS','ASSIGN']
        if self.user_input == 'exit()':
            self.state = -1

    #Returns the next token in the sequence
    def next(self):
        next_token = self.s0()
        self.position[1]+=len(self.lexeme)
        self.lexeme = ''
        self.identifier=-1
        if next_token:
            return next_token
        else:
            self.state = -1
    #return type, lexeme, position

    def update_info(self, space=False):
        if not(space):
            self.lexeme+=self.user_input[0]
        else:
            self.position[1]+=len(self.lexeme)


        if (self.user_input):
            self.user_input = self.user_input[1:]
            self.current_char = ord(self.user_input[0])
            self.position[2]+=1
        else:
            return(Token(self.id[self.identifier], self.lexeme, self.position[0:2]))

    #start of every new scan
    def s0(self):
        if 90>=self.current_char>=65 or 97<=self.current_char<=122:
            self.update_info()
            self.identifier = 1
            return(self.s2())
        elif self.current_char == 32:
            self.update_info(True)
            return(self.s0())
        elif self.current_char ==48:
            self.update_info()
            self.identifier = 0
            self.position[1]+=len(self.lexeme)
            return(Token(self.id[self.identifier], '0', self.position[0:2]))
        elif 49<=self.current_char<=57:
            self.update_info()
            self.identifier = 0
            return(self.s1())
        elif self.current_char == 59 or self.current_char ==46:
            self.update_info()
            return(self.s3())
        elif 42<=self.current_char<=43 or self.current_char == 45\
                or self.current_char == 61:
            self.update_info()
            return(self.s4())
        else:
            self.update_info(True)
            return(-1)

        #need to add in parts for the comments

    #method for numbers
    def s1(self):
        if 48<=self.current_char<=57:
            self.update_info()
            return(self.s1())
        else:
            self.update_info()
            return(Token(self.id[self.identifier],self.lexeme, self.position[0:2]))

    #method for IDs
    def s2(self):
        if 48<=self.current_char<=57 or 90>=self.current_char>=65\
            or 97<=self.current_char<=122:
            self.update_info()
            return(self.s2())
        else:
            self.update_info()
            if self.lexeme.lower() in self.keywords:
                return(Token('Key', self.lexeme, self.position[0:2]))
            return(Token('ID', self.lexeme, self.position[0:2]))

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

    #method for operator
    def s4(self):
        if self.current_char == 42:
            self.update_info()
            self.identifier = 4
            return(Token(self.id[self.identifier], self.lexeme, self.position[0:2]))
        elif self.current_char == 43:
            self.update_info()
            self.identifier = 5
            return(Token(self.id[self.identifier], self.lexeme, self.position[0:2]))
        elif self.current_char == 45:
            self.update_info()
            self.identifier = 6
            return(Token(self.id[self.identifier], self.lexeme, self.position[0:2]))
        else:
            self.update_info()
            self.identifier = 7
            return(Token(self.id[self.identifier], self.lexeme, self.position[0:2]))

    #method for comments
    def s5(self):
        #until you see the ending or a NL char, keep going
        #comments will end tokens
        return(Token(1,1,[1]))
