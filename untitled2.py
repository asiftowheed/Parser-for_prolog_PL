
import re
from enum import Enum, auto

charClass = int()
lexeme = ""
nextChar = str()
nextToken = int()
token = int()
lineCount = 0

class CharacterClass(Enum):
    UPPERCASECHAR = auto()
    DIGITCHAR = auto()
    LOWERCASECHAR = auto()
    UNKNOWNCHAR = auto()

class TokenCode(Enum):
    UPPERCASE = auto()
    LOWERCASE = auto()
    DIGIT = auto()

    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    SINGLE_QUOTE = auto()
    COMMA = auto()
    AMPERSAND = auto()
    DOLLAR = auto()
    HASH = auto()
    SPACE = auto()
    QUESTION_MARK = auto()
    PERIOD = auto()
    COLON = auto()
    TILDE = auto()
    CARET = auto()
    BACK_SLASH = auto()
    ADDITION_OP = auto()
    SUBTRACTION_OP = auto()
    MULTIPLICATION_OP = auto()
    DIVISION_OP = auto()
    NEWLINE = auto()
    EOF = auto()

def isSpecial(char):
    special = r'[\+\-\*\/\\^~:\.\? #$&]'
    return re.match(special, char)
    
char_map = {"'":TokenCode.SINGLE_QUOTE,
            ',':TokenCode.COMMA,
            '&':TokenCode.AMPERSAND,
            '$':TokenCode.DOLLAR,
            '#':TokenCode.HASH,
            ' ':TokenCode.SPACE,
            '?':TokenCode.QUESTION_MARK,
            '.':TokenCode.PERIOD,
            ':':TokenCode.COLON,
            '~':TokenCode.TILDE,
            '^':TokenCode.CARET,
            '\\':TokenCode.BACK_SLASH,
            '(':TokenCode.LEFT_PAREN,
            ')':TokenCode.RIGHT_PAREN,
            '+':TokenCode.ADDITION_OP,
            '-':TokenCode.SUBTRACTION_OP,
            '*':TokenCode.MULTIPLICATION_OP,
            '/':TokenCode.DIVISION_OP,
            '\n':TokenCode.NEWLINE}
    
def getChar():
    global charClass
    global nextChar
    global lineCount
    nextChar = f.read(1)
    #print('read char:', char)
    if nextChar:
        if nextChar == '\n':
            lineCount += 1
        if nextChar.isalpha():
            if nextChar.isupper():
                charClass = CharacterClass.UPPERCASECHAR
            else:
                charClass = CharacterClass.LOWERCASECHAR
        elif nextChar.isdigit():
            charClass = CharacterClass.DIGITCHAR
        elif nextChar == '_':
            charClass = CharacterClass.UPPERCASECHAR
        else:
            charClass = CharacterClass.UNKNOWNCHAR
    else:
        charClass = TokenCode.EOF

def addChar():
    global lexeme
    lexeme += nextChar

def lookup(c):
    global nextToken
    if c in char_map:
        nextToken = char_map[c]
    else:
        nextToken = TokenCode.EOF

def lex():
    global nextToken
    global lexeme
    lexeme = ""
    if nextToken != TokenCode.QUESTION_MARK or nextToken != TokenCode.COLON:
        skip_ws()
    if charClass == CharacterClass.UPPERCASECHAR:
        addChar()
        getChar()
        while charClass in [CharacterClass.UPPERCASECHAR, CharacterClass.LOWERCASECHAR]:
            addChar()
            getChar()
        nextToken = TokenCode.UPPERCASE
    elif charClass == CharacterClass.LOWERCASECHAR:
        addChar()
        getChar()
        while charClass in [CharacterClass.UPPERCASECHAR, CharacterClass.LOWERCASECHAR]:
            addChar()
            getChar()
        nextToken = TokenCode.LOWERCASE
    elif charClass == CharacterClass.DIGITCHAR:
        addChar()
        getChar()
        while charClass == CharacterClass.DIGITCHAR:
            addChar()
            getChar()
        nextToken = TokenCode.DIGIT
    elif charClass == CharacterClass.UNKNOWNCHAR:
        lookup(nextChar)
        getChar()
    elif charClass == TokenCode.EOF:
        nextToken = TokenCode.EOF
        lexeme = 'EOF'
    print('Next token is: ', nextToken, ', next lexeme is: ', lexeme, sep='')
    return nextToken

