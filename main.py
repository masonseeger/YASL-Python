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
Literally just needs the EOF indicator and some print statement work.
Make sure to look at the test cases and see where the EOF is in his
I dont want there to be EOF in the middle of a line
Comments.... fuck
make state for comments /* so we know when we find one
also errors and stuffs
'''
