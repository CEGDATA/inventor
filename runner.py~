import subprocess
import os, sys

"""
os.chdir(r'Z:\CEG\Software Development\Miniconda\Scripts')

PROJECT_ENV = 'sk_inventor_env'
#activate this environment whenever this script is called
subprocess.call(['activate', PROJECT_ENV])
"""

sys.path.insert(0, r".\mongo")
sys.path.insert(0, r".\excel")
sys.path.insert(0, r".\inv") 

import mongo_manager as mm
import read_write_excel as ex
import inventor_api as inv
import get_filenames as f

import xlwings as xw

from pprint import pprint

import time
#vendors we will be inserting into the database
VENDOR_LIST = ['3M', 'ABB', 'AFL', 'ANDERSON', 'Burndy', 'CG', 'Chance', 'DeltaStar', 
		'Hoffman', 'Hubbell', 'LAPP', 'Littelfuse', 'OHIO BRASS', 'Royal', 'SEFCOR',
		'Siemens', 'Trench', 'Victor Insulators']
#directories that we are not interested in traversing
FORBIDDEN = ['OldVersions', 'Import']
#the iproperties we want from the database.  NOTE This could be extracted from the excel sheet using the dataframe columns 
REQUESTED = ['Vendor', 'Part Number', 'Description', 'Catalog Web Link', 'Engr Approved By']
#the iproperties we want to write to the database.  Same as previous note
CHANGING = ['Vendor', 'Part Number', 'Description', 'Catalog Web Link', 'Engr Approved By']
#items not found in the inventor api
NOT_IN_API = ['Filename w/o Extension', 'Found Location']
#The database we want to interact with
DB_NAME = 'Inventor_DB_TESTING'
#the collection we want to interact with
COLL_NAME = 'iProperties_Collection_TESTING'
#path for excel document
EXCEL_PATH = r"Z:\CEG\DRAFTING\3DManufacturerParts\3D_Model_Database.xlsm"
#puts the vendor and part number columns first when writing, for readability
FIRST_COLUMNS = ['Vendor', 'Part Number']


def populate_db(vendor_list):
	"""
	This function will, given a list of vendors, go into the directories and pull out the iProperties from those .ipt files
	These iProperties will be inserted into the database.  Each part will have a document into the collection of the database.
	Once the documents are inserted into mongo, we will write the newly created Object Id as a custom iProperty so that the .ipt and the document 
	in the Mongo database are linked with each other.
	"""
	#get the .ipt files 
	parts = f.get_ipts(vendor_list, FORBIDDEN)
	#print(parts)
	#get the list of properties from these parts
	parts_props_list = inv.get_data(REQUESTED, parts, NOT_IN_API)
	#send this list to be inserted into mongo
	ins_ids = mm.first_to_mongo(parts_props_list, DB_NAME, COLL_NAME)
	#need to give inventor a second to get its act together 
	time.sleep(2)	
	#make a dictionary mapping the parts paths to the ids from mongo
	#NOTE, this is dependent on the ordered nature of python lists.  The parts were in a certain order, which is maintained throughout gathering
	#iProperties and inserting them into the database.  The outputted ids are therefore in the same order.
	path_id_dict = dict(zip(parts, ins_ids))
	#add the object_id property per this dictionary
	inv.change_props(path_id_dict=path_id_dict, is_first=True)
	#time.sleep(2)
	#inv.check_objectid(parts)



#inv.check_objectid([r'Z:\CEG\DRAFTING\3DManufacturerParts\LAPP\315210-70P1Z\LAPP 315210-70P1Z.ipt'])
#import win32api
#print(win32api.FormatMessage(-2147467259))
#print(win32api.FormatMessage(-2147024809))
#print(win32api.FormatMessage(-2147352567))
#exit()
#win32api errors:
#-2147024809: "The parameter is incorrect"
#-2147023170: "The remote procedure call failed"
#-2147352567: "Exception Occured"
#-2146959355: "Server execution failed"
#-2147023170: "The remote procedure call failed"



def read_from_db():
	"""
	This function will allow a user to input a "query" through inputting values into an excel sheet that will return the requested info from mongodb.
	It will output to either excel or php (or others if we use them in the future)C:\ProgramData\Anaconda3\python.exe
	"""
	#NOTE, currently, this just pulls the entire database, but this will become difficult as more and more data are added to the database, so
	#querying will be required.EXCEL_PATH = r"Z:\CEG\DRAFTING\3DManufacturerParts\3DModelDatabase_Jake_work_11152018.xlsx"
	wb = xw.Book.caller()
	sht = wb.sheets[0]
	#input dataframe is created by user on the 'Input' sheet.  This is used to structure the query to mongo	
	
	input_df = ex.get_from_excel(EXCEL_PATH, 'Input')
	documents = mm.from_mongo(DB_NAME, COLL_NAME, input_df)

	doc_df = ex.mongo_to_dataframe(documents)
	doc_df = doc_df.astype({'_id': str})
	doc_df = doc_df[FIRST_COLUMNS + [c for c in list(doc_df.columns) if c not in FIRST_COLUMNS]]

	sht.clear()
	sht.range('A1').value = doc_df
	#ex.send_to_excel(doc_df, FIRST_COLUMNS, EXCEL_PATH)			
	return None



def update_system():
	"""
	This function will update the database and iProperties according to the user input from either excel or webserver
	"""
	input_df = ex.get_from_excel(EXCEL_PATH, 'Sheet1')
	mm.update_mongo(DB_NAME, COLL_NAME, input_df)
	documents = mm.from_mongo(DB_NAME, COLL_NAME, input_df)

	doc_df = ex.mongo_to_dataframe(documents)
	doc_df = doc_df.astype({'_id': str})
	
	path_id_dict = dict(zip(doc_df['Found Location'].values, doc_df['_id']))
	inv.change_props(df=doc_df, not_in_api=NOT_IN_API, path_id_dict=path_id_dict)
	return None



def user():	
	user_input = input(
	"""What would you like to do?
	(a) Populate Database
	(b) Exit
	""")
	#quick little function to get the user input.  Calls populate db
	#shouldn't do anything else since the other calls should be done through excel at this point
	#NOTE, future development may have us run other functions from here.
	if user_input == 'a':
		vendors = list()
		check = True	
		while check:	
			vendor = input(
			"""Which vendor would you like to enter?
			NOTE, MAKE SURE DIRECTORIES ARE CLEANED
			Type 'exit' to exit
			""")
			if vendor == 'exit':
				print('Exiting...')
				exit()
			elif vendor not in VENDOR_LIST:
				print('Entered vendor not in list of approved vendors.  Please check your spelling')
				continue
			else:
				vendors.append(vendor)
				cont = input("""
				More vendors? (y)es or (n)o
				""")
				if cont == 'n':
					check = False
				elif cont == 'y':
					continue	
				else:
					print('Invalid input.  Exiting...')
					exit()
					
		print(vendors)
		populate_db(vendors)
	
	elif user_input == 'b':
		print('Exiting...')
		exit()
	else:
		print('Invalid input. Exiting...')
	return None













