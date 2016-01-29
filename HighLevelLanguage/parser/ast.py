from symtab import *

#declarations
class declAst(list):
	def __init__(self, dtype, name, value = None, scope = 'local'):
		self.dtype = dtype
		self.name = name 
		self.value = value 
		self.scope = scope 


#set methods for attributes

	def set_scope(self,scope):
		self.scope = scope 

#get methods for attributes
	def get_dtype(self):
		return self.dtype

	
	def get_name(self):
		return self.name	

	def get_value(self):
		return self.value	
	
	def get_scope(self):
		return self.scope	

#string representation

	def __repr__(self):
		return str(self.dtype)+" , "+str(self.name)+" , "+str(self.value)+" , "+str(self.scope)


#code generation
	def codegen(self,symtab,indent):	
		if self.value is not None:
			return str(self.dtype)+" "+str(self.name)+" = "+str(self.value)+";"
		else: 
			return str(self.dtype)+" "+str(self.name)+";"
#checking ast type
	def type(self):
		return 'decl'


class ifAst(object):
	def __init__(self,condition,ifblock,elseblock):
		self.condition = condition
		self.ifblock = ifblock
		self.elseblock = elseblock 

	def type(self):
		return 'if' 

#code generation
	def codegen(self,symtab,indent):
		s = ""
		if type(self.condition) is str:
			s+= "\t"*indent+"if("+exprAst(self.condition).codegen(symtab,indent)+") {\n"
		else:
			s+= "\t"*indent+"if("+(self.condition).codegen(symtab,indent)+") {\n"
		for stmt in self.ifblock :
			s+= stmt.codegen(symtab,indent+1)+"\n"
		s+= "\t"*indent+"}\n"
		s+= "\t"*indent+"else {\n"
		for stmt in self.elseblock :
			s+= stmt.codegen(symtab,indent+1)+"\n"
		s+= "\t"*indent+"}\n"
		return s
		
#function for making symtab entry from declaration
def mkentry(decl):
	return symEntry(decl.get_dtype(),decl.get_name(),decl.get_scope())

#expressions
class exprAst(object):
	def __init__(self,lvalue,op = None,rvalue = None):
		self.lvalue = lvalue
		self.op = op
		self.rvalue = rvalue 



#set methods for attributes:
	
#get methods for attributes 
	def get_lvalue(self):
		return self.lvalue


	def get_rvalue(self):
		return self.rvalue

	def get_op(self):
		return self.op


#string representation
	def __repr__(self):
		if self.op is not None:
			return str(self.lvalue)+" "+str(self.op)+" "+str(self.rvalue)
		else :
			return str(self.lvalue)

#codegeneeration
	def codegen(self,symtab,indent):
		if self.op is None and hasEntry(symtab,str(self.lvalue)) :
			if get_scope(symtab,str(self.lvalue)) is 'local':
				return str(self.lvalue)
			elif get_scope(symtab,str(self.lvalue)) is 'self':
				return "Integer.parseInt(dsm.get("+'"'+str(self.lvalue)+'",""))'
			elif get_scope(symtab,str(self.lvalue)) is 'global':
				return "Integer.parseInt(dsm.get("+'"'+str(self.lvalue)+'",""))'

		elif self.op is None and not hasEntry(symtab,str(self.lvalue)):
			return str(self.lvalue)
		else :
			return self.lvalue.codegen(symtab,indent)+" "+str(self.op)+" "+self.rvalue.codegen(symtab,indent)

#getting all variable names :
	def getvars(self):
		vlist = []
		if self.op is None:
			vlist.append(self.lvalue)
		else:
			vlist+= self.lvalue.getvars()
			vlist+= self.rvalue.getvars()
		return vlist
#chking ast type
	def type(self):
		if self.op is not None:
			return 'expr'
		else:
			return 'numeric'


class robotDecl(object):
	def codegen(self,symtab,indent):
		return ""
#function
class funcAst(object):
	def __init__(self,name,params = None):
		self.name = name
		self.params = params

	def __repr__(self):
		return str(self.name)+"()"
	
	def codegen(self,symtab,indent):
		return "\t"*(indent)+str(self)+";"

#relational expressions :
class relAst(object):
	def __init__(self,relop,e1,e2):
		self.relop = relop
		self.e1 = e1
		self.e2 = e2

#string representation
	def __repr__(self):
		return str(self.e1)+" "+str(self.relop)+" "+str(self.e2)

	def codegen(self,symtab,indent):
		return str(self.e1.codegen(symtab,indent))+" "+str(self.relop)+str(self.e2.codegen(symtab,indent))
#conditional expressions:
class condAst(object):
	def __init__(self,condop,e1,e2 = None):
		self.condop = condop
		self.e1 = e1
		self.e2 = e2


