import ply.yacc as yacc

from scanner import *
from ast import * 
from symtab import *
#initializing symbol table
global symtab
symtab = []
#number of mutexes
global wnum
wnum = 0
global mutexcount
mutexcount = 0


def p_pgm(p):
	''' pgm : agentDecl mwblock decls initblock'''
	for i in range(mutexcount):
		newdecl = declAst('boolean','wait'+str(i),'false','local')
		p[3].append(newdecl)
		global symtab
		symtab.append(mkentry(newdecl))
	p[0] = pgmAst(p[1],p[2],p[3],p[4])



#agentname
def p_agentDecl(p):
	'''agentDecl : AGENT BR CID '''
	p[0] = p[3]
#init block
def p_initblock(p):
	''' initblock : INIT LPAREN RPAREN LCURLY events RCURLY '''
	p[0] = initAst(p[5])

#events 
def p_events(p):
	'''events : event events
		  | empty
	'''
	elist = []
	if len(p) is 3:
		elist.append(p[1])
		elist += p[2]
	else:
		elist = []
	
	p[0] = elist 

def p_event(p):
	'''event : robotinit
		 | getpos SEMI
		 | varname LPAREN RPAREN LCURLY pre eff RCURLY
		 | EXIT LPAREN RPAREN LCURLY pre eff RCURLY
	'''
	if len(p) is 2 :
		global symtab
		symtab.append(symEntry('int','robotIndex','local'))
		p[0] = p[1]		 
	elif len(p) is 3:
		p[0] = getAst(p[1])
	else:
		p[0] = eventAst(p[1],p[5],p[6])


def p_getpos(p):
	'''getpos : varname EQLS GETMYPOS LPAREN RPAREN'''
	p[0] = p[1]

def p_robotinit(p):
	'''robotinit : ROBOT LPAREN RPAREN SEMI'''
	p[0] = robotDecl() 

def p_pre(p):
	'''pre : PRE LPAREN cond RPAREN SEMI
	       | PRE LPAREN TRUE RPAREN SEMI
	'''
	p[0] = p[3] 

#condition
def p_cond(p):
	'''cond : rel
		| expr 
		| cond AND cond
		| cond OR cond
	       	| NOT expr 
		| LPAREN cond RPAREN 
	'''
	if len(p) is 2:
		p[0] = p[1]
	elif len(p) is 3 :
		p[0] = condAst(p[1],p[2])
	elif p[1] is not "(":
		p[0] = condAst(p[2],p[1],p[3])
	else:
		 p[0] = p[2]

def p_rel(p):
	'''rel : expr EQ expr 
	       | expr NEQ expr
	       | expr GEQ expr
	       | expr LEQ expr 
	       | expr GE expr
	       | expr LE expr 
	'''
	p[0] = relAst(p[2],p[1],p[3])

def p_eff(p):
	'''eff : EFF LCURLY stmts RCURLY'''
	p[0] = p[3]

#statements
def p_stmts(p):
	'''stmts : stmt stmts 
		 | empty
	'''
	slist = []
	if len(p) is 3:
		slist.append(p[1])
		slist += p[2]
	else:
		slist = []
	p[0]= slist 

def p_stmt(p):
	'''stmt : asgn
		| ite 
		| atomic
		| funcCall
		| callreachavoid
	'''
	p[0] = p[1]

def p_callreachavoid(p):
	'''callreachavoid : REACHAVOID LPAREN varname COMMA val RPAREN
	'''
	p[0] = raAst(p[3],p[5])

def p_ite(p):
	'''ite : IF LPAREN cond RPAREN LCURLY stmts RCURLY ELSE LCURLY stmts RCURLY'''
	p[0] = ifAst(p[3],p[6],p[10])
#function call 
def p_funcCall(p):
	'''funcCall : varname LPAREN RPAREN SEMI '''
	p[0] = funcAst(p[1])
	
#atomic statement
def p_atomic(p):
	'''atomic : ATOMIC LCURLY stmts RCURLY '''
	global wnum
	p[0] = atomicAst(p[3],wnum)
	wnum = wnum+1
	symtab.append(p[0].mkEntry())
	global mutexcount 
	mutexcount +=1

#assignment statement
def p_asgn(p): 
	'''asgn : varname EQLS expr SEMI
		| varname EQLS funcCall 
   		| varname INCR SEMI
		'''
	if len(p) is 4:
		exp = exprAst(p[1],"+",exprAst(1))
		p[0] = asgnAst(p[1],exp)
	else:
		p[0] = asgnAst(p[1],p[3])

#multiwriter block
def p_mwblock(p):
	''' mwblock : MW LCURLY decls RCURLY '''
	global symtab 
	for decl in p[3]:
		change_scope(symtab,decl.get_name(),'global')
		decl.set_scope('global')
	p[0] = mwAst(p[3])		

#list of declarations
def p_decls(p): 
	''' decls : decl decls
		  | sharedecl decls
		  | enumdecl decls
		  | empty
	'''
	dlist = []
	if len(p) is 3:
		dlist.append(p[1])
		dlist += p[2]
		p[0] = dlist 
	else:
		p[0] = []

#empty production
def p_empty(p):
	'empty :'
	pass