def skip_ws():
    global lineCount
    global nextChar
    while re.match('\s',nextChar):
        if nextChar == '\n':
            lineCount += 1
        getChar()
        

def special():
    print('\tEnter <special>')
    if isSpecial(nextChar):
        lex()
    print('\tExit <special>')

#<alphanumeric> -> <lowercase-char> | <uppercase-char> | <digit>
def alphanumeric():
    print('\tEnter <alphanumeric>')
    if isAlphanumeric(nextToken):
        lex()
    else:
        print('\tERROR: Alphanumeric expected <alphanumeric>, line',lineCount)
        lex()
    print('\tExit <alphanumeric>')

def isAlphanumeric(token):
    return token in [TokenCode.LOWERCASE, TokenCode.UPPERCASE, TokenCode.DIGIT]

#<character> -> <alphanumeric> | <special>
def character():
    print('\tEnter <character>')
    if isAlphanumeric(nextToken):
        alphanumeric()
    else:
        special()
    print('\tExit <character>')

#<string> -> <character> | <character> <string>
def string():
    print('\tEnter <string>')
    character()
    spec = isSpecial(nextChar)
    if spec:
        string()
    elif nextToken in [TokenCode.LOWERCASE, TokenCode.UPPERCASE, TokenCode.DIGIT]:
        string()
    print('\tExit <string>')

#<numeral> -> <digit> | <digit> <numeral>
def numeral():
    print('\tEnter <numeral>')
    if nextToken == TokenCode.DIGIT:
        lex()
        if nextToken == TokenCode.DIGIT:
            numeral()
    else:
        print('ERROR: Expected digit in <numeral>, line',lineCount)
        lex()
    print('\tExit <numeral>')

#<character-list> -> <alphanumeric> | <alphanumeric> <character-list>
def character_list():
    print('\tEnter <character_list>')
    alphanumeric()
    if isAlphanumeric(nextToken):
        character_list()
    print('\tExit <character_list>')

#<variable> -> <uppercase-char> | <uppercase-char> <character-list>
def variable():
    print('\tEnter <variable>')
    if nextToken == TokenCode.UPPERCASE:
        lex()
        if isAlphanumeric(nextToken):
            character_list()
    else:
        print('ERROR: Expected uppercase character in <variable>, line',lineCount)
        lex()
    print('\tExit <variable>')

#<small-atom> -> <lowercase-char> | <lowercase-char> <character-list>
def small_atom():
    print('\tEnter <small_atom>')
    if nextToken == TokenCode.LOWERCASE:
        lex()
        if nextToken in [TokenCode.LOWERCASE, TokenCode.UPPERCASE, TokenCode.DIGIT]:
            character_list()
    else:
        print('ERROR: Expected lowercase character in <small_atom>, line',lineCount)
        lex()
    print('\tExit <small_atom>')

#<atom> -> <small-atom> | ' <string> '
def atom():
    print('\tEnter <atom>')
    if nextToken == TokenCode.LOWERCASE:
        small_atom()
    elif nextToken == TokenCode.SINGLE_QUOTE:
        lex()
        string()
        if nextToken == TokenCode.SINGLE_QUOTE:
            lex()
        else:
            print("ERROR: Missing ' in <atom>, line",lineCount)
            lex()
    else:
        print("ERROR: Expected lowercase or ' in <atom>, line",lineCount)
        lex()
    print('\tExit <atom>')

