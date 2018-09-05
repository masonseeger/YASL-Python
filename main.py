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
    #print("new scanner made with input: " + user_input)
    while True:
        if SC.state == -10:
            break

        while(SC.state ==-3):
            if SC.user_input == '~':
                break
            token = SC.next()

        if SC.state ==2:
            print(token.information())

        token = SC.next()

        if SC.state ==2:
            print(token.information())

        if SC.state == -10:
            break
        #make all of these state loops their own thing at some point to clean
        #up the code
        while(SC.state==0):
            if SC.user_input == '~':
                break
            print(token.information())
            token = SC.next()

        if 2>SC.state>-1:
            print(token.information())

        if SC.state == -10:
            break

        line +=1
        user_input = input()
        if SC.state == -3:
            SC = Scanner(user_input +'~', line, -3)
        else:
            SC = Scanner(user_input  + '~', line)

    print(token.information())

if __name__ == '__main__':
    main()
'''
for now everything looks good. Code could be cleaned and optimized a bit though
'''
