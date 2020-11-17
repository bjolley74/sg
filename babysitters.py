import logging
##logger set up
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(name)s: %(message)s')
file_handler = logging.FileHandler('babysitting.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
from mylib import *
logger.info('******* babysitters start************')


def save_bs_html(nested_list):
	'''
	Save babysitter data to html
	
	Takes a nested_list of babysitter data as input and saves it into a HTML 
	file. 
	'''
	
	logger.debug("entered save_bs_html")
	with open("bs_data.html","w") as file:
		file.write("<html>\n")
		file.write("<body text=black bgcolor=white>\n")
		file.write("<h1>Babysitter Payments</h1>\n")
		file.write("<table border=0>\n")
		file.write("<tr>\n")
		file.write("<th>{:15}</th>".format("Date"))
		file.write("<th>{:10}</th>".format("# Sitters"))
		file.write("<th>{:15}</th>".format("Amt Paid Each"))
		file.write("<th>{:15}</th></tr>\n".format("Total Paid"))
		for line in nested_list:
			file.write("<tr>")
			a,b,c,d = line[0],line[1],line[2], int(line[1]) * float(line[2])
			file.write("<center><td>{:15}</center></td>".format(a))
			file.write('<center><td>{:10}</center></td>'.format(b))
			file.write('<center><td>{:15}</center></td>'.format(c))
			file.write("<center><td>{:10}</center></td>\n".format(d))
			file.write("</tr>\n")
	logger.debug("exited function - bs_data.html saved")

def open_dat():
	'''
	open_dat has no arguments. It opens bs.cvs and returns a nested list of 
	the babysitter data
	'''
	
	logger.debug("Entered open_dat()")
	try:
		with open('bs.csv','r') as file:
			pass
	except:
		#if file does not exist will call main which creates the file
		logger.exception("Error occured in with open bs.csv")
		main()
	else:
		with open('bs.csv',"r") as file:
			l=[]
			line=file.readline().strip()
			while line:
				line2=line.split(',')
				l.append(line2)
				line=file.readline().strip()
		logger.debug("Left open_dat()")
		return l
	
def save_dat(list_in):
	'''
	Saves the data to file
	
	Takes argument of list_in, a nested list, and saves it to bs.cvs
	'''
	
	logger.debug("entered save_dat")
	#open file	
	with open("bs.csv","w") as file:
		#iterate through the list and save each line of data
		for line in list_in:
			file.write(",".join(line))
			file.write('\n')
	logger.debug("leaving function")
	
def view_babysitter_table():
	'''
	function prints the babysitter table to screen
	'''
	
	logger.debug("entered view_babysitter_table()")
	col_list = [
				"Date",
				"Number of Sitters",
				"Amount Paid to Each",
				"Total Amount Paid"
				]
	table = open_dat()
	print("{:15}{:10}{:15}{:15}".format("Date","# Sitters","Amt Paid Each","Total Paid" ))
	for line in table:
		week_total = int(line[1]) * float(line[2])
		print("{:15}{:10}{:15}{:10}".format(line[0],line[1],line[2],week_total))
	pause()
	save_bs_html(table)
	logger.debug("leaving function")
		
	
		
	
def enter_bs_data():
	'''
	gets user input of babysitter data and adds it to the table
	'''
	
	#todo:
	#	add for case for blank input
	logger.debug("entered enter_bs_data()")
	questions = [
				"Enter date: ",
				"Enter number of sitters: ",
				"Enter amt paid to each sitter: "
				]
	date, num_sitters, aps = get_input(questions)
	list_add = [date,num_sitters,aps]
	table = open_dat()
	logger.debug("table before add:")
	for item in table: logger.debug(item)
	table.append(list_add)
	logger.debug("table after add:")
	for item in table: logger.debug(item)
	save_dat(table)
	pause()

def main():
	#determines if file exists and if not will create the file and test it
	logger.debug('babysitters.py main running')
	try:
		with open("bs.csv",'r') as file:
			file.readlines()
		print("file read")
		logger.debug("file read")
	except:
		logger.exception("file not read, setting up bs.csv")
		print("Creating new file")
		with open('bs.csv','w') as new:
			new.write('01/01/1900,1,5,5')
	run_test = input("should I run test? (Y/N) ")
	ans = run_test[0].lower()
	if ans == 'y':
		view_babysitter_table()
		enter_bs_data()
		view_babysitter_table()
		
if __name__ == "__main__":
	main()
logger.info('************  babysitters end  ************')