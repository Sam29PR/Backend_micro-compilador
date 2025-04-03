import ply.yacc as yacc
from compiler.lexer import tokens  # Asegúrate de que esta importación es correcta

# Reglas de gramática

# Programa principal
def p_program(p):
    '''program : statement_list'''
    p[0] = ('program', p[1])

# Lista de sentencias
def p_statement_list(p):
    '''statement_list : statement ENDLINE statement_list
                      | statement ENDLINE'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

# Sentencias posibles
def p_statement(p):
    '''statement : statement_write
                 | statement_assign
                 | statement_capture
                 | statement_if'''
    p[0] = p[1]

# Instrucción de salida
def p_statement_write(p):
    '''statement_write : WRITE LPAREN STRING COMMA VARIABLE RPAREN'''
    p[0] = ('write', p[3], p[5])

# Asignaciones
def p_statement_assign(p):
    '''statement_assign : VARIABLE EQUALS expression'''
    p[0] = ('assign', p[1], p[3])

# Captura de entrada
def p_statement_capture(p):
    '''statement_capture : CAPTURE LPAREN VARIABLE RPAREN'''
    p[0] = ('capture', p[3])

# Sentencias IF
def p_statement_if(p):
    '''statement_if : IF LPAREN condition RPAREN THEN statement_list ENDIF'''
    p[0] = ('if', p[3], p[6])

# Expresiones matemáticas
def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    p[0] = (p[2], p[1], p[3])

def p_expression_number(p):
    '''expression : NUMBER'''
    p[0] = ('num', p[1])

def p_expression_variable(p):
    '''expression : VARIABLE'''
    p[0] = ('var', p[1])

# Condiciones lógicas
def p_condition(p):
    '''condition : expression REL_OP expression
                 | condition LOG_OP condition'''
    p[0] = (p[2], p[1], p[3])

# Manejo de errores sintácticos
syntax_errors = []  # Lista para almacenar errores

def p_error(p):
    if p:
        error_msg = f"Error de sintaxis en '{p.value}' en la línea {p.lineno}"
    else:
        error_msg = "Error de sintaxis: Token inesperado o código incompleto"
    
    syntax_errors.append(error_msg)  # Agregar error a la lista


# Construir el parser
parser = yacc.yacc()

# Función para analizar código
def parse_code(code):
    global syntax_errors
    syntax_errors = []  # Limpiar errores previos

    result = parser.parse(code)

    # 🚨 Si hay errores o el resultado es None, retorna errores
    if syntax_errors or result is None:
        return syntax_errors if syntax_errors else ["Error de sintaxis desconocido"]
    else:
        return "Compilación exitosa 🚀"