#declaration
def p_decl(p):
	'''decl : type varname SEMI
		| type varname EQLS val SEMI
	'''
	if len(p) is 4:	
		p[0] = declAst(p[1],p[2])
	else:
		p[0] = declAst(p[1],p[2],p[4])

	global symtab 	
	symtab.append(p[0])

def p_enumdecl(p):
	'''enumdecl : ENUM varname LCURLY varnames RCURLY varname EQLS varname SEMI
	'''
	print(p[4])
	p[0] = declAst(p[2],p[6],p[8],'local',p[4])

	global symtab 	
	symtab.append(p[0])


def p_varnames(p):
	'''varnames : varname COMMA varnames 
		    | varname 
	'''
	if len(p) is 4:
		l = [p[1]]
		l.extend(p[3])
		p[0]= l
	else:
		p[0] = [p[1]]

def p_sharedecl(p):
	'''sharedecl : SHARED type varname SEMI
		| SHARED type varname EQLS val SEMI
	'''
	if len(p) is 5:	
		p[0] = declAst(p[2],p[3],None,'self')
	else:
		p[0] = declAst(p[2],p[3],p[5],'self')

	global symtab 	
	symtab.append(p[0])

#value types
def p_val(p):
	'''val : INUM
	       | FNUM
	       | TRUE
	       | FALSE
	'''
	p[0] = exprAst(p[1]) 





precedence = ( ('left', 'PLUS', 'MINUS'),('left','TIMES','BY'),)

#expression
def p_expr(p):
	'''expr : val
		| varname
		| expr PLUS expr
		| expr MINUS expr
		| expr TIMES expr
		| expr BY expr
		| LPAREN expr RPAREN
        '''
	if len(p) is 2:
		p[0]  = exprAst(p[1])
	elif len(p) is 3:
		p[0] = exprAst(p[1],"+",exprAst(1))
	elif p[1] is not "(":
		p[0] = exprAst(p[1],p[2],p[3])
	else:
		 p[0] = p[2]
		 
#typenames
def p_type(p):
	'''type : INT 
		| FLOAT 
		| BOOL	
		| ITEMPOSITION
		'''
	p[0] = str(p[1])


#variable names
def p_varname(p):
	'''varname : LID 
		   | CID 
		   '''
	p[0] = str(p[1])


#error rule
def p_error(p):
	print("syntax error in input on line!",p.lineno,p.type)


parser = yacc.yacc()

def parse(infile):
	myinfile = open(infile,"r")
	s = myinfile.read() 
	result = parser.parse(s)
#	for decl in result.mwblock.decls:
#		print str(decl.name)
	myinfile.close()
	astfile = str(infile)+".ast"
	open(astfile,"w").write(str(result))
	javafile = str(infile)+".java"
	global symtab
	open(javafile,"w").write(str(result.codegen(symtab,0)))
	drawer = str(infile)+"Drawer.java"
	drawcode = "package edu.illinois.mitra.demo."+infile.lower()+";\n"	
	drawcode += "import java.awt.BasicStroke;\nimport java.awt.Color;\nimport java.awt.Graphics2D;\nimport java.awt.Stroke;\n\nimport edu.illinois.mitra.starl.interfaces.LogicThread;\nimport edu.illinois.mitra.starl.objects.ItemPosition;\nimport edu.illinois.mitra.starlSim.draw.Drawer;\n\npublic class "
	drawcode+= str(infile)+"Drawer extends Drawer  {\n\n     private Stroke stroke = new BasicStroke(8);        private Color selectColor = new Color(0,0,255,100);\n        @Override\n        public void draw(LogicThread lt, Graphics2D g) {\n                "+str(infile)+" app = ("+str(infile)+") lt;\n                g.setColor(Color.RED);\n                g.setColor(selectColor);\n                g.setStroke(stroke);\n                if(app.position != null){\n                "
	position = 0
	for decl in result.mwblock.decls:
		drawcode+='			g.drawString("'+str(decl.name)+'"+" = "+String.valueOf(app.'+str(decl.name)+"),app.position.x,app.position.y+"+str(position)+");\n"					
		position+=50
	drawcode+="\n                }\n        }\n\n}"
	maincode = "package edu.illinois.mitra.demo."+str(infile).lower()+";\nimport edu.illinois.mitra.starlSim.main.SimSettings;\nimport edu.illinois.mitra.starlSim.main.Simulation;\n\npublic class Main {\n        public static void main(String[] args) {\n                SimSettings.Builder settings = new SimSettings.Builder();\n                settings.N_IROBOTS(4);\n                settings.TIC_TIME_RATE(1.5);\n        settings.WAYPOINT_FILE("+'"four.wpt"'+");\n                settings.DRAW_WAYPOINTS(false);\n                settings.DRAW_WAYPOINT_NAMES(false);\n                settings.DRAWER(new "+str(infile)+"Drawer());\n\n                Simulation sim = new Simulation("+str(infile)+".class, settings.build());\n                sim.start();\n        }\n}"
	mainfile = "Main.java"	
	open(mainfile,"w").write(maincode)
	open(drawer,"w").write(drawcode)
import sys


s = sys.argv[1]
r = s
parse(s)
s += ".sym"
open(s,"w").write(str(printsym(symtab)))
