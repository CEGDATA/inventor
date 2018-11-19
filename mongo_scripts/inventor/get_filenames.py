#script will walk through the 3D manufacturing parts directories and return strings for the filepaths to the .ipt files we are interested in
#extracting iProperties from.
#These paths will be given to open_things.py
#NOTE, this whole program likely needs more future proofing but this is a decent start
import os

#NOTE this would be good to get from the excel file, but it is here for now
VENDOR_LIST = ['ANDERSON', 'LAPP'] 
FORBIDDEN = ['OldVersions', 'Import']

def get_ipts():
	ipt_list = []
	for vendor in VENDOR_LIST:
		print(vendor)
		#we want to ignore the first directory being the vendor directory
		i = 0
		for root, dirs, files in os.walk('Z:\\CEG\\DRAFTING\\3DManufacturerParts\\' + vendor):
			dirs[:] = [d for d in dirs if d not in FORBIDDEN]
			if i != 0:
				for f in files:
					if f.endswith('.ipt'):
						full_path = os.path.join(root, f)
						ipt_list.append(full_path)
			i += 1
	return ipt_list












