# Alejandro Vila Casahonda - A01174693
# Daniel Medina – A01286980
# Alejandro Rubalcava Vargas- A01286513

# Token types
SYMBOL, NUMBER, BOOLEAN, STRING, PARENTHESIS, WHITESPACE, ERROR, END = range(8)


def getToken(text, i):
    """
    Reads the next token from 'text' starting at position i.
    Returns (token_type, lexeme, new_position).
    Returns (None, None, i) when the entire input has been consumed.
    """
    # Capture runs of whitespace (spaces, newlines, tabs).
    # They are not syntax tokens but must be preserved so the HTML
    # output retains the original indentation.
    if i < len(text) and text[i].isspace():
        start = i
        while i < len(text) and text[i].isspace():
            i += 1
        return WHITESPACE, text[start:i], i

    # End of input
    if i >= len(text):
        return None, None, i

    c = text[i]

    # End-of-program marker
    if c == "$":
        return END, "$", i + 1

    # Symbol: one or more lowercase letters
    if c.islower():
        start = i
        while i < len(text) and text[i].islower():
            i += 1
        return SYMBOL, text[start:i], i

    # Number: one or more decimal digits
    elif c.isdigit():
        start = i
        while i < len(text) and text[i].isdigit():
            i += 1
        return NUMBER, text[start:i], i

    # Boolean: #t or #f
    elif c == "#":
        if i + 1 < len(text) and text[i + 1] in ("t", "f"):
            return BOOLEAN, text[i:i + 2], i + 2
        else:
            return ERROR, text[i], i + 1

    # String: 0-or-more lowercase letters, digits, or spaces between double quotes
    elif c == '"':
        i += 1          # skip the opening quote
        start = i
        while i < len(text) and text[i] != '"':
            # Only lowercase letters, digits, and plain spaces are valid inside a string
            if not (text[i].islower() or text[i].isdigit() or text[i] == " "):
                return ERROR, text[i], i + 1
            i += 1
        if i >= len(text):
            return ERROR, "cadena sin cerrar", i
        # Include both quotes in the lexeme so the HTML displays them
        return STRING, '"' + text[start:i] + '"', i + 1

    # Parentheses
    elif c in "()":
        return PARENTHESIS, c, i + 1

    # Any other character is a lexical error
    else:
        return ERROR, c, i + 1


def lexer(text):
    """
    Tokenizes the complete input text.

    Returns a tuple (tokens, error_lexeme):
      - Success: (list_of_all_tokens_including_whitespace, None)
      - Failure: (partial_token_list_including_the_error_token, error_lexeme_string)

    Processing stops immediately on the first lexical error.
    """
    i = 0
    tokens = []

    while i < len(text):
        tok_type, lexeme, i = getToken(text, i)

        if tok_type is None:
            break

        tokens.append((tok_type, lexeme))

        # Stop and report the first lexical error
        if tok_type == ERROR:
            return tokens, lexeme

    return tokens, None   # no errors found
