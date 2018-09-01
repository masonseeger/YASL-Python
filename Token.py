'''
Created: 9/1/2018
By: Mason Seeger

Token class that consists of a token and the state of the lexicon
'''

class Token:
    def __init__(self, type, lexeme, position):
        self.type = type
        self.position = position
        self.lexeme = lexeme

    def information(self):
        return self.type + ' ' + self.lexeme + ' ' + self.position
