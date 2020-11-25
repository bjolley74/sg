import os
import logging
from pathlib import Path

##logger set up
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(name)s: %(message)s')
file_handler = logging.FileHandler('logs/clean.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

#generator for directory list
def dir_list_gen(path):
	logger.debug("entered dir_list_gen")
	logger.debug(f"getting files from {path}")
	count=0
	for name in os.listdir(path): 
		count+=1
		yield name
	
#generator for pattern match
def pattern_match(path, pattern):
	logger.debug("entered pattern match")
	matches = 0
	for fn in dir_list_gen(path):
		if pattern.lower() in fn.lower():
			logger.debug("file match = {}".format(fn))
			matches+=1
			logger.debug("matches = {}".format(matches))
			yield fn

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
	start_dir = os.getcwd()
	logger.debug("**************clean.py start***********")
	print('cleaning up files...')
	clean_list = []
	paths = ['/data', '/reports']
	removed_text_fn = Path("./data/removed_fams.txt")
	for x in open_file(removed_text_fn):
		logger.debug(f"x = {x}")
		for path in paths:
			cdpath = Path(os.getcwd() + path)
			os.chdir(cdpath)
			logger.debug(f'path = {path}')
			for match in pattern_match(cdpath, x):
				file_to_delete = Path(path + '/' + match)
				clean_list.append(file_to_delete)
				logger.debug("returned from pattern_match")
				logger.debug(f"clean_list = {clean_list}")
			os.chdir('..')
	if len(clean_list) > 0:
		os.chdir(start_dir)
		print("The following files will be removed: ")
		for filename in clean_list: 
			logger.info(f"file to delete = {filename}")
			print(filename)
		delete = input("do you wish to delete these files? (y/n) ")
		logger.info(f"delete = {delete}")
		if delete[0].lower() == 'y':
			logger.debug("delete == 'y'")
			for filename in clean_list:
				logger.debug(f"deleting {filename}".format(filename))
				try:
					delete_file = Path(start_dir + str(filename))
					os.remove(delete_file)
				except OSError as e:
					msg = f"Error: {delete_file} - {e.strerror}"
					print(msg)
					logger.error(msg)
				else:
					print(f"{filename} deleted")
					with open("./data/removed_fams.txt","w") as new_file:
						logger.debug("wrote new file")
		else:
			msg = 'Exiting without deletion, user chose not to remove files.'
			logger.debug(msg)
			print(msg)
	else:
		msg = 'Exiting without deletion, clean method found no files to delete'
		logger.info(msg)
		print(msg)
	
	logger.debug("**************clean.py end*************")
	
if __name__ == "__main__":
	main()