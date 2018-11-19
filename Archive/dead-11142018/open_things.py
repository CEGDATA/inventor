#Script will open inventor and all .ipt files we are concerned with
#Script will extract the iProperties we are concerned with
#Script will send lists of iProperties and file location, etc. to read_write_excel, where they will be written into a dataframe and written to a 
#new excel file.


#NOTE ON THE DICTIONARY:
#The reasons for creating a dictionary and then converting to a dataframe later are:
#1. It allows us to be flexible for future property needs - If we needed to declare a list for each property, we would have to update the code every
#time a new property was needed.  
#2. We needed a way to "name" the lists without different variables.  The lists are now defined by their key in the dictionary - and these are 
#extracted from the orginal file.
import win32com.client
from win32com.client import gencache
import get_filenames as f
import read_write_excel as excel
import to_mongo as mongo
import os

#NOTE just for testing the db
import pymongo
from pprint import pprint

#these are not extracted from the api, but from the file path string
NOT_IN_API = ['Filename w/o Extension', 'Found Location']

def open_inventor():
	#opens inventor
	inventor = win32com.client.Dispatch('Inventor.Application')
	#decide if you want the app to be visible or not - NOTE uncomment to set visible
	#inventor.Visible = True

	#NOTE I don't know what this line actually does.
	#Here's a link to a potentially helpful article I haven't read yet
	#http://www.icodeguru.com/WebServer/Python-Programming-on-Win32/ch12.htm
	mod = gencache.EnsureModule('{D98A091D-3A0F-4C3E-B36E-61F62068D488}', 0, 1, 0)
	return inventor, mod
	
def get_structure():
	#get the current excel file
	current_df = excel.get_excel()	
	#get the list of ipt files we are concerned with
	parts_list = f.get_ipts()	
	return current_df, parts_list

def extract(prop, prop_set, part, prop_dict):
	#get the value of the iproperty
	i_prop = prop_set(prop).Value
	#append the appropriate list within the dictionary	
	prop_dict[prop].append(i_prop)
	return prop_dict

def get_data(df, parts, app, mod):
	#now we get the properties we want
	#these can be extracted from the dataframe column names, but we also have the filename and the path which are not properties we can extract
	#from iProperties
	cols = df.columns.tolist()
	print(cols)
	inv_properties = [p for p in cols if p not in NOT_IN_API]
	print(inv_properties)

	our_properties_dict = {}
	for prop in cols:
		our_properties_dict[prop] = []
		print(our_properties_dict)

	for part in parts:
		#open the .ipt file in inventor	
		app.Documents.Open(part)
		#gets the document as whatever the open document in inventor is
		doc = app.ActiveDocument
		#NOTE, we may have to dive into other property sets, but for now we will just use Design Tracking Properties
		#a list of all of the sets and what properties can be extracted from them is here:
		#https://forums.autodesk.com/t5/inventor-customization/get-set-iproperty-directly-with-id-enum/td-p/5124654
		design_props = doc.PropertySets.Item('Design Tracking Properties')

		#update our dictionary with all of the lists with the key as the property we are looking at
		for prop in inv_properties:
			our_properties_dict = extract(prop, design_props, part, our_properties_dict)
			print(our_properties_dict)
		#split the part filepath on the backslashes (directory changes).  The last value of this list is the filepath	
		#then, we split on the period, which indicates the file extension, and get the 0th value in this list	
		filename_wo_extension = part.split('\\')[-1].split('.')[0]
		#get the found location and the filename and add them to their locations in the dictionary
		#os.path.dirname() converts the string to the directory path - does not include the filename
		found_location = os.path.dirname(part)
		print(our_properties_dict)
		our_properties_dict['Filename w/o Extension'].append(filename_wo_extension)
		our_properties_dict['Found Location'].append(found_location)

		app.Documents.CloseAll()
	#close inventor after we have extracted the data we are interested in
	app.Quit()
	return our_properties_dict


inventor, mod = open_inventor()
current_df, parts_list = get_structure()
#print(current_df)
#print(parts_list)
property_dict = get_data(current_df, parts_list, inventor, mod)
print(property_dict)
excel.make_df_send_to_excel(property_dict)
"""mongo.dict_to_mongo(property_dict, 'InventorDB', 'iProp_Collection')

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

db = client['InventorDB']
coll = db['iProp_Collection']

results = coll.find()
for result in results:
	pprint(result)"""




