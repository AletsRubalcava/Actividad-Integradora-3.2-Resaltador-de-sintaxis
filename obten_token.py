# Alejandro Vila Casahonda - A01174693
# Daniel Medina – A01286980
# Alejandro Rubalcava Vargas- A01286513

# Token types
SYMBOL, NUMBER, BOOLEAN, STRING, PARENTHESIS, ERROR, END = range(7)

def getToken(text, i):
    # Skip whitespace
    while i < len(text) and text[i].isspace():
        i += 1
        
    # End of input
    if i >= len(text):
        return None, None, i
        
    c = text[i]

    # End symbol
    if c == "$":
        return END, "$", i+1

    # Symbol: lowercase letters
    if c.islower():
        start = i
        while i < len(text) and text[i].islower():
            i += 1
        return SYMBOL, text[start:i], i
    
    # Number: digits
    elif c.isdigit():
        start = i
        while i < len(text) and text[i].isdigit():
            i += 1
        return NUMBER, text[start:i], i
    
    # Boolean: #t or #f
    elif c == "#":
        if i+1 < len(text) and text[i+1] in ["t", "f"]:
            return BOOLEAN, text[i:i+2], i+2
        else:
            return ERROR, text[i], i+1
        
    # String: characters inside quotes
    elif c == '"':
        i += 1  # skip opening quote
        start = i

        while i < len(text) and text[i] != '"':
            # Only allow lowercase, digits, and space
            if not (text[i].islower() or text[i].isdigit() or text[i] == " "):
                return ERROR, text[i], i+1
            i += 1

        # If closing quote not found
        if i >= len(text):
            return ERROR, "String not closed", i
        
        return STRING, text[start:i], i+1  # include closing quote

    # Parenthesis
    elif c in "()":
        return PARENTHESIS, c, i+1
    
    # Any other character = error
    else:
        return ERROR, c, i+1
    

def lexer(text):
    i = 0
    tokens = []

    # Process entire input
    while i < len(text):
        type, lexeme, i = getToken(text, i)

        # No more tokens
        if type is None:
            break

        # Stop on error
        if type == ERROR:
            print("Lexical Error")
            return

        # Save token
        tokens.append((type, lexeme))

    return tokens