#string representation

	def __repr__(self):
		if self.e2 is not None:
			return str(self.e1)+" "+str(self.condop)+" "+str(self.e2)
		else:
			return str(self.condop)+str(self.e1)


#code generation:
	def codegen(self,symtab,indent):
		if self.e2 is not None:
			return self.e1.codegen(symtab,indent)+" "+str(self.condop)+self.e2.codegen(symtab,indent)
		else:
			return str(self.condop)+"("+self.e1.codegen(symtab,indent)+")"

#if then else statements
#atomic statements
class atomicAst(object):
	def __init__(self,stmts,wnum):
		self.stmts = stmts
		self.wnum = wnum
	
#string representation 
	def __repr__(self):
		s = "atomic :\n"
		for stmt in self.stmts:
			s+= str(stmt)+"\n"
		return s 

	def mkEntry(self):
		out = []
		for stmt in self.stmts:
			if stmt.type() == 'asgn':
				out.append(stmt.get_name())
		return symEntry('atomic',out,'local')


#code generation
	def codegen(self,symtab,indent):
		s= ""
		s += "\t"*indent+"if(!wait"+str(self.wnum)+"){\n"
		s += "\t"*(indent+1)+"NumBots = gvh.gps.getPositions().getNumPositions();\n"
		s += "\t"*(indent+1)+"mutex.requestEntry(0);\n"
		s += "\t"*(indent+1)+"wait"+str(self.wnum)+" = true;\n"
		s+= "\t"*(indent)+"}\n\n"
		s+= "\t"*indent+" if(mutex.clearToEnter(0)) {\n"
		for stmt in self.stmts:
			s+= stmt.codegen(symtab,indent+1)+"\n"
		s+= "\t"*(indent+1)+"mutex.exit(0);\n"
		s+= "\t"*indent+"}\n"
		return s 
#assignment statements : 
class asgnAst(object):
	def __init__(self,name,expr):
		self.name = name
		self.expr = expr

	def get_name(self):
		return self.name
#string representation
	def __repr__(self):
		return str(self.name)+" = "+str(self.expr)
	
#codegeneration
	def codegen(self,symtab,indent):
		s = ""
		for var in self.expr.getvars():
			s+= "\t"*indent+getcodegen(str(var),symtab)	
		return s+"\n"+"\t"*indent+putcodegen(str(self.name),self.expr,symtab)

	def type(self):
		return 'asgn'
def getcodegen(varname,symtab):
	if get_scope(symtab,varname) is 'local':
		return ""
	elif get_scope(symtab,varname) is 'self':
		return str(varname)+" = "+"Integer.parseInt(dsm.get("+'"'+str(varname)+'",""));\n'
	elif get_scope(symtab,varname) is 'global':
		return str(varname)+" = "+"Integer.parseInt(dsm.get("+'"'+str(varname)+'","*"));\n'
	else:
		return ""	

def putcodegen(varname,expr,symtab):
	if get_scope(symtab,varname) is 'local':
		return str(varname)+" = "+str(expr)+";\n"
	elif get_scope(symtab,varname) is 'self':
		return "dsm.put("+'"'+str(varname)+'","",'+str(expr)+');'
	elif get_scope(symtab,varname) is 'global' :
		return "dsm.put("+'"'+str(varname)+'","*",'+str(expr)+');'
	else:
		return ""


#mwblock
class mwAst(object):
	def __init__(self,decls):
		self.decls = decls

#get methods 
	def get_decls(self):
		return self.decls
#string representation
	def __repr__(self):
		s = "MW :\n" 
		for decl in self.decls:
			s+= str(decl)+"\n"
		return s
#code generation
	def codegen(self,symtab,indent):
		s = ""
		for decl in self.decls:
			s+= "\t"*indent+"public "+decl.codegen(symtab,indent)+"\n"
		return s
#event class
class eventAst(object):
	def __init__(self,name,pre,eff):
		self.name = name
		self.pre = pre
		self.eff = eff

#string representation
	def __repr__(self):
		s = "event "+str(self.name)+":\n"
		s += "pre:"
		s += str(self.pre)+"\n"
		s += "eff:\n"
		for stmt in self.eff:
			s+= str(stmt)+"\n"

		return s 

	def codegen(self,symtab,indent):
		s = ""
		if type(self.pre) is str:
			s+= "\t"*indent+"if("+exprAst(self.pre).codegen(symtab,indent)+") {\n"
		else:
			s+= "\t"*indent+"if("+(self.pre).codegen(symtab,indent)+") {\n"
		for stmt in self.eff :
			s+= stmt.codegen(symtab,indent+1)+"\n"
		s+= "\t"*(indent+1)+"continue;\n"
		s+= "\t"*indent+"}\n"
		return s



