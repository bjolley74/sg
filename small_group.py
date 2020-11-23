import webbrowser as wb
import logging
from family import Family, get_fam_list, create_fam, correct_fam, remove_family
from mylib import print_heading, clear, pause
from babysitters import view_babysitter_table, enter_bs_data
from reports import html_report
import clean

##logger set up
log = "babysitting.log"
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
format = '%(asctime)s: %(levelname)s: %(name)s: %(funcName)s: %(message)s'
formatter = logging.Formatter(format)
file_handler = logging.FileHandler(log)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def update_families():
	'''
	builds menu to update the list of families
	
	takes no arguments
	prints menu and gets input from user on option
	then calls appropriate function based on user input
	'''
	
	logger.debug("Entered function")
	#fam_list = get_fam_list()
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
				clean.main()
	
				
def menu(menu_name,menu_list,exit_char="x"):
	logger.debug("entered function")
	print_heading(menu_name)
	num_items = len(menu_list)
	for i in range(num_items):
		print("\t\t{} - {}".format(i+1,menu_list[i]))
	print()
	print()
	print()
	choice = input("\t\tEnter selection or '{}' to exit ".format(exit_char))
	print()
	logger.debug("exiting function")
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
		choice = menu("{} Family Menu".format(last),sub_list)
		try:
			num = int(choice)
		except:
			logger.debug("exiting fam_sub_menu")
			break
		else:
			if num == 1:
				logger.debug("{} - view balance".format(last))
				print()
				output = "{} balance = {}".format(last, Fam.balance)
				print(output)
				print()
				pause()
			elif num == 2:
				logger.debug("{} - view table".format(last))
				clear()
				Fam.print_table()

			elif num == 3:
				logger.debug("{} - update table".format(last))
				Fam.update_table()
			elif num == 4:
				logger.debug("{} - save html".format(last))
				print(Fam.save_html())
				open_page = input('Would you like to open page now (y/n)? ')
				if open_page.lower() == 'y':
					print('opening page......')
					wb.open(Fam.html,new=2,autoraise=False)
			else:
				print("{} - invalid number entered".format(num))
				pause()

def view_cash_on_hand():
	logger.debug("************************  COH start  ***********************")
	coh = 0.0
	d=view_all_balances()
	for balance in d.values():
		coh+=balance
	logger.info("coh = {}".format(coh))
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
		elif choice == '3':
			clear()
			print_heading("Cash On Hand")
			cash=view_cash_on_hand()
			print("\t\tCash on Hand = ${:,.2f}".format(cash))
			print()
			pause()
		else:
			print("wrong input = {}".format(choice))
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
			logger.debug("menu_num = {}, sel = {}".format(menu_num,sel))
			if sel == '1':
				logger.debug("Update Fam")
				update_families()
			elif sel == '2':
				logger.debug("View Balances")
				clear()
				print_heading("All Family Balances")
				fam_balances = view_all_balances()
				for name,balance in fam_balances.items():
					print("{} balance = ${:,.2f}".format(name,balance))
				pause()
			elif sel == '3':
				logger.debug("babysitter payments".title())
				bs_pay_sub_menu()
			elif sel == '4':
				#insert cash on hand call from bs_pay_sub_menu
				clear()
				print_heading("Cash On Hand")
				cash=view_cash_on_hand()
				print("\t\tCash on Hand = ${:,.2f}".format(cash))
				print()
				pause()
			elif sel == '5':
				logger.debug("HTML Report")
				f = get_fam_list()
				d = {}
				for fam in f:
					family = Family(fam)
					logger.info("family last = {}".format(family.last))
					family.save_html()
					d[fam]=family.table
				b = view_all_balances()
				c = view_cash_on_hand()
				print(html_report(b,c,tables=d))
				print()
				open_html = input("would you like to open the report (y/n)?")
				if open_html.lower() == "y":
					wb.open('full_report.html',new=2,autoraise = False)
		else:
			logger.error("{} is invalid choice".format(sel))
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
			logger.debug("num of fams = {}, menu_num = {}, sel = {}".format(num_of_fams,menu_num,sel))
			if int(sel) <= num_of_fams:
				try:
					fam = Family(main_list[menu_num])
				except:
					logger.exception("sel={0}, num_of_fams = {1}".format(menu_num,num_of_fams))
				else:
					fam_sub_menu(fam)
					logger.debug("family name is {}".format(fam.last))
				finally:
					logger.debug("selection success")
			elif sel == str(num_of_fams + 1):
				logger.debug("Actions Menu")
				actions_menu()
		else:
			logger.error("{} is invalid choice".format(sel))
			continue

def validate():
	logger.debug("Entered validate function")
	valid_users=["bobby","bonnie","bj"]
	valid = False
	losername = input("Enter First Name: ")
	if losername.lower() in valid_users:
		valid = True
	logger.info("user entered = {}".format(losername))
	return valid

	
if __name__ == "__main__":
	valid_user = validate()
	if valid_user:
		main()
	else:
		print("User Verification Failed - program terminated")
		logger.critical("User Verification Failed - program terminated")
	print_heading("Goodbye!")
	