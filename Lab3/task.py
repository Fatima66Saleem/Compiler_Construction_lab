import ply.lex as lex

# Reserved keywords dictionary
reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'int': 'INT',
    'return': 'RETURN'
}

tokens = ('Number', 'ID', 'PLUS', 'MINUS', 'MULT', 'DIV', 'LPAREN', 'RPAREN', 'EQUALS', 'SEMICOLON', 'UNDERSCORE',
           'LB', 'RB', 'LC', 'RC', 'COMMA', 'GE', 'LE', 'EQ', 'NE', 'GT', 'LT')

tokens = tokens + tuple(reserved.values())

# Arithmetic operators
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULT = r'\*'
t_DIV = r'/'

# Parentheses, brackets, braces, and other symbols
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_EQUALS = r'='
t_SEMICOLON = r';'
t_UNDERSCORE = r'_'
t_LB = r'\['
t_RB = r'\]'
t_LC = r'\{'
t_RC = r'\}'
t_COMMA = r','

# Ignore spaces and tabs
t_ignore = ' \t'

# Assignment and comparison operators

t_GE = r'>='
t_LE = r'<='
t_EQ = r'=='
t_NE = r'!='
t_GT = r'>'
t_LT = r'<'

# ID ko FUNCTION ke roop mein define kiya taake reserved words check ho sakein
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

# Number ko FUNCTION ke roop mein define kiya (int/float conversion ke liye)
def t_Number(t):
    r'\d+(\.\d+)?'
    if '.' in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t

def t_comment(t):
    r'\#.*'
    pass

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character '{t.value[0]}'"
          f"at Line number: {t.lineno}")
    
    t.lexer.skip(1)

lexer = lex.lex()

# Test it out
data = input("Enter code: ")
# data = '123 4.56 789 fatima aqsa123 + - * / ( ) = _78 ; { [] } , - if it is reserved >= <= == != > < '

lexer.input(data)

while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)