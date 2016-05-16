from symtab import *
#destinaions.isEmpty()

class inputBlock(list):
	def __init__(self,var):
		self.var = var


	def codegen(self,symtab,indent):
			s= ""
			s+="\t"*(indent)+"for(ItemPosition i : gvh.gps.getWaypointPositions()){\n"
			s+="\t"*(indent+1)+str(self.var)+".put(i.getName(), i);\n"
			s+="\t"*(indent)+"}\n"
			return s
	def type(self):
		return "ib"
	
class dirAst(list):
	def __init__(self,lhs, op,rhs):
		self.lhs = lhs
		self.op = op
		self.rhs = rhs
	def codegen(self,symtab,indent):
		return "\t"*indent+str(self.lhs)+str(self.op)+str(self.rhs)+";\n"
class logAst(list):
	def __init__(self,var = ""):
		self.var = var 


	def codegen(self,symtab,indent):
		if str(self.var)=='':
			s = "\t"*(indent)+"System.out.println(gvh.log.getLog());\n"
		else: 
			s = "\t"*(indent)+'gvh.log.i("'+str(self.var).title() + '", "read");\n'

		return s
	def type(self):
		return "log" 

class mapAst(list):
	def __init__(self,var):
		self.var = var


	def codegen(self,symtab,indent):
		s = "\t"*(indent)+"final Map<String,ItemPosition> "+str(self.var)+" = new HashMap<String,ItemPosition>();\n"
		return s

	def type(self):
		return "map"



class msgAst(list):
	def __init__(self,var):
		self.var = var


	def codegen(self,symtab,indent):
		return '\t'*indent+'RobotMessage inform = new RobotMessage("ALL", name, ARRIVED_MSG,'+str(self.var)+'.getName());\n'+'\t'*indent+'gvh.comms.addOutgoingMessage(inform);\n'
class removeAst(object):
	def __init__(self,var=""):
		self.var = var

	def codegen(self,symtab,indent):
		s = "\t"*(indent)+"destinations.remove("+str(self.var)+".getName());\n"
		return s

class breakAst(object):
	def __init__(self):
		pass
	
	def codegen(self,symtab,indent):
		return "\t"*indent + "break;"

	def type(self):
		return "breakAst"

class returnAst(object):
	def __init__(self,value='null'):
		self.value = value 
	
	def codegen(self,symtab,indent):
		return "\t"*indent+ "return "+str(self.value)+";\n"

	def type(self):
		return "returnAst"
class destAst(object):
	def __init__(self,var):
		self.var = var

	def codegen(self,symtab,indent):
		return str(self.var)+".isEmpty()"



#declarations
class declAst(list):
	def __init__(self, dtype, name, value = None, scope = 'local',enumlist=[]):
		self.dtype = dtype
		self.name = name 
		self.value = value 
		self.scope = scope 
		self.enumlist = enumlist


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
		if len(self.enumlist) is not 0 :
			#print(self.name,self.enumlist)	
			s = "enum "+str(self.dtype) + " {"
			for name in self.enumlist:
				s+= str(name)
				s+= ','

			s.strip(',')
			s+= "};\n";
		 	s+=  "\t"*indent+str(self.dtype)+" "+str(self.name)+" = "+str(self.value)+";\n"
			return s
		elif self.value is not None:
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
		s+= "//if then else condition\n"
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

class flagAst(list):
	def __init__(self,val):
		self.val = val 

	def __repr__(self):
		return str(val)
	
	def codegen(self,symtab,indent):
		return "gvh.plat.reachAvoid."+str(self.val)


#expressions
class exprAst(list):
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

	def type(self):
		return "robotdecl"
#function
class funcAst(object):
	def __init__(self,name,params):
		self.name = name
		self.params = params

	def __repr__(self):
		s = str(self.name)+"("
		for p in range(len(self.params)):
			s+=str(self.params[p])
			if p == len(self.params) -1 :
				break;
			else:
				s+= ","
			print(p)
		s+= ")"
		return s
			
	def codegen(self,symtab,indent):
		return "\t"*(indent)+str(self)+";"

	def type(self):
		return "func"
