'''
Created: 9/1/2018
By: Mason Seeger

YASL - Yet Another Simple Language

As of now this program is a lexicon for a simple programming language.
'''
from Scanner import Scanner
from Token import Token


def main():
    line = 1
    pos = 0
    ct = 0
    print("taking input")
    user_input = input()
    SC = Scanner(user_input + '~', line)
    print("new scanner made with input: " + user_input)
    while True:
        if SC.state == -1:
            break

        token = SC.next()

        while(SC.state>=0):
            if SC.user_input == '~':
                #print("line ended...")
                break
            print(token.information())
            #print("token printed, updated user_input: " + SC.user_input)
            pos = len(token.lexeme)
            token = SC.next()

        print(token.information())
        line +=1
        user_input = input()
        SC = Scanner(user_input  + '~', line)

    print("EOF")

if __name__ == '__main__':
    main()
'''
some characters are sticking together at the end of lines
ie 43err should be 43, err; right now it is coming out as 43e, rr
this happens with almost everything, I need to make sure things are not
added when they are not the same type
You probably just need to take out the updates just before any returns...
Also the final else in scanner just needs to return the current token and 
give an 'error state'
Maybe use state for ok, error, or comment...
'''
