import ply.lex as lex

# Definir los tokens
tokens = [
    'VARIABLE', 'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS',
    'LPAREN', 'RPAREN', 'STRING', 'COMMA', 'ENDLINE',
    'WRITE', 'CAPTURE', 'IF', 'THEN', 'ENDIF', 'REL_OP', 'LOG_OP'
]

# Palabras reservadas
reserved = {
    'write': 'WRITE',
    'capture': 'CAPTURE',
    'if': 'IF',
    'then': 'THEN',
    'end-if': 'ENDIF',
    'and': 'LOG_OP',
    'or': 'LOG_OP',
    'not': 'LOG_OP'
}

# Reglas para tokens simples
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EQUALS  = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_COMMA   = r','
t_ENDLINE = r'::'  

# Operadores relacionales
def t_REL_OP(t):
    r'<=|>=|<>|==|<|>'
    return t

# Cadenas de texto
def t_STRING(t):
    r'\".*?\"'
    return t

# Números
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Variables y palabras reservadas
def t_VARIABLE(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'VARIABLE')  # Detecta palabras clave
    return t

# Ignorar espacios y tabulaciones
t_ignore = ' \t'

# Manejo de saltos de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Manejo de errores
def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}' en la línea {t.lineno}")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()

# Función para obtener tokens
def get_tokens(code):
    lexer.input(code)
    tokens_list = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens_list.append({'type': tok.type, 'value': tok.value})
    return tokens_list