#relational expressions :
class relAst(object):
	def __init__(self,relop,e1,e2):
		self.relop = relop
		self.e1 = e1
		self.e2 = e2

	def type(self):
		return "relast" 
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

	def type(self):
		return "codast" 
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
		s += "\t"*(indent+1)+"NumBots = gvh.gps.get_robot_Positions().getNumPositions();\n"
		s += "\t"*(indent+1)+"mutex.requestEntry(0);\n"
		s += "\t"*(indent+1)+"wait"+str(self.wnum)+" = true;\n"
		s+= "\t"*(indent)+"}\n\n"
		s+= "\t"*indent+" if(mutex.clearToEnter(0)) {\n"
		for stmt in self.stmts:
			s+= stmt.codegen(symtab,indent+1)+"\n"
		s+= "\t"*(indent+1)+"mutex.exit(0);\n"
		s+= "\t"*indent+"}\n"
		return s

 
	def type(self):
		return "atomicast" 
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
		s+= "//code for : "+str(self)+":"+putcodegen(str(self.name),self.expr,symtab)+"\n"
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
		return str(varname)+" = "+str(expr)+";\n" 


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
	def __init__(self,name,pre,eff,endflag = False):
		self.name = name
		self.pre = pre
		self.eff = eff
		self.endflag = endflag
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
						
			if stmt.type() == "breakAst" or stmt.type() == "returnAst" :
				self.endflag = True;	
			if stmt.type() == "ib":
				pass
			else:
				s+= stmt.codegen(symtab,indent+1)+"\n"
		if not self.endflag:
			s+= "\t"*(indent+1)+"continue;\n"
		s+= "\t"*indent+"}\n"
		return s

	def get_ib(self):
		libs = []
		for stmt in self.eff :
			if stmt.type() == "ib":
				libs.append(stmt)
		return libs 

	def type(self):
		return "event"
class getAst(object):
	def __init__(self,name):
		self.name = name 

	def codegen(self,symtab,indent):
		s = "\t"*indent + str(self.name) +" = gvh.gps.getMyPosition();\n"
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

	def get_ib(self):
		libs = []
		for event in self.events:
			if event.type() == "event":
				libs.extend(event.get_ib())
		return libs
		
#code generation
	def codegen(self,symtab,indent):
		s = "\t"*(indent)+"while(true) {\n"
		s+= "\t"*(indent+1)+"sleep(100);\n"
		s+= "\t"*(indent+1)+"if(gvh.plat.model instanceof Model_quadcopter){\n"
		s+= "\t"*(indent+2)+'gvh.log.i("WIND", ((Model_quadcopter)gvh.plat.model).windxNoise + " " +  ((Model_quadcopter)gvh.plat.model).windyNoise);\n'
		s+="\t"*(indent+1)+"}\n"
		amotionflag = False
		for entry in symtab :
			if entry.get_dtype() == 'ItemPosition':
				amotionflag = True	
		for event in self.events:
			s+= event.codegen(symtab,indent+1)+"\n\n"
		s+= "\t"*(indent)+"}\n"
		return s		


