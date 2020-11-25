#import libraries
import mylib as ml
import logging
import datetime
import babysitters as bs


##logger set up
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
format = '%(asctime)s: %(levelname)s: %(name)s: %(funcName)s: %(message)s'
formatter = logging.Formatter(format)
file_handler = logging.FileHandler('logs/babysitting.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def html_report(b,c,*args,**kwargs):
	'''
	Creates HTML page report
	
	Creates detailed HTML report with all of the family balances and the cash on 
	hand amount. Can also include links to each family's HTML page with details
	of their payments (defaulted to True), as well as a link to the Babysitter 
	HTML payment detail page.
	
	Arguments:
	b = dictionary of family balances
	c = cash on hand amount
	args = list of any additional arguments that are inserted
	kwargs = dictionary of any keyword arguments that are added
	'''
	
	#get list of family names from dictionary 
	a=b.keys()
	logger.info("additional args given: {}".format(args))
	logger.info("kwargs = {}".format(kwargs))
	
	#open file
	html_filename = 'reports/full_report.html'
	with open(html_filename, "w") as html_file:
		html_file.write("<html>\n")
	
		#HTML head
		html_file.write("\t<head>\n")
		html_file.write("\t\t<title>Full Small Group Babysitting Report</title>\n")
		html_file.write("\t\t<link href='main.css' type='text/css' rel='stylesheet'/>\n")
		html_file.write("\t</head>\n")
	
		#HTML body
		html_file.write("\t\t<body>")
	
		#Heading
		html_file.write("\t\t\t<h1>Small Group Babysitting Report</h1>\n")
	
		#Section A - Family Balances 
		html_file.write("\t\t\t<br>\n\t\t\t<h3>Family Balances</h3>\n")
		for key in a:
			html_file.write(f"\t\t\t<div class='family-balance'>{key} balance is ${b[key]:.2f}</div>\n")
		html_file.write("\t\t\t<hr>\n\t\t\t<br>\n")
	
		#Section B - Cash On Hand
		html_file.write(f"\t\t\t<h3>Cash on Hand</h3>\n\t\t\t<br>\n\t\t\tCash on hand = ${c:.2f}</h3>\n")
		num_args=len(args)

		#Section C - Tables
		if "table" in kwargs.keys():
			t = kwargs['table']
			html_file.write("\t\t\t<hr>\n")
			html_file.write("\t\t\t<br>\n\t\t\t<h3>Family Tables</h3>\n\t\t\t<br>")
			for f, tbl in t.items():
				html_file.write(f"\t\t\t<h4>{f} Family Table</h4>\n")
				headers = tbl.pop(0)
				headers.append('Balance')
				html_file.write("\t\t\t<table>\n")
				html_file.write('\t\t\t\t<thead>\n')
				money_in = [float(x[1]) for x in tbl]
				money_out = [float(x[2]) for x in tbl]
				z = zip(money_in,money_out)
				weekly = [x-y for (x,y) in z]
				loop = 0
				html_file.write('\t\t\t\t\t<tr>\n')
				for col in headers:
					html_file.write(f"\t\t\t\t\t\t<th>{col}</th>\n")
				html_file.write("\t\t\t\t\t</tr>\n")
				html_file.write('\t\t\t\t</thead>\n')
				html_file.write('\t\t\t\t</tbody>\n')
				for row in tbl:
					logger.debug(f"row: {row}")
					html_file.write("\t\t\t\t\t<tr>\n")
					row.append(weekly[loop])
					loop += 1
					for item in row:
						logger.debug(f"item: {item}")
						html_file.write(f"\t\t\t\t\t\t<td>{item}</td>\n")
					logger.debug(f'loop now = {loop}')
				html_file.write("\t\t\t\t\t</tr>\n")
				html_file.write('\t\t\t\t</tbody>\n')
			html_file.write("\t\t\t</table>\n")
		
		#Babysitter data
		headers = ['Date', '# Sitters', "Amt Paid Each", "Total Paid"]
		bs_data = bs.open_dat()
		html_file.write("\t\t\t<hr>\n")
		html_file.write("\t\t\t<h3>Babysitter Payments</h3>\n")
		html_file.write("\t\t\t\t<table>\n")
		html_file.write('\t\t\t\t\t<thead>\n')
		html_file.write("\t\t\t\t\t\t<tr>\n")
		for head in headers:
			html_file.write(f"\t\t\t\t\t\t\t<th>{head:15}</th>\n")
		html_file.write('\t\t\t\t\t\t</tr>\n')
		html_file.write('\t\t\t\t\t</thead>\n')
		html_file.write('\t\t\t\t\t<tbody>\n')
		for line in bs_data:
			html_file.write("\t\t\t\t\t\t<tr>\n")
			for item in line:
				html_file.write(f"\t\t\t\t\t\t\t<td>{item:15}</td>\n")
			html_file.write(f"\t\t\t\t\t\t\t<td>{int(line[1]) * float(line[2]):15}</td>\n")
			html_file.write("\t\t\t\t\t\t</tr>\n")
		html_file.write('\t\t\t\t\t</tbody>\n')
		html_file.write("\t\t\t\t</table>")

		#Additional Info
		if num_args > 1:
			html_file.write("\t\t\t<hr>\n\t\t\t<br>\n\t\t\t<h3>Additional Info</h3>\n")
			html_file.write('\t\t\t\t<ul>\n')
			for arg in args:
				html_file.write(f"\t\t\t\t\t<li>{arg}</li>\n")
			
		#footer 
		html_file.write("\t\t<footer>")
		date = datetime.datetime.now()
		d = date.strftime("%m/%d/%Y, %H:%M:%S")
		html_file.write(f"\t\t\t{d}\n")
		html_file.write('\t\t</footer>\n')

		#end of file
		html_file.write("\t</body>\n</html>\n")

	logger.info("*********  HTML Report Saved  *****************")
	return "full_report.html saved"

if __name__ == "__main__":
	#use to test module
	b={"George":1,"Ralph":2,"Bonnie":3,"Burt":4,"Andrew":5}
	c=24.53
	d={"George":{'1':[1,2,3,4,5]},"Ralph":{'2':[2,4,6,8,10]},"Bonnie":{'3':[3,6,9,12,15]},"Burt":{'4':[4,8,12,16,20]},"Andrew":{'5':[5,10,15,20,25]}}
	e=[1,2,3,4,5]
	UT_orange = "F77F00"
	white = "FFFFFF"
	print(html_report(b,c,e,d,text=white,bgcolor=UT_orange))
	
	