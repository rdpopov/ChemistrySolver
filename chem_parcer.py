#!/usr/bin/python3
import re #regex library
import chem_algo as libalgo
import sys
###	given a chemical reaction returns the compounds inside it, and which isde they are on
###	fixes the array begore that as well
def ret_compounds(reaction):
	tmp = reaction.replace(' ','').replace('>','')
	tmp = tmp.split('-')
	result = []
	pos = tmp[0].split('+')
	neg = tmp[1].split('+')
	for i in pos:
	    result.append([i.lstrip("0123456789"),1])
	for i in neg:
	    result.append([i.lstrip("0123456789"),-1])
	return result

###	removes brackets from bracketed formulas
def remove_br(string):
	return string.strip("1234567890").strip("()")

def extract(struct):
	comp = struct[0]
	mod = struct[1]
	chem_regex = "([A-Z][a-z]?[0-9]*)|([(].*[)][0-9]*)"
	num_regex = "[0-9]*\Z"
	x = re.findall(chem_regex, comp)
	for i in range(0, len(x)):
		x[i] = list(x[i])
		x[i] = list(filter(None, x[i]))
		mod = re.findall(num_regex, x[i][0])
		mod.append('1')
		mod = list(filter(None,mod))
		x[i] = [remove_br(x[i][0]), int(mod[0])]
	return x
	
###	checks if something is an element or a compound
###	returns true or false 
def check_if_element(Element):
	elem = 0
	for i in Element[0]:
		if "A" <= i <= "Z":
			elem += 1
	if elem >1:
		return False
	return True


class chemical:
	def __init__(self,chem,side):
		self._elements = dict()
		self._matser_compound =	[chem,1]
		self._side = side

	def desolve_compound(self):
		loc_que=[self._matser_compound]  
		for chem in loc_que:
			tmp=extract(chem)
			for member in tmp:
				if check_if_element(member):
					if member[0] in self._elements:
						self._elements[str(member[0])].append(int(member[1])*int(chem[1]))
					else:
						self._elements.update({member[0]:[int(member[1])*int(chem[1])]})
				else :
					loc_que.append(member)
		loc_que.pop(0)

		for chem in self._elements.keys():
			self._elements[chem] = sum(self._elements[chem])
		
	
class chemical_reaction:
	def __init__(self,reaction):
		self._compounds_list = ret_compounds(reaction)
		self._comp = []
		self._vector = [1] * len(self._compounds_list) 
		self._chem_set = set()
		for i in self._compounds_list:
			self._comp.append(chemical(i[0],i[1]))
		
		for i in self._comp:
			i.desolve_compound()
			for el in i._elements.keys():
				self._chem_set.add(el)
		self._matrix =[[] for i in range (len(self._chem_set))]
		
	def make_table(self):
		p =0
		for i in self._chem_set:
			for j in range (0,len(self._comp)):
				if i in self._comp[j]._elements.keys():
					self._matrix[p].append(self._comp[j]._elements[i]*self._comp[j]._side)
				else:
					self._matrix[p].append(0)
			p+=1
			
	def solve_eq(self):
		self._vector = libalgo.get_integer_kernel(self._matrix)
		tmp_format_string_list =[]
		added_arrow = False
		length = len(self._vector)
		for i in range(0,length):
			if added_arrow == False and 1<i < length and self._comp[i]._side == -1:
				added_arrow = True
				tmp_format_string_list.append('-> ')
			else: 
				if i!=0:
					tmp_format_string_list.append('+ ')
			
			tmp_format_string_list.append(str(self._vector[i]))
			tmp_format_string_list.append('*')
			tmp_format_string_list.append(self._compounds_list[i][0])
			tmp_format_string_list.append(' ')
			
		print (''.join(tmp_format_string_list))

#string="K2Cr2O7 + KI + H2SO4 -> Cr2(SO4)3 + I2 + H2O + K2SO4"
while 1:
	string = input("Reaction: ")	
	if string == "Exit":
		sys.exit(0)
	else:
		c=chemical_reaction(string)
		c.make_table()
		c.solve_eq()
		#print (c._matrix)
		#print(c._vector)
		#libalgo.matr_vect(c._matrix,c._vector)