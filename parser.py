# Alejandro Vila Casahonda - A01174693
# Daniel Medina – A01286980
# Alejandro Rubalcava Vargas- A01286513

import sys
from obten_token import (lexer,
                        SYMBOL, NUMBER, BOOLEAN, STRING,
                        PARENTHESIS, WHITESPACE, ERROR, END)

OUTPUT_FILE = "output.html" # cambiar para nuevo archivo

# ligar los tokens a una clase de css
CSS_CLASS = {
    SYMBOL:      "symbol",
    NUMBER:      "number",
    BOOLEAN:     "boolean",
    STRING:      "string",
    PARENTHESIS: "parenthesis",
    END:         "end",
    ERROR:       "error",
}

# ── HTML helpers ──────────────────────────────────────────────────────────────

def html_escape(text):
    """Escape the three characters that are special inside HTML text."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_html_body(tokens):
    """
    Convert a token list to an HTML string.
    Whitespace tokens are emitted as-is (the surrounding <pre> preserves them).
    Every other token is wrapped in a <span> with the appropriate CSS class.
    """
    parts = []
    for tok_type, lexeme in tokens:
        if tok_type == WHITESPACE:
            parts.append(html_escape(lexeme))
        else:
            cls = CSS_CLASS.get(tok_type, "error")
            parts.append(f'<span class="{cls}">{html_escape(lexeme)}</span>')
    return "".join(parts)


def write_html(body, error_msg=None):
    """
    Write a complete, valid HTML file to OUTPUT_FILE.
    If error_msg is given it is appended inside a styled <span>.
    """
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(
            '<!DOCTYPE html>\n'
            '<html lang="es">\n'
            '<head>\n'
            '    <meta charset="UTF-8">\n'
            '    <title>Resaltador de Sintaxis</title>\n'
            '    <link rel="stylesheet" href="resalta_sintaxis.css">\n'
            '</head>\n'
            '<body>\n'
            '<pre class="code">'
        )
        f.write(body)
        if error_msg:
            f.write(f'\n<span class="error-msg">{html_escape(error_msg)}</span>')
        f.write(
            '\n</pre>\n'
            '</body>\n'
            '</html>\n'
        )


# ── Recursive-descent parser ──────────────────────────────────────────────────
# Grammar (must not be modified):
#   <prog>      ::= <exp> <prog> | $
#   <exp>       ::= <atom> | <list>
#   <atom>      ::= symbol | <constant>
#   <constant>  ::= number | boolean | string
#   <list>      ::= ( <elements> )
#   <elements>  ::= <exp> <elements> | ε

parse_tokens = []   # non-whitespace tokens (the ones the grammar cares about)
idx = 0             # current position inside parse_tokens


def consume(expected_type):
    """Advance past the current token if it matches expected_type; otherwise raise SyntaxError."""
    global idx
    if idx < len(parse_tokens) and parse_tokens[idx][0] == expected_type:
        idx += 1
    else:
        if idx >= len(parse_tokens):
            raise SyntaxError("Se esperaban más tokens pero se llegó al final de la entrada")
        raise SyntaxError(f"Se esperaba tipo {expected_type} pero se encontró: {parse_tokens[idx]}")


def prog():
    """<prog> ::= <exp> <prog> | $"""
    global idx
    while idx < len(parse_tokens) and parse_tokens[idx][0] != END:
        exp()
    if idx < len(parse_tokens) and parse_tokens[idx][0] == END:
        consume(END)
    else:
        raise SyntaxError("El programa debe terminar con $")


def exp():
    """<exp> ::= <atom> | <list>"""
    tok_type, lexeme = parse_tokens[idx]
    if tok_type in (SYMBOL, NUMBER, BOOLEAN, STRING):
        atom()
    elif tok_type == PARENTHESIS and lexeme == "(":
        lst()
    else:
        raise SyntaxError(f"Token inesperado: {parse_tokens[idx]}")


def atom():
    """<atom> ::= symbol | number | boolean | string"""
    tok_type, _ = parse_tokens[idx]
    if tok_type in (SYMBOL, NUMBER, BOOLEAN, STRING):
        consume(tok_type)
    else:
        raise SyntaxError(f"Se esperaba un átomo pero se encontró: {parse_tokens[idx]}")


def lst():
    """<list> ::= ( <elements> )"""
    consume(PARENTHESIS)    # consume opening "("
    elements()
    consume(PARENTHESIS)    # consume closing ")"


def elements():
    """<elements> ::= <exp> <elements> | ε"""
    # Keep consuming expressions until we see ")" or run out of tokens
    while (idx < len(parse_tokens) and
        not (parse_tokens[idx][0] == PARENTHESIS and parse_tokens[idx][1] == ")")):
        exp()


# ── Main ──────────────────────────────────────────────────────────────────────

print("Ingresa el programa (Ctrl+D para finalizar):")
text = input()

# ── Step 1: Lexical analysis ──────────────────────────────────────────────────
all_tokens, lex_error = lexer(text)

if lex_error is not None:
    # The ERROR token is already the last element of all_tokens so it will be
    # rendered in red by build_html_body.
    body = build_html_body(all_tokens)
    write_html(body, ">> ERROR LEXICO <<")
    print(f"Error léxico: '{lex_error}'. Salida escrita en {OUTPUT_FILE}")
    sys.exit(1)

# ── Step 2: Build HTML body from the full token list (whitespace included) ───
html_body = build_html_body(all_tokens)

# ── Step 3: Strip whitespace tokens — the parser only needs syntax tokens ────
parse_tokens = [(t, l) for t, l in all_tokens if t != WHITESPACE]

# ── Step 4: Syntactic analysis ────────────────────────────────────────────────
try:
    prog()
    write_html(html_body)
    print(f"Sintaxis correcta. Salida escrita en {OUTPUT_FILE}")
except SyntaxError as e:
    write_html(html_body, ">> ERROR SINTÁCTICO <<")
    print(f"Error sintáctico: {e}. Salida escrita en {OUTPUT_FILE}")
    sys.exit(1)
