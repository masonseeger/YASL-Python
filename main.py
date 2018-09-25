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

def checkEOComment(SC, token):
    if (SC.state == 2):
        print(token.information())

def eofFound(SC):
    if(SC.state==-10):
        return(-1)

def commentState(SC, token):
    while(SC.state ==-3):
        if SC.user_input == '~':
            break
        token = SC.next()
        checkEOComment(SC, token)

def tokenLoop(SC, token, parser):
    while(SC.state==0):
        if SC.user_input == '~':
            break
        parser.S(token)
        print(token.information())
        token = SC.next()

def main():
    line = 1
    pos = 0
    ct = 0
    eof = 0
    parser = Parser()
    SC = Scanner(" ", 0)
    print("taking input")
    try:
        user_input = input()
        SC = Scanner(user_input + '~', line)
    #print("new scanner made with input: " + user_input)

        while True:
            if eofFound(SC):
                break

            if SC.state == -3:
                commentState(SC, token)

            token = SC.next()
            checkEOComment(SC, token)

            if eofFound(SC):
                break
            #make all of these state loops their own thing at some point to clean
            #up the code

            while(SC.state==0):
                if SC.user_input == '~':
                    break
                parser.S(token)
                if not(parser.ok):
                    break
                #print(token.information())
                token = SC.next()

            if not(parser.ok):
                break
            if 2>SC.state>-1:
                parser.S(token)
                #print(token.information())

            if not(parser.ok):
                break

            if eofFound(SC):
                break

            line +=1
            SC.position = [line,1,1]
            user_input = input()
            if SC.state == -3:
                SC = Scanner(user_input +'~', line, -3)
            else:
                SC = Scanner(user_input  + '~', line)

    except EOFError:
            eof = Token('EOF', ' ', [line, 1])

    if eof: #EOF found as the first thing in a line
        if(SC.state ==-3):
            print("error, no */ found before EOF")
        print(eof.information())
    elif not(parser.ok):
        print("error in the parser, currently an undefined identifier")
        print("ending the program   ")
    else: #EOF found in the middle of a line
        print(Token('EOF', ' ', SC.position[0:2]).information())

    print(parser.consts)

if __name__ == '__main__':
    main()
'''
Still should clean code more
Should be ready for project #2
PLUS MINUS STAR etc need to print the characters, not the words...

'''
