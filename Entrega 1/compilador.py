from ply import *
import sys

keywords = (
    'LET', 'READ', 'DATA', 'PRINT', 'IF', 'THEN', 'FOR', 'NEXT', 'TO', 'STEP',
    'END', 'STOP', 'DEF', 'DIM', 'REM', 'RETURN'
)

"""
LET le asigna un valor a una variable
READ se usa para agarrar inputs, para mis tests no se usa pero por si las dudas ahi esta
DATA permite generar arreglos de un tamaño mas grande a 10 y va de la mano con READ
PRINT es un print
IF guarda la condicion que provoca algo
THEN es ese algo que se hace al tener el IF
FOR guarda el estado inicial de la variable de control, seguido de TO al rango final y despues STEP que es como va aavanzar el valor inicial
NEXT se usa si no tienes un STEP definido y simplemente le suma 1 a la variable de control
END marca el fin del ciclo
STOP detiene el programa en cualquier momento, sin importar si es el final o no de linea
DEF define el nombre de variable con su valor
DIM define el tamaño de los arreglos
REM comentario de linea
**no existen comentarios de muchas lineas**
RETURN regresa el valor seleccionado


"""

tokens = keywords + (
    'EQUALS', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'POWER',
    'LPAREN', 'RPAREN', 'LT', 'LE', 'GT', 'GE', 'NE',
    'COMMA', 'SEMI', 'INTEGER', 'FLOAT', 'STRING', 'NEWLINE', 'ID'
)

t_ignore = ' \t'

"""
Los comentarios en basic comienzan con REM, y es necesario dada la naturaleza del lenguaje usar REM cada linea. Es decir, no hay comentarios con multiples lineas
"""
def t_REM(t):
    r'REM .*'
    return t

"""
Las variables estan limitadas de A a Z, A0 a A9, B0 a B9, ... , Z0 a Z9
Referencia: https://es.wikipedia.org/wiki/Dartmouth_BASIC en el apartado de Palabras clave en el ultimo parrafo
"""
def t_ID(t):
    r'[A-Z][A-Z0-9]*'
    if t.value in keywords:
        t.type = t.value
    return t

"""
Lista de operadores
igual a
negacion
multiplicacion
exponenciacion
division
mayor que
mayor o igual a
menor que
menor o igual a
no igual a

"""

t_EQUALS = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_POWER = r'\^'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LT = r'<'
t_LE = r'<='
t_GT = r'>'
t_GE = r'>='
t_NE = r'<>'
t_COMMA = r'\,'
"""
Puedes hacer multiples prints en una sola linea al usar el punto y coma
Referencia: https://www.dartmouth.edu/basicfifty/commands.html en la parte de prints
"""
t_SEMI = r';'
t_INTEGER = r'\d+'
t_FLOAT = r'((\d*\.\d+)(E[\+-]?\d+)?|([1-9]\d*E[\+-]?\d+))'
t_STRING = r'\".*?\"'

def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += 1
    return t

##Errores para tokens y yacc

def t_error(t):
    print("Token no valido: %s" % t.value[0])
    ##exit()
    t.lexer.skip(1)
#
# def p_error(t):
#      print("Syntax error in input!")

##Checar orden de los tokens

#Donde se origina el arbol (la raiz o tallo)

# def p_empty(t):
#     'empty :'
#     pass

def p_main(t):
    '''main : list_statements'''

def p_list_statement(t):
    '''list_statements : statement list_statements
                        | if_statement list_statements
                        | for_statement list_statements
                        | end_statement
    '''
def p_statement(t):
    '''statement : INTEGER command NEWLINE
                 | INTEGER NEWLINE
                 | NEWLINE'''

def p_command(t):
    '''command : REM
               | LET ID EQUALS expr
               | PRINT STRING
               | READ expr
               | DATA expr'''

def p_expr(t):
    '''expr : ID PLUS val
            | ID MINUS val
            | ID TIMES val
            | ID DIVIDE val
            | ID POWER val
            | ID COMMA expr
            | ID
            | val COMMA expr
            | val'''

def p_val(t):
    '''val : INTEGER
           | FLOAT'''

def p_end_statement(t):
    ''' end_statement : INTEGER END NEWLINE'''

def p_for_statement(t):
    ''' for_statement : INTEGER FOR ID EQUALS expr TO expr STEP val NEWLINE for_block
                        |  INTEGER FOR ID EQUALS expr TO expr NEWLINE for_block'''

def p_for_block(t):
    ''' for_block : statement for_block
                    | if_statement for_block
                    | for_statement for_block
                    | next_statement
    '''

def p_next_statement(t):
    '''next_statement : INTEGER NEXT ID NEWLINE'''

def p_if_statement(t):
    '''if_statement : INTEGER IF expr EQUALS expr THEN INTEGER NEWLINE'''


def p_error(t):
    if t != None:
        print("Parser error at '%s'" % t.value)


def parse(data, debug=0):
    parser.error=0
    pres = parser.parse(data, debug=debug)
    if parser.error:
        return None
    return pres


if len(sys.argv) == 2:
    with open(sys.argv[1]) as f:
        data = f.read()
        lexer = lex.lex()
        lexer.input(data)
        parser = yacc.yacc()

        while True:
            tok = lexer.token()
            if not tok:
                break
            print(tok)

        parse(data)

else:
    print("Usage: Namefile.py Testfile.bas")
