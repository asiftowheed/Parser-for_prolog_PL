# -*- coding: utf-8 -*-
"""
Created on Mon May  7 14:46:04 2018

@author: Asif Towheed
"""

import os
import re

def special():
    global nextToken
    global numErrors
    global programLine
    global programColumn
    if ADDITION_OPERATOR <= nextToken <= AMPERSAND:
        lex()
    else:
        print('Syntax Error special')
        numErrors += 1
        lex()


def character():
    global nextToken
    if UPPER_LETTERS <= nextToken <= DIGITS:
        alphanumericCharacter()
    else:
        special()


def string():
    global nextToken
    character()
    if UPPER_LETTERS <= nextToken <= AMPERSAND:
        string()


def numeral():
    global nextToken
    global numErrors
    if nextToken == DIGITS:
        lex()
        if nextToken == DIGITS:
            numeral()
    else:
        print('Syntax Error numeral')
        numErrors += 1
        lex()


def alphanumericCharacter():
    global nextToken
    global numErrors
    if UPPER_LETTERS <= nextToken <= DIGITS:
        lex()
    else:
        print('Syntax Error alpha')
        numErrors += 1
        lex()


def characterList():
    global nextToken
    alphanumericCharacter()
    if UPPER_LETTERS <= nextToken <= DIGITS:
        characterList()


def variable():
    global nextToken
    global numErrors
    if nextToken == UPPER_LETTERS:
        lex()
        if UPPER_LETTERS <= nextToken <= DIGITS:
            characterList()
    else:
        print('Syntax Error var')
        numErrors += 1
        lex()


def smallAtom():
    global nextToken
    global numErrors
    if nextToken == LOWER_LETTERS:
        lex()
        if UPPER_LETTERS <= nextToken <= DIGITS:
            characterList()
    else:
        print('Syntax Error satom')
        numErrors += 1
        lex()


def atom():
    global nextToken
    global numErrors
    if nextToken == LOWER_LETTERS:
        smallAtom()
    elif nextToken == SINGLE_QUOTATION:  # if the token is a single quotation
        lex()
        string()
        if nextToken == SINGLE_QUOTATION:
            lex()
        else:
            print('Syntax Error atom 1 at line:',programLine,"column:",programColumn)
            numErrors += 1
            lex()
    else:
        print('Syntax Error atom 2 at line:',programLine,"column:",programColumn)
        numErrors += 1
        lex()


def structure():
    global nextToken
    global numErrors
    atom()
    if nextToken == LEFT_PARENTHESIS:
        lex()
        termList()
        if nextToken == RIGHT_PARENTHESIS:
            lex()
        else:
            print('Syntax Error struct at line:',programLine,"column:",programColumn)
            numErrors += 1
            lex()


def term():
    global nextToken
    global numErrors
    if nextToken == DIGITS:
        numeral()
    elif nextToken == UPPER_LETTERS:
        variable()
    elif nextToken == LOWER_LETTERS or nextToken == SINGLE_QUOTATION:
        structure()  # SEE IF YOU CAN SPLIT ATOM AD STRUCTURE TO DISTINGUISH THE CODE
    else:
        print('Syntax Error term at line:',programLine,"column:",programColumn)
        numErrors += 1
        lex()


def termList():
    global nextToken
    global numErrors
    term()
    if nextToken == COMMA:
        lex()
        termList()
    elif nextToken != RIGHT_PARENTHESIS and nextToken != FULL_STOP:
        print('Syntax Error termlist at line:',programLine,"column:",programColumn)
        numErrors += 1
        termList()


def predicate():
    global nextToken
    global numErrors
    atom()
    if nextToken == LEFT_PARENTHESIS:
        lex()
        termList()
        if nextToken == RIGHT_PARENTHESIS:
            lex()
        else:
            print('Syntax Error predicate at line:',programLine,"column:",programColumn)
            numErrors += 1
            lex()


def predicateList():
    global nextToken
    predicate()
    if nextToken == COMMA:
        lex()
        predicateList()


def query():
    global nextToken
    global numErrors
    if nextToken == QUESTION_MARK:
        lex()
        if nextToken == SUBTRACTION_OPERATOR:
            lex()
            predicateList()
            if nextToken == FULL_STOP:
                lex()
            else:
                print('Syntax Error query1 at line:',programLine,"column:",programColumn)
                numErrors += 1
                lex()
        else:
            print('Syntax Error query2 at line: ',programLine,"column:",programColumn)
            numErrors += 1
            lex()
            predicateList()
    else:
        print('Syntax Error query3 at line: ',programLine,"column: ",programColumn)
        numErrors += 1
        lex()


def clause():
    global nextToken
    global numErrors
    predicate()
    if nextToken == COLON:
        lex()
        if nextToken == SUBTRACTION_OPERATOR:
            lex()
            predicateList()
        else:
            print('Syntax Error clause1 at line number',programLine," column: ",programColumn)
            numErrors += 1
            lex()
            predicateList()
    if nextToken == FULL_STOP:
        lex()
    else:
        print('Syntax Error clause2 at line number:',programLine," column: ",programColumn)
        numErrors += 1
        lex()


