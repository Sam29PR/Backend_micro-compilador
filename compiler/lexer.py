import ply.lex as lex

# Palabras reservadas
reserved = {
    'write': 'WRITE',
    'capture': 'CAPTURE',
    'if': 'IF',
    'then': 'THEN',
    'end-if': 'ENDIF',
    'and': 'AND',
    'or': 'OR',
    'not': 'NOT'
}

# Lista de tokens
tokens = [
    'VARIABLE', 'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS',
    'LPAREN', 'RPAREN', 'STRING', 'COMMA', 'DOUBLECOLON',
    'REL_OP'
] + list(reserved.values())

# Tokens simples
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r','
t_DOUBLECOLON = r'::'

def t_REL_OP(t):
    r'<=|>=|<>|<|>'
    return t

def t_STRING(t):
    r'\".*?\"'
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_VARIABLE(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'VARIABLE')
    return t

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}' en la línea {t.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()

def get_tokens(code):
    lexer.input(code)
    tokens_list = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)  # Para depuración
        tokens_list.append({'type': tok.type, 'value': tok.value})
    return tokens_list
