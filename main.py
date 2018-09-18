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

def endComment(SC, token):
    if (SC.state == 2):
        print(token.information())

def eofFound(SC):
    if(SC.state==-10):
        return(-1)

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

            while(SC.state ==-3):
                if SC.user_input == '~':
                    break
                token = SC.next()
                endComment(SC, token)

            token = SC.next()

            endComment(SC, token)

            if eofFound(SC):
                break
            #make all of these state loops their own thing at some point to clean
            #up the code

            while(SC.state==0):
                if SC.user_input == '~':
                    break
                parser.S(token)
                print(token.information())
                token = SC.next()

            if 2>SC.state>-1:
                parser.S(token)
                print(token.information())

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
    else: #EOF found in the middle of a line
        print(Token('EOF', ' ', SC.position[0:2]).information())

    print(parser.consts)

if __name__ == '__main__':
    main()
'''
for now everything looks good. Code could be cleaned and optimized a bit though

'''