class raAst(object):
	def __init__(self,target,unsafe):
		self.target = target
		self.unsafe = unsafe
	
	def codegen(self,symtab,indent):
		s = ""
		s+= "\t"*(indent)+"gvh.plat.reachAvoid.doReachAvoid(gvh.gps.getMyPosition(),"+str(self.target)+","+str(self.unsafe)+");\n"
		s+= "\t"*(indent)+"kdTree = gvh.plat.reachAvoid.kdTree;\n"
		s+= "\t"*(indent)+'gvh.log.i("DoReachAvoid",'+ str(self.target)+'.x + " " +'+str(self.target)+'.y);\n'
		s+= '\t'*(indent)+'''doReachavoidCalls.update(new ItemPosition(name + "'s " + "doReachAvoid Call to destination: " +'''+str(self.target)+'.name, gvh.gps.getMyPosition().x,gvh.gps.getMyPosition().y));\n'
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
		motionflag = False

		obslist = []
		for entry in symtab :
			if entry.get_dtype() == 'atomic':
				atomicflag = True
			if entry.get_name() == 'robotIndex':
				robotflag = True
		
			if entry.get_dtype() == 'ObstacleList':
				obsflag = True
				#print("hello"+entry.get_name())	
				obslist.append(entry.get_name());
			if entry.get_dtype() == 'ItemPosition':
				motionflag = True	
		if atomicflag == True:
			symtab.append(symEntry('MutualExclusion','mutex','local'))	
			symtab.append(symEntry('int','Numbots','local'))	

		s= initcode(self.name)
		s+= "\n\npublic class "+str(self.name)+"App extends LogicThread {\n\n"
		if self.mwblock.get_decls() is not []:
			s+= "\t"*(indent+1)+"private DSM dsm;\n"
		s+= (self.mwblock).codegen(symtab,indent+1)
		if atomicflag:
			s+= "\t"*(indent+1)+"private MutualExclusion mutex;\n"
			s+= "\t"*(indent+1)+"private int NumBots = 0;\n"
		if robotflag:
			s+= "\t"*(indent+1)+"int robotIndex = 0;\n"
	
		if motionflag:
			s+="\t"*(indent+1)+'private static final boolean RANDOM_DESTINATION = false;\n'
			s+="\t"*(indent+1)+'public static final int ARRIVED_MSG = 22;\n'
			s+="\t"*(indent+1)+'PositionList<ItemPosition> destinationsHistory = new PositionList<ItemPosition>();\n'
			s+= "\t"*(indent+1)+'PositionList<ItemPosition> doReachavoidCalls = new PositionList<ItemPosition>();\n'
			s+="\t"*(indent+1)+'public RRTNode kdTree;\n'	
			s+="\t"*(indent+1)+'public ItemPosition position;\n'	
		for decl in self.decls:
			s+= "\t"*(indent+1)+"public "+decl.codegen(symtab,indent+1)+"\n"

		s+= "\t"*(indent+1)+"public "+str(self.name)+"App(GlobalVarHolder gvh) {\n"
		s+= "\t"*(indent+2)+"super(gvh);\n"
		if robotflag:
			s+="\t"*(indent+2)+'robotIndex = Integer.parseInt(name.replaceAll("[^0-9]",""));\n'
		if atomicflag:
			s+= "\t"*(indent+2)+'mutex = new GroupSetMutex(gvh,0);\n'

		s+= "\t"*(indent+2)+"dsm = new DSMMultipleAttr(gvh);\n"
		if motionflag:
			s+="\t"*(indent+2)+"MotionParameters.Builder settings = new MotionParameters.Builder();\n"
			s+="\t"*(indent+2)+"settings.COLAVOID_MODE(COLAVOID_MODE_TYPE.USE_COLAVOID);\n"
			s+="\t"*(indent+2)+"MotionParameters param = settings.build();\n"
			s+="\t"*(indent+2)+"gvh.plat.moat.setParameters(param);\n"
			ibs = self.initblock.get_ib()
			for ib in ibs:
				s+= ib.codegen(symtab,indent+2)
			s+="\t"*(indent+2)+"gvh.comms.addMsgListener(this,ARRIVED_MSG);\n"
			for obs in obslist:
				s+= "\t"*(indent+2)+str(obs)+"= gvh.gps.getObspointPositions();\n"
			
		s+= "\t"*(indent+1)+"}\n"
	
		s+= "\t"*(indent+2)+"@Override\n"
		s+= "\t"*(indent+2)+"public List<Object> callStarL() {\n"
		s+= createDSMs(self.mwblock,indent+3)
		s+= "\t"*(indent+3)+"position = gvh.gps.getMyPosition();\n"
		s+= self.initblock.codegen(symtab,indent+3)	
		s+= "\t"*(indent+2)+"}\n"
		s+= endcode(indent+1,"Stage.PICK",motionflag)
		s+= "}"
		#print obslist
		return s 
		
