import os
import logging

##logger set up
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(name)s: %(message)s')
file_handler = logging.FileHandler('clean.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

#generator for directory list
def dir_list_gen(path):
	logger.debug("entered dir_list_gen")
	logger.debug("getting files from {}".format(path))
	count=0
	for file in os.listdir(path): 
		count+=1
		#logger.debug("file from path = {}, count = {}".format(file,count))
		yield file
	
#generator for pattern match
def pattern_match(path,pattern):
	logger.debug("entered pattern match")
	count = 0
	matches = 0
	for file in dir_list_gen(path):
		count+=1
		#logger.debug("count = {}".format(count))
		if pattern.lower() in file.lower():
			logger.debug("file match = {}".format(file))
			matches+=1
			logger.debug("matches = {}".format(matches))
			yield file

def open_file(filename:str)-> str:
	'''
	generator that opens and yields a line from the data file as string
	
	'''
	logger.debug("entered open_file")
	with open(filename,'r') as file:
		for line in file:
			logger.debug("line yielded = {}".format(line.rstrip("\n")))
			yield line.rstrip("\n")

#main
def main():
	'''
	main program loop
	
	'''
	logger.debug("**************clean.py start***********")
	path = os.getcwd()
	logger.debug("path = ".format(path))
	clean_list = []
	for x in open_file("removed_fams.txt"):
		logger.debug("x = {}".format(x))
		for match in pattern_match(path,x):
			clean_list.append(match)
			logger.debug("returned from pattern_match")
			logger.debug("clean_list = {}".format(clean_list))
	if len(clean_list) > 0:
		print("The following files will be removed: ")
		for file in clean_list: 
			print(file)
			logger.info("file to delete = {}".format(file))
		delete = input("do you wish to delete these files? (y/n) ")
		logger.info("delete = {}".format(delete))
		if delete.lower() == 'y':
			logger.debug("delete == 'y'")
			for file in clean_list:
				logger.debug("deleting {}".format(file))
				try:
					os.remove(file)
				except OSError as e:
					print("Error: {} - {}".format(e.filename,e.strerror))
					logger.error("Error: {} - {}".format(e.filename,e.strerror))
				else:
					print("{} deleted".format(file))
					with open("removed_fams.txt","w") as file:
						logger.debug("wrote new file")
		else:
			logger.debug("user chose not to delete files")
	else:
		logger.info('clean method found no files to delete')	
	logger.debug("**************clean.py end*************")
	
if __name__ == "__main__":
	main()