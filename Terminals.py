'''
Created: 10/12/2018
By: Mason Seeger

YASL - Yet Another Simple Language

Terminal grammmar peices from YASL's grammar
'''

class Num:
    def __init__(self, lexeme):
        self.lexeme = lexeme

    def display(self, indent):
        print(indent*' ' + 'NUM ' + str(self.lexeme))

class Id:
    def __init__(self, lexeme):
        self.lexeme = lexeme

    def display(self, indent):
        print(indent*' ' + 'ID ' + self.lexeme)

class Type:
    def __init__(self, lexeme):
        self.lexeme = lexeme

    def display(self, indent):
        print(indent*' ' + 'TYPE ' + self.lexeme)

class TRUE:
    def display(self, indent):
        print(indent*' ' + 'BOOL TRUE')

class FALSE:
    def display(self, indent):
        print(indent*' ' + 'BOOL FALSE')

class Op:
    def __init__(self, lexeme):
        self.lexeme = lexeme

    def display(self, indent):
        print(indent*' ' + 'BinOp ' + self.lexeme)

class StringItem:
    def __init__(self, lexeme):
        self.lexeme = lexeme

    def display(self, indent):
        print(indent*' ' + 'StringItem ' + self.lexeme)

class Input:
    def __init__(self, msg):
        self.lexeme = msg

    def display(self, indent):
        print(indent*' ' + 'Input  ' + self.lexeme)

class Input2:
    def __init__(self, msg, id):
        self.lexeme = msg
        self.id = id

    def display(self, indent):
        print(indent*' ' + 'Input2 ' + self.lexeme +', ' + self.id)
