'''
Created: 9/1/2018
By: Mason Seeger

Token class that consists of a token and the state of the lexicon
'''

class Token:
    def __init__(self, type, lexeme, position):
        self.type = str(type)
        self.position = position
        self.lexeme = str(lexeme)

    def information(self):
        return self.type + ' ' + self.lexeme + ' ' + str(self.position[0]) + ':'+ str(self.position[1])
