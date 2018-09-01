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
        self.position = [line,0,0] #line, start pos of current lexem, current pos
        self.current_char = self.user_input[0]
        self.lexeme = ''
        self.keywords = ['program', 'val', 'begin', 'print', 'end', 'div', 'mod']
        if self.user_input == 'exit()':
            self.state = -1

    #Returns the next token in the sequence
    def next(self):
        next_token = s0()

        return Token(0,0,0)
    #return type, lexeme, position

    def update_info(self, space=False):
        if not(space):
            self.lexeme+=self.user_input[0]
        else:
            self.position[1]+=len(self.lexeme)

        self.current_char = ord(self.user_input[1])
        self.user_input = self.user_input[1:]
        self.position[2]+=1


    #start of every new scan
    def s0(self):
        if 90>=self.current_char>=65 or 97<=self.current_char<=122:
            update_info()
            s2()
        elif self.current_char == 32:
            update_info(True)
            s0()
        elif self.current_char ==48:
            update_info()
            self.position[1]+=len(self.lexeme)
            return(Token('NUM', '0', self.position[0:2]))
        elif 49<=self.current_char<=57:
            update_info()
            s1()
        elif self.current_char == 59 or self.current_char ==46:
            update_info()
            s3()
        elif 42<=self.current_char<=43 or self.current_char == 45\
                or self.current_char == 61:
            update_info()
            s4()
        else:
            update_info(True)
            s0()

        #need to add in parts for the comments

        return(Token(0,0,[0,0]))

    #method for numbers
    def s1(self):
        if 48<=self.current_char<=57:
            update_info()
            s1()
        else:
            update_info()
            return(Token('NUM',self.lexeme, self.position[0:2] ))

    #method for IDs
    def s2(self):
        if 48<=self.current_char<=57 or 90>=self.current_char>=65\
            or 97<=self.current_char<=122:
            update_info()
            s2()
        else:
            update_info()
            if self.lexeme.lower() in self.keywords:
                return(Token('Key', self.lexeme, self.position[0:2]))
            return(Token('ID', self.lexeme, self.position[0:2]))

    #method for punctuation
    def s3(self):
        if self.current_char == 59:
            update_info()
            return(Token('SEMI', self.lexeme, self.position[0:2]))
        else:
            update_info()
            return(Token('PERIOD', self.lexeme, self.position[0:2]))

    #method for operator
    def s4(self):
        if self.current_char == 42:
            update_info()
            return(Token('STAR', self.lexeme, self.position[0:2]))
        elif self.current_char == 43:
            update_info()
            return(Token('PLUS', self.lexeme, self.position[0:2]))
        elif self.current_char == 45:
            update_info()
            return(Token('MINUS', self.lexeme, self.position[0:2]))
        else:
            update_info()
            return(Token('ASSIGN', self.lexeme, self.position[0:2]))

        return(1)

    #method for comments
    def s5(self):
        #until you see the ending or a NL char, keep going
        #comments will end tokens
        return(1)