#<term> -> <atom> | <variable> | <structure> | <numeral>
def term():
    print('\tEnter <term>')
    #if nextToken in [TokenCode.LOWERCASE,TokenCode.SINGLE_QUOTE]:
    #    atom()
    if nextToken == TokenCode.DIGIT:
        numeral()
    elif nextToken == TokenCode.UPPERCASE:
        variable()
    elif nextToken == TokenCode.LOWERCASE:
        structure()
    else:
        print('ERROR: Expected type not found in <term>, line',lineCount)
        lex()
    print('\tExit <term>')

#<term-list> -> <term> | <term> , <term-list>
def term_list():
    print('\tEnter <term_list>')
    term()
    if nextToken == TokenCode.COMMA:
        lex()
        term_list()
    elif nextToken != TokenCode.RIGHT_PAREN and nextToken != TokenCode.PERIOD:
        print('\tERROR: Expected ( or ., line',lineCount)
        term_list()
    print('\tExit <term_list>')

#<structure> -> <atom> ( <term-list> )
def structure():
    print('\tEnter <structure>')
    atom()
    if nextToken == TokenCode.LEFT_PAREN:
        lex()
        term_list()
        if nextToken == TokenCode.RIGHT_PAREN:
            lex()
        else:
            print('ERROR: Missing ) in <structure>, line',lineCount)
            lex()
    print('\tExit <structure>')

#<predicate> -> <atom> | <atom> ( <term-list> )
def predicate():
    print('\tEnter <predicate>')
    atom()
    if nextToken == TokenCode.LEFT_PAREN:
        lex()
        term_list()
        if nextToken == TokenCode.RIGHT_PAREN:
            lex()
        else:
            print('ERROR: Missing ) in <predicate>, line',lineCount)
            lex()
    print('\tExit <predicate>')

#<predicate-list> -> <predicate> | <predicate> , <predicate-list>
def predicate_list():
    print('\tEnter <predicate_list>')
    predicate()
    if nextToken == TokenCode.COMMA:
        lex()
        predicate_list()
    print('\tExit <predicate_list>')

#<query> -> ?- <predicate-list> .
def query():
    print('\tEnter <query>')
    global TokenCode
    global nextToken
    if nextToken == TokenCode.QUESTION_MARK:
        lex()
        if nextToken == TokenCode.SUBTRACTION_OP:
            lex()
            predicate_list()
            if nextToken == TokenCode.PERIOD:
                lex();
            else:
                print('ERROR: Missing . in <query>, line',lineCount)
                lex()
        else:
            print('ERROR: Missing - in <query>, line',lineCount)
            lex()
            predicate_list()
    else:
        print('ERROR: Missing ? in <query>, line',lineCount)
        lex()
    print('\tExit <query>')

#<clause> -> <predicate> . | <predicate> :- <predicate-list> .               
def clause():
    print('\tEnter <clause>')
    predicate()
    if nextToken == TokenCode.COLON:
        lex()
        if nextToken == TokenCode.SUBTRACTION_OP:
            lex()
            predicate_list()
        else:
            print('ERROR: Missing - in <clause>, line',lineCount)
            lex()
            predicate_list()
    elif nextToken == TokenCode.PERIOD:
        lex()
    else:
        print('ERROR: Missing . or : in <clause>, line',lineCount)
        lex()
    print('\tExit <clause>')

#<clause-list> -> <clause> | <clause> <clause-list>
def clause_list():
    print('\tEnter <clause_list>')
    clause()
    if nextToken in [TokenCode.LOWERCASE, TokenCode.SINGLE_QUOTE]:
        clause_list()
    print('\tExit <clause_list>')

def program():
    print('\tEnter <program>')
    getChar()
    lex()
    if nextToken == TokenCode.EOF:
        print('\n\n========= END OF PROGRAM =========')
        return
    elif nextToken == TokenCode.QUESTION_MARK:
        query()
    else:
        clause_list()
        query()
    print('\tExit <program>')

import os
text_files = list(filter(lambda x: x[-4:] == '.txt', os.listdir('./')))
f = open('1.txt')
program()
'''
for file in text_files:
    f = open(file)
    print()
    print('========= File',file,'executing =========')
    program()
    lineCount = 0'''