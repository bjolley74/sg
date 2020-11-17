#import libraries
import mylib as ml
import logging
import datetime
import babysitters as bs
#from family import get_fam_list

log = "babysitting.log"
##logger set up
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
format = '%(asctime)s: %(levelname)s: %(name)s: %(funcName)s: %(message)s'
formatter = logging.Formatter(format)
file_handler = logging.FileHandler(log)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

logger.info("******* reports.py  *****************")

#todo
#  
#
#  

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
	#get colors from kwargs
	if "text" in kwargs.keys():
		text_color = kwargs["text"]
	else:
		text_color = "000000"
	if "bgcolor" in kwargs.keys():
		bgcolor = kwargs["bgcolor"]
	else:
		bgcolor = "FFFFFF"
	if "tables" in kwargs.keys():
		t = kwargs['tables']
	
	logger.info("additional args given: {}".format(args))
	logger.info("kwargs = {}".format(kwargs))
	
	#open file
	file = open("full_report.html", "w")
	file.write("<html>\n")
	
	#HTML head
	file.write("<head>\n")
	file.write("<title>")
	file.write("Full Small Group Babysitting Report")
	file.write("</title>\n")
	file.write("<style>table, th, td {  border: 1px solid black;  border-collapse: collapse;}</style>")
	file.write("</head>\n")
	
	#HTML body
	file.write("<body bgcolor={} text = {}>\n".format(bgcolor,text_color))
	
	#Heading
	file.write("<center><h1>Small Group Babysitting Report</h1></center>\n")
	
	#Section A - Family Balances 
	file.write("<br><br>\n<h3>Family Balances</h3>\n")
	for key in a:
		file.write("<div>{} balance is ${:.2f}</div>\n".format(key,b[key]))
	file.write("<hr><br>\n")
	
	#Section B - Cash On Hand
	file.write("<h3>Cash on Hand</h3>\n<br>\n Cash on hand = ${:.2f}</h3>\n".format(c))
	num_args=len(args)
	
		#Section C - Tables
	file.write("<hr></hr>\n")
	file.write("<br>\n<h3>Family Tables</h3>\n<br>")
	for f,tbl in t.items():
		file.write("<h4>{} Family Table</h4>".format(f))
		headers = tbl.pop(0)
		headers.append('Balance')
		file.write("<table>")
		money_in = [float(x[1]) for x in tbl]
		money_out = [float(x[2]) for x in tbl]
		z = zip(money_in,money_out)
		weekly = [x-y for (x,y) in z]
		loop = 0
		file.write('</tr>')
		for col in headers:
			file.write("<th><center>{}</th></center>".format(col))
		file.write("<tr>")
		for row in tbl:
			logger.debug("row: {}".format(row))
			file.write("<tr>")
			row.append(weekly[loop])
			loop+=1
			for item in row:
				logger.debug("item: ".format(item))
				file.write("<td>{}</td>".format(item))
			logger.debug('loop now = {}'.format(loop))
			file.write("</tr>")
		file.write("</table>")
	
	#Babysitter data
	bs_data = bs.open_dat()
	file.write("<hr>")
	file.write("<h3>Babysitter Payments</h3>\n")
	file.write("<table border=0>\n")
	file.write("<tr>\n")
	file.write("<th>{:15}</th>".format("Date"))
	file.write("<th>{:10}</th>".format("# Sitters"))
	file.write("<th>{:15}</th>".format("Amt Paid Each"))
	file.write("<th>{:15}</th></tr>\n".format("Total Paid"))
	for line in bs_data:
		file.write("<tr>")
		e,f,g,h = line[0],line[1],line[2], int(line[1]) * float(line[2])
		file.write("<center><td>{:15}</center></td>".format(e))
		file.write('<center><td>{:10}</center></td>'.format(f))
		file.write('<center><td>{:15}</center></td>'.format(g))
		file.write("<center><td>{:10}</center></td>\n".format(h))
		file.write("</tr>\n")
	file.write("</table>")
	#file.write("<a href='bs_data.html'>Babysitter Data</a>\n<br>\n")
	
	#Additional Info
	if num_args > 1:
		file.write("<hr><br><h3>Additional Info</h3>\n")
		for arg in args:
			file.write("<div>{}</div>\n".format(arg))
			
	#footer 
	file.write("<hr>\n")
	file.write("")
	date = datetime.datetime.now()
	file.write("<center><h4>{}</h4></center>\n".format(date))
	
	#end of file
	file.write("</body></html>")
	file.close()
	
	logger.info("*********  HTML Report Saved  *****************")
	return "full_report.html saved"

if __name__ == "__main__":
	#use to test module
	b={"George":1,"Ralph":2,"Bonnie":3,"Burt":4,"Andrew":5}
	c=24.53
	d={"George":[1,2,3,4,5],"Ralph":[2,4,6,8,10],"Bonnie":[3,6,9,12,15],"Burt":[4,8,12,16,20],"Andrew":[5,10,15,20,25]}
	e=[1,2,3,4,5]
	UT_orange = "F77F00"
	white = "FFFFFF"
	print(html_report(b,c,d,e,text=white,bgcolor=UT_orange))
	
	