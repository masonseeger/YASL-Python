'''
Created: 9/1/2018
By: Mason Seeger

YASL - Yet Another Simple Language

As of now this program is a lexicon for a simple programming language.

Using Windows ctrl+z gives end of file
'''
import sys
from Scanner import Scanner
from Token import Token
from Parser import Parser
from Interpreter import Interpreter

def eofFound(SC):
    if(SC.state==-10):
        return(-1)

def main():
    fileName = sys.argv[1]
    f = open(fileName, 'r')
    eof = 0

    try:
        SC = Scanner(f)
        parser = Parser(SC)
        program = parser.S()
        interpreter = Interpreter(program)
        interpreter.interpProgram()
        #program.display(0)

    except EOFError:
            eof = Token('EOF', ' ', [SC.position[0],1])

    if eof: #EOF found as the first thing in a line
        print("in eof")
        if(SC.state ==-3):
            print("error, no */ found before EOF")
        print(eof.information())
    elif not(parser.ok):
        print("error in the parser, currently an undefined identifier")
        print("ending the program   ")

    #print(parser.consts)

if __name__ == '__main__':
    main()
