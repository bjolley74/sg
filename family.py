import logging
##logger set up
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(name)s: %(message)s')
file_handler = logging.FileHandler('babysitting.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
from datetime import datetime as dt
from mylib import print_heading, pause, get_input, clear

logger.info("family.py run as {}".format(__name__))
class Family:
	'''
	Class for families that are in small group
	
	properties:
		.last - families last name
		.filename - csv filename
		.html - html last name
		.table - nested list read from the csv table
		.money_in - list of the money in column of table
		.money_out - list of the money out column of table
		.sum_money_in - sum of elements in money_in list
		.sum_money_out - sum of elements in money_out_list
		.balance - difference of sum_money_in and sum_money_out
	'''
	
	def __init__(self,last_name):
		self.last = last_name
		self.filename = self.last + ".csv"
		self.html = self.last + ".html"
		self.table = self.open_csv()
	
	@property
	def money_in(self):
		logger.debug("entered Family.money_in")
		mon_in=[]
		count = 0
		for item in self.table:
			if count == 0:
				count += 1
				logger.debug("{} thrown out".format(item[1]))
			else:
				mon_in.append(float(item[1]))
		logger.debug("exited money_out")
		return mon_in
		
	@property
	def money_out(self):
		logger.debug("entered Family.money_out")
		out = []
		count = 0
		for item in self.table:
			if count == 0:
				count += 1
				logger.debug("{} thrown out".format(item[2]))
			else:
				out.append(float(item[2]))
		logger.debug("exited money_out")
		return out
		
	@property
	def sum_money_in(self):
		#calculate sum of money_in
		logger.debug("entered sum_money_in")
		sum_money_in = 0
		len_in = len(self.money_in)
		for x in range(len_in):
			sum_money_in += self.money_in[x]
		logger.debug("exited sum_money_in")
		return sum_money_in
			
	@property
	def sum_money_out(self):
		#calculate sum of money_out
		logger.debug("entered sum_money_out")
		sum_money_out = 0
		len_out = len(self.money_out)
		for x in range(len_out):
			sum_money_out += self.money_out[x]
		logger.debug("exited sum_money_out")
		return sum_money_out
			
	@property
	def balance(self):
		logger.debug("Entered Family.blance")
		balance = self.sum_money_in - self.sum_money_out
		logger.debug("Exited Family.blance")
		return balance
		
	def print_table(self):
		logger.debug("Entered Family.print_table()")
		print_heading("{} Family Table".format(self.last))
		for line in self.table:
			print("{:12}{:10}{:10}".format(line[0],line[1],line[2]))
		pause()
		logger.debug("Exited Family.print_table()")
	
	@property
	def amt_owed(self):
		'''
		amt_owed is a class function included for future use
		'''
		
		logger.debug("Entered Family.amt_owed()")
		amount=10
		logger.debug("Exited Family.amt_owed()")
		return amount
	
	def open_csv(self, opt='r'):
		logger.debug("Entered open_csv")
		logger.info("last name is {}".format(self.last))
		file=open(self.filename,opt)
		l=[]
		line=file.readline().strip()
		while line:
			line2=line.split(',')
			l.append(line2)
			line=file.readline().strip()
		file.close()
		logger.debug("exited open_csv")
		return l

	def save_html(self):
		logger.debug("entering Family.save_html")
		time = dt.now()

		table = self.table
		logger.info(f"writing {self.html}")
		html_file = open(self.html,"w")
		html_file.write("<html>\n")
		html_file.write("\t<head>\n")
		html_file.write(f"\t\t<title>{self.last} Table</title>\n")
		html_file.write("\t\t<link href='main.css' rel='stylesheet' type='text/css' />\n")
		html_file.write("\t</head>\n")
		html_file.write("\t<body>\n")
		html_file.write(f"\t\t<h1>{self.last} Family Table</h1>\n")
		html_file.write('\t\t<table class="center">\n')
		count=0
		for i in table:
			list_len = len(i)
			d=0
			if list_len == 3:
				if count == 0:
					a,b,c = i[0],i[1],i[2]
					html_file.write('\t\t\t<thead>\n')
					html_file.write("\t\t\t\t<tr>\n")
					html_file.write('\t\t\t\t\t<th>{:12}</th>\n'.format(a))
					html_file.write('\t\t\t\t\t<th>{:10}</th>\n'.format(b))
					html_file.write('\t\t\t\t\t<th>{:10}</th>\n'.format(c))
					html_file.write('\t\t\t\t\t<th>{:10}</th>\n'.format("Balance"))
					html_file.write('\t\t\t\t</tr>\n')
					html_file.write('\t\t\t</thead>\n')
					count += 1
				else:
					a,b,c = i[0],i[1],i[2]
					d += float(b)-float(c)
					if count == 1:
						html_file.write('\t\t\t<tbody>\n')
					html_file.write('\t\t\t\t<tr>\n')
					html_file.write('\t\t\t\t\t<td>{:12}</td>\n'.format(a))
					html_file.write('\t\t\t\t\t<td>{:10}</td>\n'.format(b))
					html_file.write('\t\t\t\t\t<td>{:10}</td>\n'.format(c))
					html_file.write('\t\t\t\t\t<td>{:10}</td>\n'.format(d))
					html_file.write('\t\t\t\t</tr>\n')
					count += 1
			else:
				logger.warning(f"list length of {list_len} is incorrect")
		html_file.write('\t\t\t</tbody>\n')
		html_file.write("\t\t</table>\n")
		html_file.write("\t\t<br>\n\t\t<br>\n")
		html_file.write('\t\t<footer>\n')
		html_file.write(f"\t\t\t{time}\n")
		html_file.write("\t\t</footer>\n\t</body>\n</html>\n")
		logger.debug("exiting Family.save_html")
		return "HTML File Saved"
	
	def save_table(self,table,filename):
		with open(filename,"w") as csvfile:
			print("\tsaving file")
			for line in table:
				csvfile.write(",".join(line))
				csvfile.write("\n")
			
	def email_html(self):
		#to do:
		#  create function to email table to family
		logger.debug("Entered email_html")
		print()
		print("email function in progress")
		pause()
		logger.debug("exiting email_html")
	
	def update_table(self):
		'''
		updates family.table
		
		Takes no arguments. Function to get user input and save it to the family
		table. Saves the table in CSV format to Family.filename
		'''
		
		#to do:
		#  provide function to update any mistakes in table
		logger.debug("Entered update_table")
		#print heading
		menu_name="update {} family table".format(self.last)
		print_heading(menu_name)
		#set up list of questions
		q = [
			"Enter date (mm/dd/yyyy): ",
			"Enter Money In(24.00): ",
			"Enter Money Out(24.00): "]
		#get list of answers from user
		print()
		answers = get_input(q) 
		
		#create copy of self.table
		table = self.table
		
		#print resulting table and get user ok
		print()
		print("\t\tHere is updated table:")
		for line in table:
			print("\t{:12}{:10}{:10}".format(line[0],line[1],line[2]))
		print("\t{:12}{:10}{:10}".format(answers[0],answers[1],answers[2]))
		print()
		ok = input("\t\tDoes table look ok? (y/n) ")
		checkok = ok.lower()
		if checkok[0:1] == "y":
			print("\t\tSaving table")
			#append table with list of answers
			table.append(answers)
			self.save_table(table,self.filename)
			logger.debug("table: {}".format(table))
			logger.info("table saved")
		else:
			print("OK, disgarding changes")
			logger.info("changes not saved due to user choice")
		pause()
		self.save_html()
		logger.debug("Exiting update_table")

def save_fam(fam):
	'''
	Saves family list
	
	Takes list as input and saves it to a file called families.txt
	'''
	
	logger.debug("Entered save_fam")
	string = ",".join(fam)
	with open("families.txt",'w') as f:
		f.write(string)
	logger.debug("Family list saved")
	
	
def get_fam_list():
	'''
		returns a list of families from text file
		takes argument of filename
	'''
	
	logger.debug("Entered get_fam_list")
	with open("families.txt","r") as f:
		line=f.readline().strip()
		fam_list = line.split(',')
	logger.debug("Exiting get_fam_list")
	return fam_list

def create_fam():
	'''	get input and create instance of family class'''
	
	logger.debug("Entered create_fam")
	print_heading("Add Family")
	while True:
		clear()
		fam_list = get_fam_list()
		start_len = len(fam_list)
		last = input("Enter family last name: ")
		if last in fam_list:
			logger.error("{} already in family list".format(last))
		else:
			fam_list.append(last)
			fam_list.sort()
			save_fam(fam_list)
			logger.info("{} saved to families.txt".format(last))
		end_len = len(fam_list)
		if start_len >= end_len:
			logger.error(
						"start length of {} >= end length of {}".format(
																start_len,
																end_len
																)
						)
		else:
			filename = last + ".csv"
			with open(filename,"w+") as f:
				f.write("Date,Money_in,Money_out")
			again = input("Enter another family? (y/n) ")
			if again.lower() == "y":
				continue
			elif again.lower() == "n":
				break
			else:
				logger.error("{} invalid menu selection".format(again))
	
	
		
def remove_family():
	'''
	Allows user to remove family from family list
	
	No arguments - displays families from families.txt along with a number
	asks for input from user on which number to remove and then pops that 
	family from list and resaves the new family list. Saves popped family to 
	removed_fams.dat for later removal of associated files (CSV,HTML,ETC)
	'''
	
	logger.debug("Entered remove_family")
	print_heading("Delete Family")
	fam_list = get_fam_list()
	list_len = len(fam_list)
	print()
	for i in range(list_len):
		print("{} - {}".format(i,fam_list[i]))
	print()
	remove = int(input("Enter number of family to remove: "))
	fam_2_remove = fam_list[remove]
	print("This will delete the {} family - are you sure? ".format(
		fam_2_remove,end=""
		))
	certain = input("Enter y/n ")
	if certain.lower() == "y":
		try:
			fam_list.pop(remove)
		except:
			print("Error occured. No changes made. Check if family exists" +
			" or is spelled correctly.")
		else:	
			print("{} family removed".format(fam_2_remove))
			logger.info("{} family removed".format(fam_2_remove))
	else:
		print("no changes made")
	print("Families: ")
	for fam in fam_list:
		print("\t{}".format(fam))
	save_fam(fam_list)
	with open("removed_fams.txt","a+") as f:
		f.write("{}".format(fam_2_remove))
	logger.debug("Exiting remove_family")
	
def correct_fam():
	logger.debug("Entered correct_fam")
	print_heading("Correct Family Spelling")
	fam_list = get_fam_list()
	list_len = len(fam_list)
	print()
	for i in range(list_len):
		print("{} - {}".format(i,fam_list[i]))
	fam_2_correct = int(input("Enter number of family member to correct: "))
	old_fn = fam_list[fam_2_correct] + ".csv"
	fam_list[fam_2_correct] = input("Enter correction: ")
	new_fn = fam_list[fam_2_correct] + ".csv"
	from os import getcwd,chdir,rename
	print(getcwd())
	pause()
	rename(old_fn,new_fn)
	print("\nNew family list:")
	for fam in fam_list:
		print("\t{}".format(fam))
	save_fam(fam_list)
	logger.debug("Entered correct_fam")

def main(*args,**kwargs):
	fam_list = get_fam_list()
	for name in fam_list:
		if name == "Jolley":
			fam = Family(name)
			print("Last Name:", fam.last)
			print("Money in:", *fam.money_in)
			print("amt_owed", fam.amt_owed)
			print("Money out:",fam.money_out)
			print("balance:",fam.balance)
			pause()
			print(fam.save_html())
			fam.email_html()
			#fam.update_table()
			fam.print_table()
		else:
			print(name)
	#create_fam()
	#correct_fam()
	#remove_family()
	print("               goodbye                   ")
		

if __name__ == "__main__":
	logger.debug("***************** start *******************")
	main()
	logger.debug("***************** end *********************")