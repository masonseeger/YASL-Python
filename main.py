'''
Created: 9/1/2018
By: Mason Seeger

YASL - Yet Another Simple Language

As of now this program is a lexicon for a simple programming language.

Using Windows ctrl+z gives end of file
'''
from Scanner import Scanner
from Token import Token
from Parser import Parser

def eofFound(SC):
    if(SC.state==-10):
        return(-1)

def main():
    eof = 0
    SC = Scanner(" ")
    parser = Parser(SC)
    try:
        user_input = input()
        SC = Scanner(user_input + '~')
        parser = Parser(SC)

        while True:
            token = SC.next()
            if eofFound(SC):
                break
            print(token.information())
            #parser.S(token)

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