def clauseList():
    global nextToken
    clause()
    if nextToken == LOWER_LETTERS or nextToken == SINGLE_QUOTATION:
        clauseList()


def program():
    global nextToken
    getChar()
    lex()
    if nextToken == EOF:
        print("Exit <program>")
        return
    elif nextToken == QUESTION_MARK:
        query()
    else:
        clauseList()
        query()


# ===================================================================
# HUSSU STUFF



        # CONSTANTS
UPPERCASE = 0
LOWERCASE = 1
DIGIT = 2
UNKNOWN = 99
# TOKENS
UPPER_LETTERS = 5
LOWER_LETTERS = 10
DIGITS = 15
ADDITION_OPERATOR = 20
SUBTRACTION_OPERATOR = 25
MULTIPLICATION_OPERATOR = 30
DIVISION_OPERATOR = 35
BACK_SLASH = 40
CHAPEAU = 45  # ^
TILDE = 50
COLON = 55
FULL_STOP = 60
QUESTION_MARK = 65
HASH = 70
DOLLAR_SIGN = 75
AMPERSAND = 80
LEFT_PARENTHESIS = 85
RIGHT_PARENTHESIS = 90
SINGLE_QUOTATION = 95
COMMA = 100
EOF = 105

charClass = None
lexeme = ''
nextChar = None
lexLen = None
nextToken = 12345
programLine = 1
programColumn = -1
numErrors = 0
currentFile = None


def getChar():
    global currentFile
    global programColumn
    global charClass
    global nextChar
    nextChar = currentFile.read(1)
    if nextChar:
        if re.match(r'[A-Z_]', nextChar):
            charClass = UPPERCASE
        elif re.match(r'[a-z]', nextChar):
            charClass = LOWERCASE
        elif re.match(r'\d', nextChar):
            charClass = DIGIT
        else:
            charClass = UNKNOWN
        programColumn = programColumn + 1
    else:
        charClass = EOF


def addChar():
    global nextChar
    global lexeme
    lexeme += nextChar


def getNonBlank():
    global nextChar
    global programLine
    global programColumn
    while re.match('\s', nextChar):
        if nextChar == '\n':
            programLine += 1
            programColumn = -1
        getChar()


def lookup():
    global nextChar
    global nextToken
    lookupDict = {'(': LEFT_PARENTHESIS, ')': RIGHT_PARENTHESIS, '+': ADDITION_OPERATOR,
                  '-': SUBTRACTION_OPERATOR, '*': MULTIPLICATION_OPERATOR, '/': DIVISION_OPERATOR,
                  '\\': BACK_SLASH, '^': CHAPEAU, '~': TILDE, ':': COLON, '?': QUESTION_MARK, '.': FULL_STOP, '#': HASH, '$': DOLLAR_SIGN,
                  '&': AMPERSAND, '\'': SINGLE_QUOTATION, ',': COMMA}
    nextToken = lookupDict.get(nextChar, EOF)
    addChar()


def lex():
    global charClass
    global lexeme
    global nextToken
    lexeme = ''
    if nextToken != QUESTION_MARK or nextToken != COLON:
        getNonBlank()
    if charClass == UPPERCASE:
        addChar()
        getChar()
        while charClass == UPPERCASE or charClass == LOWERCASE:
            addChar()
            getChar()
        nextToken = UPPER_LETTERS
    elif charClass == LOWERCASE:
        addChar()
        getChar()
        while charClass == UPPERCASE or charClass == LOWERCASE:
            addChar()
            getChar()
        nextToken = LOWER_LETTERS
    elif charClass == DIGIT:
        addChar()
        getChar()
        while charClass == DIGIT:
            addChar()
            getChar()
        nextToken = DIGITS
    elif charClass == UNKNOWN:
        lookup()
        getChar()
    elif charClass == EOF:
        lexeme = 'EOF'


def main():
    global currentFile
    global numErrors
    global programLine
    global programColumn
    
    for index,f in enumerate(os.listdir(os.getcwd()),1):
        if re.match(r'[1-9]\d*\.txt', f) and index==int(os.path.splitext(f)[0]):               
            currentFile = open(f)
            print(f)
            numErrors = 0
            programLine = 1
            programColumn = -1
            program()
            print(numErrors)
        else:
            print("File Input Sequence Broken!")
            break


main()


"""
say(N, From, To) :- write('move disc '), write(N), write(' from '),
 write(From), write(' to '), write(To), nl.
hanoi(N) :- move(N, left, center, right).
move(0, _, _, _).
move(N, From, To, Using) :- is(M, N-1), move(M, From, Using, To),
 say(N, From, To), move(M, Using, To, From).
?- hanoi(3).
"""