def initcode(name):
	s = "package edu.illinois.mitra.demo."+str(name).lower()+";\n\n"
	
	s+="import java.util.HashMap;\n"
	s+="import java.util.Map;\n"
	s+="import java.util.Random;\n"
	s+= "import java.util.List;\n\n"
	s+= "import edu.illinois.mitra.starl.comms.RobotMessage;\n"
	s+= "import edu.illinois.mitra.starl.functions.DSMMultipleAttr;\n"
	s+= "import edu.illinois.mitra.starl.functions.SingleHopMutualExclusion;\n"
	s+= "import edu.illinois.mitra.starl.functions.GroupSetMutex;\n"
	s+= "import edu.illinois.mitra.starl.gvh.GlobalVarHolder;\n"
	s+= "import edu.illinois.mitra.starl.interfaces.DSM;\n"
	s+= "import edu.illinois.mitra.starl.interfaces.LogicThread;\n"
	s+="import edu.illinois.mitra.starl.models.Model_quadcopter;\n"
	s+="import edu.illinois.mitra.starl.motion.RRTNode;\n"
	s+="import edu.illinois.mitra.starl.motion.MotionParameters;\n"
	s+= "import edu.illinois.mitra.starl.motion.MotionParameters.COLAVOID_MODE_TYPE;\n"
	s+= "import edu.illinois.mitra.starl.interfaces.MutualExclusion;\n"
	s+= "import edu.illinois.mitra.starl.objects.ItemPosition;\n"
	s+="import edu.illinois.mitra.starl.objects.ObstacleList;\n"
	s+="import edu.illinois.mitra.starl.objects.PositionList;\n"
	return s 



def endcode(indent,stage,motionflag):
	if not motionflag :
		return "\t"*indent+"@Override\n"+"\t"*indent+"protected void receive(RobotMessage m) {\n"+"\t"*indent+"}\n"
	else :
		s =  "\t"*indent+"@Override\n"+"\t"*indent+"protected void receive(RobotMessage m) {\n"
		s+= "\t"*indent+"String posName = m.getContents(0);\n"
		s+= "\t"*indent+"if(destinations.containsKey(posName))\n"
		s+= "\t"*indent+"		destinations.remove(posName);\n"
	
		s+= "\t"*indent+"if(currentDestination.getName().equals(posName)) {\n"
		s+= "\t"*indent+"	//	gvh.plat.moat.cancel();\n"
		s+= "\t"*indent+"		gvh.plat.reachAvoid.cancel();\n"
		s+= "\t"*indent+"		stage = "+str(stage)+ ";\n"
		s+= "\t"*indent+"	}\n"
		s+= 	"\t"*indent+"}\n"
		s+= "private static final Random rand = new Random();\n"

		s+="\t"*indent+'@SuppressWarnings("unchecked")\n'
		s+="\t"*indent+"private <X, T> T getRandomElement(Map<X, T> map) {\n "
		s+="\t"*indent+"	if(RANDOM_DESTINATION)\n"
		s+="\t"*indent+"		return (T) map.values().toArray()[rand.nextInt(map.size())];\n"
		s+="\t"*indent+"	else\n"
		s+="\t"*indent+"		return (T) map.values().toArray()[0];\n"
		s+="\t"*indent+"}\n"

		return s 	
def createDSMs(mwblock,indent):
	s = ""
	decls = mwblock.get_decls()
	for decl in decls:
		if (decl.type()) == "map":
			pass
		else: 
			s+= "\t"*(indent)+"dsm.createMW("+'"'+str(decl.get_name())+'", 0);\n'
	return s
