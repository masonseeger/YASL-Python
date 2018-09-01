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
    user_input = input()
    SC = Scanner(user_input, line)

    while True:
        if SC.state == -1:
            break

        current_token = Token(SC.next())

        while(SC.state>=0):
            print(current_token.information())
            pos = len(current_token.lexeme)
            current_token = Token(SC.next())

        line +=1
        user_input = input()
        SC = Scanner(user_input, line)

    print("EOF")

if __name__ == '__main__':
    main()

#make something in the while for NL character
#think about making a dict or hashmap for the whole returning things in Scanner