#initblock
class initAst(object):
	def __init__(self,events):
		self.events = events
	

	def __repr__(self):
		s = "Init:\n"
		for event in self.events:
			s+= str(event)+"\n"

		return s 


#code generation
	def codegen(self,symtab,indent):
		s = "\t"*(indent)+"while(true) {\n"
		s+= "\t"*(indent+1)+"sleep(100);\n"
		for event in self.events:
			s+= event.codegen(symtab,indent+1)+"\n\n"
		s+= "\t"*(indent)+"}\n"
		return s		



#program
class pgmAst(object):
	def __init__(self,name,mwblock,decls,initblock):
		self.name = name
		self.mwblock = mwblock 	
		self.decls = decls
		self.initblock = initblock

	def __repr__(self):
		s = "PGM:\n"
		s+= str(self.mwblock)
		s+= "LocalDecls:\n"
		for decl in self.decls:
			s+=str(decl)+"\n"	
		s+= str(self.initblock)
		return s

#code generation 
	def codegen(self,symtab,indent):
		atomicflag = False;
		robotflag = False;
		globalflag = False


		for entry in symtab :
			if entry.get_dtype() == 'atomic':
				atomicflag = True
			if entry.get_name() == 'robotIndex':
				robotflag = True
		
		if atomicflag == True:
			symtab.append(symEntry('MutualExclusion','mutex','local'))	
			symtab.append(symEntry('int','Numbots','local'))	

		s= initcode(self.name)
		s+= "\n\npublic class "+str(self.name)+" extends LogicThread {\n\n"
		if self.mwblock.get_decls() is not []:
			s+= "\t"*(indent+1)+"private DSM dsm;\n"
		s+= (self.mwblock).codegen(symtab,indent+1)
		if atomicflag:
			s+= "\t"*(indent+1)+"private MutualExclusion mutex;\n"
			s+= "\t"*(indent+1)+"private int NumBots = 0;\n"
		if robotflag:
			s+= "\t"*(indent+1)+"int robotIndex = 0;\n"
		for decl in self.decls:
			s+= "\t"*(indent+1)+"public "+decl.codegen(symtab,indent+1)+"\n"

		s+= "\t"*(indent+1)+"public ItemPosition position;\n"
		s+= "\t"*(indent+1)+"public "+str(self.name)+"(GlobalVarHolder gvh) {\n"
		s+= "\t"*(indent+2)+"super(gvh);\n"
		if robotflag:
			s+="\t"*(indent+2)+"robotIndex = Integer.parseInt(name.substring(3,name.length()));\n"
		if atomicflag:
			s+= "\t"*(indent+2)+'mutex = new SingleHopMutualExclusion(1,gvh,"bot0");\n'
		s+= "\t"*(indent+2)+"dsm = new DSMMultipleAttr(gvh);\n"
		s+= "\t"*(indent+1)+"}\n"
	
		s+= "\t"*(indent+2)+"@Override\n"
		s+= "\t"*(indent+2)+"public List<Object> callStarL() {\n"
		s+= createDSMs(self.mwblock,indent+3)
		s+= "\t"*(indent+3)+"position = gvh.gps.getMyPosition();\n"
		s+= self.initblock.codegen(symtab,indent+3)	
		s+= "\t"*(indent+2)+"}\n"
		s+= endcode(indent+1)
		s+= "}"
		return s 
		
def initcode(name):
	s = "package edu.illinois.mitra.demo."+str(name).lower()+";\n\n"
	s+= "import java.util.List;\n\n"
	s+= "import edu.illinois.mitra.starl.comms.RobotMessage;\n"
	s+= "import edu.illinois.mitra.starl.functions.DSMMultipleAttr;\n"
	s+= "import edu.illinois.mitra.starl.functions.SingleHopMutualExclusion;\n"
	s+= "import edu.illinois.mitra.starl.gvh.GlobalVarHolder;\n"
	s+= "import edu.illinois.mitra.starl.interfaces.DSM;\n"
	s+= "import edu.illinois.mitra.starl.interfaces.LogicThread;\n"
	s+= "import edu.illinois.mitra.starl.interfaces.MutualExclusion;\n"
	s+= "import edu.illinois.mitra.starl.objects.ItemPosition;\n"

	return s 

def endcode(indent):
	return "\t"*indent+"@Override\n"+"\t"*indent+"protected void receive(RobotMessage m) {\n"+"\t"*indent+"}\n"

def createDSMs(mwblock,indent):
	s = ""
	decls = mwblock.get_decls()
	for decl in decls:
		s+= "\t"*(indent)+"dsm.createMW("+'"'+str(decl.get_name())+'", 0);\n'
	return s
