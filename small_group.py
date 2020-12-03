import webbrowser
import logging
from os.path import exists
from family import Family, get_fam_list, create_fam, correct_fam, remove_family
from mylib import print_heading, clear, pause, check_for_file,check_os
from babysitters import view_babysitter_table, enter_bs_data
from reports import html_report

this_os = check_os()
if this_os == 'windows':
	chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
elif this_os == 'mac':
	chrome_path = 'open -a /Applications/Google/Chrome.app %s'
elif this_os == 'nix':
	chrome_path = '/usr/bin/google-chrome %s'
else:
	chrome_path = None
chrome = webbrowser.get(chrome_path)

##logger set up
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
format = '%(asctime)s: %(levelname)s: %(name)s: %(funcName)s: %(message)s'
formatter = logging.Formatter(format)
file_handler = logging.FileHandler('logs/babysitting.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

logger.info('\n\n')

def update_families():
	'''
	builds menu to update the list of families
	
	takes no arguments
	prints menu and gets input from user on option
	then calls appropriate function based on user input
	'''
	
	logger.debug("Entered function")
	menu_list = [
				"Add Family",
				"Correct Family",
				"Remove Family"
				]
	while True:
		choice = menu("Update Families",menu_list)
		if choice.isalpha():
			if choice == "x":
				logger.debug("exiting function")
				break
			else:
				continue
		elif choice.isnumeric():
			num = int(choice)
			if num == 1:
				logger.debug("menu choice - create_fam")
				create_fam()
			if num == 2:
				logger.debug("menu choice - correct family")
				correct_fam()
			if num == 3:
				logger.debug("menu choice - remove family")
				remove_family()
	
				
def menu(menu_name,menu_list,exit_char="x"):
	clear()
	logger.debug("entered menu function")
	print_heading(menu_name)
	for i, item in enumerate(menu_list):
		print(f"\t\t{i+1} - {item}")
	print("\n\n\n")
	choice = input(f"\t\tEnter selection or '{exit_char}' to exit ")
	logger.debug("exiting menu function")
	return choice
	
def fam_sub_menu(Fam):
	logger.debug("Entered fam_sub_menu")
	last=Fam.last
	sub_list = [
				"View Balance", 
				"View Table", 
				"Update Table", 
				"Save Table to HTML"
				]
	while True:
		choice = menu(f"{last} Family Menu", sub_list)
		try:
			num = int(choice)
		except ValueError:
			logger.debug("exiting fam_sub_menu")
			break
		else:
			if num == 1:
				logger.debug("f{last} - view balance")
				print()
				output = f"{last} balance = {Fam.balance}"
				print(output)
				print()
				pause()
			elif num == 2:
				logger.debug(f"{last} - view table")
				clear()
				Fam.print_table()

			elif num == 3:
				logger.debug(f"{last} - update table")
				Fam.update_table()
			elif num == 4:
				logger.debug(f"{last} - save html")
				print(Fam.save_html())
				open_page = input('Would you like to open page now (y/n)? ')
				if open_page.lower() == 'y':
					print('opening page......')
					chrome.open_new(Fam.html)
			else:
				print(f"{num} - invalid number entered")
				pause()

def view_cash_on_hand():
	logger.debug("************************  COH start  ***********************")
	coh = 0.0
	d=view_all_balances()
	for balance in d.values():
		coh += balance
	logger.info(f"coh = {coh}")
	logger.debug("*************   Calculated Cash on Hand   *******************")
	return coh

def bs_pay_sub_menu():
	logger.debug("entered bs_pay_sub_menu")
	sub_menu_list = [
					"View Babysitter Payment Table",
					"Enter Babysitter Payment Data",
					]
	while True:
		choice = menu("Babysitter Payments", sub_menu_list)
		if choice == "x":
			break
		elif choice == '1':
			view_babysitter_table()
		elif choice == '2':
			enter_bs_data()
		else:
			print(f"wrong input = {choice}")
			pause()

def view_all_balances():
	'''returns dictionary with balances for each family'''
	logger.debug("entered function")
	balances = {}
	names = get_fam_list()
	for name in names:
		Fam=Family(name)
		balances[name]=Fam.balance
	logger.debug("leaving function")
	return balances
	
def actions_menu():
	logger.debug("entered actions_menu()")
	clear()
	while True:
		menu_list = [
				"Update Family",
				"View All Families Balances",
				"Babysitter Payments",
				"View Cash On Hand",
				"Overall HTML Report"
				]
		sel = menu("Actions Menu",menu_list)
		if sel.isalpha():
			if sel.lower() == "x":
				logger.debug("exiting main menu")
				break
		elif sel.isnumeric():
			logger.debug("user input is numeric")
			menu_num = int(sel)-1
			logger.debug(f"menu_num = {menu_num}, sel = {sel}")
			if sel == '1':
				logger.debug("Update Fam")
				update_families()
			elif sel == '2':
				logger.debug("View Balances")
				clear()
				print_heading("All Family Balances")
				fam_balances = view_all_balances()
				for name,balance in fam_balances.items():
					print(f"{name} balance = ${balance:.2}")
				pause()
			elif sel == '3':
				logger.debug("babysitter payments".title())
				bs_pay_sub_menu()
			elif sel == '4':
				clear()
				print_heading("Cash On Hand")
				cash = view_cash_on_hand()
				print(f"\t\tCash on Hand = ${cash:.2}\n")
				pause()
			elif sel == '5':
				logger.debug("HTML Report")
				f = get_fam_list()
				d = {}
				for fam in f:
					family = Family(fam)
					logger.info(f"family last = {family.last}")
					family.save_html()
					d[fam]=family.table
				b = view_all_balances()
				c = view_cash_on_hand()
				print(html_report(b,c,tables=d))
				print()
				open_html = input("would you like to open the report (y/n)?")
				if open_html.lower() == "y":
					chrome.open_new('reports/full_report.html')
		else:
			logger.error(f"{sel} is invalid choice")
			continue
		
#main program function
def main():
	logger.debug("entered main menu()")
	clear()
	while True:
		main_list = get_fam_list()
		add = [
				"Actions Menu",
				]
		for item in add:
			main_list.append(item)
		sel = menu("Main Menu",main_list)
		if sel.isalpha():
			if sel.lower() == "x":
				logger.debug("exiting main menu")
				break
		elif sel.isnumeric():
			logger.debug("user input is numeric")
			num_of_fams = (len(main_list) - len(add))
			menu_num = int(sel)-1
			logger.debug(f"num of fams = {num_of_fams}, menu_num = {menu_num}, sel = {sel}")
			if int(sel) <= num_of_fams:
				try:
					fam = Family(main_list[menu_num])
				except:
					logger.exception(f"sel={menu_num}, num_of_fams = {num_of_fams}")
				else:
					fam_sub_menu(fam)
					logger.debug(f"family name is {fam.last}")
				finally:
					logger.debug("selection success")
			elif sel == str(num_of_fams + 1):
				logger.debug("Actions Menu")
				actions_menu()
		else:
			logger.error(f"{sel} is invalid choice")
			continue

def validate():
	'''
	validates required files exist 
		'''

	logger.debug("Entered validate function")
	valid = True
	with open('data/files.dat', 'r') as f:
		file_list = []
		line = f.readline().strip()
		while line:
			file_list.append(line)
			line = f.readline().strip()
	for file_name in file_list:
		if not exists(file_name):
			print(f'creating {file_name}')
			logger.info(f'{file_name} created')
			try:
				with open(file_name, 'w') as f:
					f.write('')
			except (FileNotFoundError, OSError) as e:
				print(f"Error: {e.strerror}")
				logger.debug(e)
				valid = False
	return valid

def exit_protocol(**kwargs):
	if 'error_' in kwargs.keys():
		exit_code = 1
		logger.critical(f"exit code: {exit_code}: error msg: {kwargs['error_']}")
		print(f'exiting program with exit code{exit_code}\n{kwargs["error_"]}')
	else:
		exit_code = 0
		logger.info(f'exit code: {exit_code}')
	print_heading("Goodbye!")
	
if __name__ == "__main__":
	files_valid = validate()
	if files_valid:
		main()
	else:
		exit_protocol(error_="File Verification Failed - program terminated")
		logger.critical("File Verification Failed - program terminated")
	
	