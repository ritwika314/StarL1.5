import ply.lex as lex 


reserved = { "Agent" : 'AGENT' , "MW" : 'MW', 'Init' : 'INIT','pre': 'PRE','eff' : 'EFF', 'exit' : 'EXIT','ObstacleList' : 'OBSTACLELIST',
	     	"int" : 'INT', 'float' : 'FLOAT', 'boolean' : 'BOOL', 'true' : 'TRUE', 'false' : 'FALSE', 'shared': 'SHARED', 'enum': 'ENUM', 'ItemPosition':'ITEMPOSITION', 'Map':'MAP', 'List': 'LIST','Queue':'QUEUE','Stack':'STACK','printLog':'PRINTLOG','isEmpty':'ISEMPTY','null':'NULL', 'return' : 'RETURN', 
	    "log":'LOG','msg':'MSG', "atomic" : 'ATOMIC', 'getRobotIndex' : 'ROBOT','if' : 'IF' , 'else':'ELSE','getmypos' :'GETMYPOS', 'doReachAvoid': 'DOREACHAVOID', 'failFlag':'FAILFLAG', 'doneFlag':'DONEFLAG','remove':'REMOVE','getInput':'GETINPUT'
	   }


tokens = ['BR','SEMI','COMMA',
	'CID','LID',
	'RCURLY','LCURLY','RPAREN','LPAREN',
	'INCR','PLUS','MINUS','TIMES','BY',
	'EQ','GEQ','LEQ','GE','LE','NEQ',
	'EQLS',
	'INUM','FNUM',
	'NOT', 'AND', 'OR'
	] + list(reserved.values())

#meta_chars
t_BR	 = r'\:\:'
t_RCURLY = r'\}'
t_LCURLY = r'\{'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SEMI	 = r';'
t_COMMA	 = r','


#relational operators
t_EQ = r'=='
t_GEQ = r'>='
t_LEQ = r'<='
t_GE = r'>'
t_LE = r'<'
t_NEQ = r'\!='
t_NOT = r'\!'
t_AND = r'\&\&'
t_OR = r'\|\|'



#binary operators
t_INCR = r'\+\+'
t_EQLS = r'='
t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_BY 	= r'\/'



#capitalized identifiers 
def t_CID(t):
	r'[A-Z][.a-zA-Z0-9]*'
	t.type = reserved.get(t.value,'CID') #Check for reserved words 
	return t

#lowercase identifiers	
def t_LID(t):
	r'[a-z][.a-zA-Z0-9]*'
	t.type = reserved.get(t.value,'LID') #Check for reserved words 
	return t

#numbers
def t_FNUM(t):
	r'[\-]?[0-9]+\.[0-9]+'
	return t


def t_INUM(t):
	r'[\-]?[0-9]+'
	return t 


#newline
def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)


t_ignore = ' \t'

#error 
def t_error(t):
	print("Illegal character at '%s' "%t.value[0])
	t.lexer.skip(1)



#build lexer 
lexer = lex.lex()
'''
#test
s = raw_input("Enter filename\n:")
lexer.input(open(s).read())
while(True):
	tok = lexer.token()
	if not tok:
		break
	print tok
'''
