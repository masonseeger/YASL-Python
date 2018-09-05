'''
Created: 9/1/2018
By: Mason Seeger

Token class that consists of a token and the state of the lexicon
'''

class Token:
    def __init__(self, type, lexeme, position, defined = True):
        self.type = type.upper()
        self.position = position
        self.lexeme = str(lexeme)
        self.defined = defined

    def information(self):
        if self.defined:
            return self.type + ' ' + str(self.position[0]) + ':'+ str(self.position[1])
        else:
            return self.type + ' ' + self.lexeme + ' ' + str(self.position[0]) + ':'+ str(self.position[1])
