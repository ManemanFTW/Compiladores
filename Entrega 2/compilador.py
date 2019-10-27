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

##clase nodo para que el arbol se vea coqueto
class Node:
    def __init__(self, type, children=None, leaf=None):
        self.type = type
        if children:
            self.children = children
        else:
            self.children = [ ]
        self.leaf = leaf

    def __str__(self, level=0):
        ret = "\t" * level + repr(self.type)
        if self.leaf:
            ret += " => " + self.leaf + "\n"
        else:
            ret += "\n"
        
        for child in self.children:
            ret += child.__str__(level+1)
        return ret

##Creditos a bruno que me dijo que podia usar la documentacion de Yacc y tambien para
## que se vea bonito, por que si no se ve feo :c


'''
El AST es generado utilizando la clase nodo que recibe como primer parametro el nodo actual, los hijos que genera y el ultimo parametro es si el hujo es una hoja (que no tiene hijos el hijo)
Ademas de eso, descurbi (mas bien entendí) que el arbol usa backtraking o recursividad para generar sus nodos, es decir, comienza una vez que encuentra los nodos hijos que no tiene hijos (hojas) y de ahi se va
en reversa para comenzar a asignarle valores a los nodos iniciales, si encuentra un error al final, no puede regresar a menos que se tengan productiones de error.

Al tener producciones de error usando el token de error (cualquier cosa que no este en la gramatica o en los tokens) es posible decirle al parser que esa produccion existe pero debe de mandarte directamente a un estado final.
Esto es para que el arbol pueda ser generado a pesar de haber errores de parsing, de otra forma no genera el arbol al no tener una salida al encontrar un error.

El arbol generado cuando existe error de parsing es menor y casi siempre es igual ya que como mecanismo de recuperacion, el compilador ignora los errores hasta que encuentre un caracter de recuperacion, en este caso es el NEWLINE.
al encontrar un caracter correcto despues del NEWLINE que es una nueva linea entonces continua haciendo el arbol normalmente.

Por eso, en los tres tests de error de parsing, el arbol ignora todos los errores y busca llegar a un estado estable que es el estado final.
Es una implementacion casi identica al modo panico.
'''
    
def p_main(t):
    '''main : list_statements'''
    t[0] = Node('Main', [t[1]], None)

def p_list_statement(t):
    '''list_statements : statement list_statements
                        | if_statement list_statements
                        | for_statement list_statements
                        | end_statement'''
    if len(t) == 3:
        t[0] = Node('List statement', [t[1], t[2]], None)
    else:
        t[0] = Node('List statement', [t[1]], None)
    
def p_statement(t):
    '''statement : INTEGER command NEWLINE
                 | INTEGER NEWLINE
                 | NEWLINE'''
    #print(t[1])
    if len(t) == 4:
        t[0] = Node('Statement', [t[2]], t[1])
    elif len(t) == 3:
        t[0] = Node('Statement', [t[1]], 'Newline')
    else:
        t[0] = Node('Statement', None, 'Newline')
    

def p_command(t):
    '''command : REM
               | LET ID EQUALS expr
               | PRINT STRING
               | COMMA PRINT'''
    #print(t[1])
    if len(t) == 5:
        t[0] = Node('Command', [t[4]], t[2])
    elif t[1] == 'PRINT':
        t[0] = Node('Command PRINT', None, t[2])
    elif t[1] == ',':
        t[0] = Node('Command REM', None, 'Error')
    elif len(t) == 3:
        t[0] = Node('Command', [t[2]], t[1])
    else:
        t[0] = Node('Command', None, t[1])

def p_command_Erem(t):
    '''command : COMMA PRINT'''
    t[0] = Node('Command PRINT', None, 'Error')

def p_command_Erem(t):
    '''command : LET error'''
    t[0] = Node('Command LET', None, t[1])

def p_error(t):
    print("Sintax error")

def p_command_data(t):
    '''command : DATA numlist'''
    t[0] = Node('Data', [t[2]], None)

def p_numlist(t):
    '''numlist : numlist COMMA val
               | val'''
    if len(t) > 2:
        t[0] = Node('Number list', [t[1], t[3]], None)
    else:
        t[0] = Node('Number list', [t[1]], None)

def p_command_read(t):
    '''command : READ varlist'''
    t[0] = Node('Read', [t[2]], None)

def p_varlist(t):
    '''varlist : varlist COMMA ID
               | ID'''
    if len(t) > 2:
        t[0] = Node('Variable list', [t[1]], None)
    else:
        t[0] = Node('Variable list', None, t[1])

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
    #print(t[1])
    if len(t) == 3:
        t[0] = Node('Expr', [t[1], t[3]], t[1])
    elif t[1] == 'ID':
        #print("Entro id")
        t[0] = Node('Expr', None, t[1])
    else:
        #print("Entro val")
        t[0] = Node('Expr', [t[1]], None)
        
def p_val(t):
    '''val : INTEGER
           | FLOAT'''
    #print(t[1])
    t[0] = Node('Val', None, t[1])

def p_end_statement(t):
    ''' end_statement : INTEGER END'''
    t[0] = Node('End statement', None, 'End')

def p_for_statement(t):
    ''' for_statement : INTEGER FOR ID EQUALS expr TO expr STEP val NEWLINE for_block
                        |  INTEGER FOR ID EQUALS expr TO expr NEWLINE for_block'''
    #print(t[1]+t[2]+t[3]+t[4]+t[6])
    if len(t) == 12:
        t[0] = Node('For statement', [t[5], t[7], t[9], t[11]], t[3])
    else:
        t[0] = Node('For statement', [t[5], t[7], t[9]], t[3])
    

def p_for_block(t):
    ''' for_block : statement for_block
                    | if_statement for_block
                    | for_statement for_block
                    | next_statement'''
    #print(t[1])
    if len(t) == 3:
        t[0] = Node('For block', [t[1], t[2]], None)
    else:
        t[0] = Node('For block', [t[1]], None)

def p_next_statement(t):
    '''next_statement : INTEGER NEXT ID NEWLINE'''
    #print(t[1])
    t[0] = Node('Next Statemment', None, t[1])

def p_if_statement(t):
    '''if_statement : INTEGER IF ID EQUALS val THEN INTEGER NEWLINE'''
    #print(t[1]+t[2]+t[3]+t[4]+t[6]+t[7])
    t[0] = Node('If statement', [t[5]], None)


def p_error(t):
    if t != None:
        print("Parser error at '%s'" % t.value)


def parse(data, debug=1):
    parser.error=0
    pres = parser.parse(data, debug=debug)
    if parser.error:
        return pres
    return pres


if len(sys.argv) == 2:
    with open(sys.argv[1]) as f:
        data = f.read()
        lexer = lex.lex()
        lexer.input(data)

        while True:
            tok = lexer.token()
            if not tok:
                break
            print(tok)
    
    parser = yacc.yacc()
    res = parser.parse(data)
    r = open("AST.txt", "w+")
    r.write(str(res))
    r.close()
    print('Árbol generado en AST.txt')

else:
    print("Usage: Namefile.py Testfile.bas")
