#symtab entry
class symEntry(list):
	def __init__(self,dtype,name,scope):
		self.dtype = dtype
		self.name = name
		self.scope = scope


#set methods:
	def set_scope(self,scope):
		self.scope = scope


#get methods:
	def get_scope(self):
		return self.scope

	def get_dtype(self):
		return self.dtype

	def get_name(self):
		return self.name

#string representation:
	def __repr__(self):
		return str(self.name)+" : "+str(self.dtype)+" "+str(self.scope)

	def type(self):	
		return 'symentry'

#function for printing list of symtab entries(symtab)
def printsym(symtab):
	s = ""
	for entry in symtab:
		s+= str(entry.type())+str(entry)+"\n"
		
	return s
def hasEntry(symtab,name):
	for entry in symtab:
		if entry.get_name() == name:
			return True
	return False	
		
#finding entry in symtab, and changing scope
def change_scope(symtab,name,scope):
	for entry in symtab:
		if entry.get_name() == name:
			entry.set_scope(scope)

def get_scope(symtab,name):
	for entry in symtab:
		if entry.get_name() == name:
			return entry.get_scope()

def get_dtype(symtab,name):
	for entry in symtab:
		if entry.get_name() == name:
			return entry.get_dtype()
