from os import system,name,listdir,path

def files(cwd,ext):
	'''
	generator function that takes a path object as argument and yields the files in
	the directory that have the ext, a string object given as an argument, and
	yields matches to that extension
	'''
	directory = listdir()
	for file in directory:
		_, ext1 = file.split(".")
		if ext1 == ext:
			yield file
			
def pause():
	'''function to allow user to review screen before continuing'''
	_ = input('\n\nPress Enter to continue')

def dict_to_list(dict):
	'''
	function takes a dictionary as argument and returns the dictionary as a list
	'''
	return dict.items()
	
def list_to_dict(item_list,key_list=[]):
	'''
	item_list: list containg the items to be included in the dictionary
	key_list: list, default is a blank list to create a range of numbers 1 to 
	(n+1) as keys
	'''
	
	len_keys = len(key_list)
	n=len(item_list)
	if len_keys == 0:
		for k in range(n):
			key_list.append(str(k+1))
	dict={1:"test"}
	for x in range(n):
		dict[key_list[x]]=item_list[x]
	del dict[1]
	return dict

def clear(): 
	'''	define clear function to clear screen'''
    # for windows
	if name == 'nt': 
		_ = system('cls')

	else:# for mac and linux
		_ = system('clear') 

def print_heading(menu_name):
	'''
	function to print headings for menus
	takes argument menu_name for menu title
	'''
	clear()
	print("*"*90)
	print("*{}*".format(" "*88))
	length = 88 - len(menu_name)
	if length%2 == 0:
		sp = int(length/2)
		space = " "*sp
		print("*{}{}{}*".format(space,menu_name,space))
	else:
		sp1 = int(length/2)
		sp2 = length - sp1
		space1 = " " * sp1
		space2 = " " * sp2
		print("*{}{}{}*".format(space1,menu_name,space2))
	print("*{}*".format(" "*88))
	print("*"*90)
	print("\n\n")
	
def set_up_dict(filename,keys=False):
	'''function to set up dictionary from a file'''
	with open(filename, 'r') as file:
		mystr=file.readline().strip()
		mylist=mystr.split(',')
	if keys == False:
		d=list_to_dict(mylist)
	else:
		d=list_to_dict(mylist,keys)
	return d

def get_input(mylist):
	''' 
	function to get multiple inputs from user, takes list of questions as input 
	and returns list of answers
	'''
	list_out = []
	for item in mylist:
		item_in = input(item)
		list_out.append(item_in)
	return list_out

def check_for_file(filepath):
	if not path.exists(filepath):
		file = open(filepath, 'w')
		file.close()