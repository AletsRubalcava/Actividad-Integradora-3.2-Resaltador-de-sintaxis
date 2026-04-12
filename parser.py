# Alejandro Vila Casahonda - A01174693
# Daniel Medina – A01286980
# Alejandro Rubalcava Vargas- A01286513

# Import lexer and token types
from obten_token import lexer
from obten_token import SYMBOL, NUMBER, BOOLEAN, STRING, PARENTHESIS, END

# Get user input
textInput = input("Insert input: ")

# Generate tokens
tokens = lexer(textInput)

# If lexer failed, stop program
if tokens is None:
    exit()

i = 0  # current token index

# Check and consume expected token
def consumeToken(expectedType):
    global i
    if i < len(tokens) and tokens[i][0] == expectedType:
        i += 1  # move to next token
    else:
        # Error if token is not what we expect
        if i >= len(tokens):
            raise SyntaxError(f"Expected {expectedType} but reached end of input")
        else:
            raise SyntaxError(f"Expected {expectedType} but found: {tokens[i]}")
    
# Program rule: sequence of expressions ending with $
def prog():
    global i
    while i < len(tokens) and tokens[i][0] != END:
        exp()
    
    # Check final $
    if i < len(tokens) and tokens[i][0] == END:
        consumeToken(END)
    else:
        raise SyntaxError("Program must end with $")

# Expression rule
def exp():
    type, lexeme = tokens[i]

    # If simple value is atom
    if type in [SYMBOL, NUMBER, BOOLEAN, STRING]:
        atom()
    # If "(" is array
    elif type == PARENTHESIS and lexeme == "(":
        array()
    else:
        raise SyntaxError(f"Unexpected token: {tokens[i]}")
    
# Atom rule: simple tokens
def atom():
    type, lexeme = tokens[i]
    if type in [SYMBOL, NUMBER, BOOLEAN, STRING]:
        consumeToken(type)
    else:
        raise SyntaxError(f"Expected atom but found: {tokens[i]}")
    
# Array rule: ( exp* )
def array():
    consumeToken(PARENTHESIS)  # consume "("
    
    # Process expressions inside parentheses
    while i < len(tokens) and not (tokens[i][0] == PARENTHESIS and tokens[i][1] == ")"):
        exp()
    
    consumeToken(PARENTHESIS)  # consume ")"

# Run parser
try:
    prog()
    print("Correct syntax")
except SyntaxError as e:
    print("Syntax Error:", e)