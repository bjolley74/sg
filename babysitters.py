import logging
##logger set up
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(name)s: %(message)s')
file_handler = logging.FileHandler('logs/babysitting.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
from mylib import pause, get_input, check_for_file

logger.info('******* babysitters start************')


def save_bs_html(nested_list):
	'''
	Save babysitter data to html
	
	Takes a nested_list of babysitter data as input and saves it into a HTML 
	file. 
	'''

	logger.debug("entered babysitters.py/save_bs_html")
	header = ['Date', '# Sitters', 'Amt Paid Each', 'Total Paid']
	with open("reports/bs_data.html","w") as file:
		file.write("<html>\n\t<head>\n")
		file.write("\t\t<link href='main.css' rel='stylesheet' type='text/css' />\n")
		file.write("\t</head>\n")
		file.write("\t<body>\n")
		file.write("\t\t<h1>Babysitter Payments</h1>\n")
		file.write("\t\t<table>\n")
		file.write('\t\t\t<thead>\n')
		file.write("\t\t\t\t<tr>\n")
		for num in range(len(header)):
			file.write(f"\t\t\t\t\t<th>{header[num]}</th>\n")
		file.write("\t\t\t\t</tr>\n")
		file.write("\t\t\t</thead>\n")
		file.write("\t\t\t<tbody>\n")
		for line in nested_list:
			file.write("\t\t\t\t<tr>\n")
			a,b,c,d = line[0],line[1],line[2], int(line[1]) * float(line[2])
			file.write(f"\t\t\t\t\t<td>{a}</td>\n")
			file.write(f'\t\t\t\t\t<td>{b}</td>\n')
			file.write(f'\t\t\t\t\t<td>{c}</td>\n')
			file.write(f"\t\t\t\t\t<td>{d}</td>\n")
			file.write("\t\t\t\t</tr>\n")
		file.write("\t\t\t</tbody>\n")
		file.write("\t\t</table>\n")
		file.write("\t</body>\n")
		file.write("</html>\n")
	logger.debug("exited function - bs_data.html saved")

def open_dat():
	'''
	open_dat has no arguments. It opens bs.cvs and returns a nested list of 
	the babysitter data
	'''
	
	logger.debug("Entered babysitters.py/open_dat()")
	check_for_file('data/bs.csv')
	with open('data/bs.csv',"r") as file:
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
	with open("data/bs.csv","w") as file:
		#iterate through the list and save each line of data
		for line in list_in:
			file.write(",".join(line))
			file.write('\n')
	logger.debug("leaving function")
	
def view_babysitter_table():
	'''
	function prints the babysitter table to screen
	'''
	
	logger.debug("entered babysitter.py/view_babysitter_table()")
	col_list = [
				"Date",
				"Number of Sitters",
				"Amount Paid to Each",
				"Total Amount Paid"
				]
	table = open_dat()
	for col_header in col_list:
		print(f" {col_header:15} ", end='')
	print('')
	for line in table:
		week_total = int(line[1]) * float(line[2])
		print(f"{line[0]:15}{line[1]:15}{line[2]:15}{week_total:15}")
	pause()
	save_bs_html(table)
	logger.debug("leaving babysitter.py/view_babysitter_table()")

def enter_bs_data():
	'''
	gets user input of babysitter data and adds it to the table
	'''
	
	logger.debug("entered enter_bs_data()")
	questions = [
				"Enter date: ",
				"Enter number of sitters: ",
				"Enter amt paid to each sitter: "
				]
	list_add = []
	#test for to make sure list_add has same length as questions
	while len(list_add) < len(questions): list_add = get_input(questions)
	#open data table
	table = open_dat()
	#debug log to show table data before add
	logger.debug("table before add:")
	for item in table: logger.debug(f'{item}')
	table.append(list_add)
	#and after add
	logger.debug("table after add:")
	for item in table: logger.debug(f'{item}')
	#save changed table
	save_dat(table)
	pause()

def main():
	#determines if file exists and if not will create the file and test it
	logger.debug('babysitters.py main running')
	check_for_file('data/bs.csv')
	with open("data/bs.csv",'r') as file:
		file.readlines()
	print("file read")
	logger.debug("file read")
	run_test = input("should I run test? (Y/N) ")
	ans = run_test[0].lower()
	if ans == 'y':
		view_babysitter_table()
		enter_bs_data()
		view_babysitter_table()
		
if __name__ == "__main__":
	main()