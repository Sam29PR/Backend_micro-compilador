import ply.yacc as yacc
from compiler.lexer import tokens

syntax_errors = []

# Programa principal
def p_program(p):
    '''program : statement_list'''
    p[0] = ('program', p[1])

# Lista de sentencias
def p_statement_list(p):
    '''statement_list : statement_list statement
                      | statement'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

# Sentencias disponibles
def p_statement(p):
    '''statement : statement_assign
                 | statement_write
                 | statement_capture
                 | statement_if'''
    p[0] = p[1]

# Asignación de variable
def p_statement_assign(p):
    'statement_assign : VARIABLE EQUALS expression ENDLINE'
    p[0] = ('assign', p[1], p[3])

# Escritura en pantalla
def p_statement_write(p):
    'statement_write : WRITE LPAREN STRING COMMA expression RPAREN ENDLINE'
    p[0] = ('write', p[3], p[5])

# Captura de entrada
def p_statement_capture(p):
    'statement_capture : CAPTURE LPAREN VARIABLE RPAREN ENDLINE'
    p[0] = ('capture', p[3])

# Sentencia IF
def p_statement_if(p):
    'statement_if : IF LPAREN condition RPAREN THEN statement_list ENDIF'
    p[0] = ('if', p[3], p[6])

# Expresiones aritméticas
def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    p[0] = (p[2], p[1], p[3])

def p_expression_parens(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = ('num', p[1])

def p_expression_variable(p):
    'expression : VARIABLE'
    p[0] = ('var', p[1])

# Condiciones relacionales
def p_condition_rel(p):
    'condition : expression REL_OP expression'
    p[0] = (p[2], p[1], p[3])

# Condiciones lógicas (and, or)
def p_condition_logic(p):
    'condition : condition LOG_OP condition'
    p[0] = (p[2], p[1], p[3])

# Negación (not cond)
def p_condition_not(p):
    'condition : LOG_OP condition'
    p[0] = ('not', p[2])

# Agrupación con paréntesis en condiciones
def p_condition_group(p):
    'condition : LPAREN condition RPAREN'
    p[0] = p[2]

# Manejo de errores
def p_error(p):
    if p:
        msg = f"Error de sintaxis en '{p.value}' en la línea {p.lineno}"
        print(f"[ERROR] {msg}") 
    else:
        msg = "Error de sintaxis: Código incompleto o inesperado"
    syntax_errors.append(msg)

parser = yacc.yacc()

def parse_code(code):
    global syntax_errors
    syntax_errors = []
    parser.start = 'program'
    result = parser.parse(code)
    if syntax_errors or result is None:
        return syntax_errors if syntax_errors else ["Error de sintaxis desconocido"]
    else:
        return "Compilación exitosa 🚀"
