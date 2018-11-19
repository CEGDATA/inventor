#script will read the current excel file located at excel_path and return it - will also re-write to the ARCHIVE folder in that directory
#script will receive lists of values from the open_things.py script in order to construct the new dataframe
#script will write new dataframe to the same path

import pandas as pd
import os

#path = "Z:\\CEG\\DRAFTING\\3DManufacturerParts"
#os.chdir(path)

PATH = "Z:\\CEG\\DRAFTING\\3DManufacturerParts\\3DModelDatabase_Jake_work_11072018.xlsx"
#print(PATH)
SHEET = 'Base Data'

def get_excel():
	threed_models_df = pd.read_excel(PATH, sheet=SHEET)
	return threed_models_df

def make_df_send_to_excel(incoming_dict):
	property_df = pd.DataFrame(incoming_dict)
	property_df.to_excel(PATH, sheet_name=SHEET, index=False)
	



