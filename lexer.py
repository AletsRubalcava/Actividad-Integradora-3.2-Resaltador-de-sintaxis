SYMBOL, NUMBER, BOOLEAN, STRING, PARENTHESIS, ERROR, END = range(7)

def getToken(text, i):
    while i < len(text) and text[i].isspace():
        i += 1
        
    if i >= len(text):
        return None, None, i
        
    c = text[i]

    if c == "$":
        return END, "$", i+1

    # Symbol
    if c.islower():
        start = i
        while i < len(text) and text[i].islower():
            i += 1
        return SYMBOL, text[start:i], i
    
    # Number
    elif c.isdigit():
        start = i
        while i < len(text) and text[i].isdigit():
            i += 1
        return NUMBER, text[start:i], i
    
    # Boolean
    elif c == "#":
        if i+1 < len(text) and text[i+1] in ["t", "f"]:
            return BOOLEAN, text[i:i+2], i+2
        else:
            return ERROR, text[i], i+1
        
    # String
    elif c == '"':
        i += 1  # Skip first "
        start = i

        while i < len(text) and text[i] != '"':
            if not (text[i].islower() or text[i].isdigit() or text[i] == " "):
                return ERROR, text[i], i+1
            i += 1

        if i >= len(text):
            return ERROR, "String not closed", i
        
        return STRING, text[start:i], i+1  # Consumes last "

    # Parenthesis
    elif c in "()":
        return PARENTHESIS, c, i+1
    
    # Error
    else:
        return ERROR, c, i+1
    
def lexer(text):
    i = 0
    tokens = []

    while i < len(text):
        type, lexeme, i = getToken(text, i)

        if type is None:
            break

        if type == ERROR:
            print("Lexical Error")
            return

        tokens.append((type, lexeme))

    return tokens