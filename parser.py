from lexer import lexer
from lexer import SYMBOL, NUMBER, BOOLEAN, STRING, PARENTHESIS, END

textInput = input("Insert input: ")

tokens = lexer(textInput)

# If lexer has none
if tokens is None:
    print("Lexical error:")
    exit()

i = 0

def consumeToken(expectedType):
    global i
    if i < len(tokens) and tokens[i][0] == expectedType:
        i += 1
    else:
        if i >= len(tokens):
            raise SyntaxError(f"Expected {expectedType} but reached end of input")
        else:
            raise SyntaxError(f"Expected {expectedType} but found: {tokens[i]}")
    
def prog():
    global i
    while i < len(tokens) and tokens[i][0] != END:  # END = token para $
        exp()
    
    if i < len(tokens) and tokens[i][0] == END:
        consumeToken(END)  # consume $ al final
    else:
        raise SyntaxError("Program must end with $")

def exp():
    type, lexeme, = tokens[i]

    if type in [SYMBOL, NUMBER, BOOLEAN, STRING]:
        atom()
    elif type == PARENTHESIS and lexeme == "(":
        array()
    else:
        raise SyntaxError(f"Unexpected token: {tokens[i]}")
    
def atom():
    type, lexeme = tokens[i]
    if type in [SYMBOL, NUMBER, BOOLEAN, STRING]:
        consumeToken(type)
    else:
        raise SyntaxError(f"Expected atom but found: {tokens[i]}")
    
def array():
    consumeToken(PARENTHESIS)  # Consume "("
    while i < len(tokens) and not (tokens[i][0] == PARENTHESIS and tokens[i][1] == ")"):
        exp()  # Calls recursively exp()
    consumeToken(PARENTHESIS)  # Consume ")"

try:
    prog()
    print("Correct syntax")
except SyntaxError as e:
    print("Syntax error:", e)