#script to read data from mongodb, put into pandas dataframe and write to excel.
#will be similar to putting the data on the website, these may be combined at some point.
import pandas as pd

EXCEL_PATH = r"Z:\CEG\DRAFTING\3DManufacturerParts\3DModelDatabase_Jake_work_11152018.xlsx"
FIRST_COLUMNS = ['Vendor', 'Part Number']

def mongo_to_dataframe(documents):
	mongo_df = pd.DataFrame(documents)
	#removes the mongodb id from the dataframe	
	#mongo_df.drop('_id', axis=1, inplace=True)
	return mongo_df

def send_to_excel(df):
	#for display purposes, doesn't actually change
	#NOTE, we could have the user input the columns, and have pandas order the columns that way
	df = df[FIRST_COLUMNS + [c for c in list(df.columns) if c not in FIRST_COLUMNS]]
	print(df)	
	df.to_excel(EXCEL_PATH, index=False)

def get_from_excel():
	#get the dataframe	
	df = pd.read_excel(EXCEL_PATH)
	#df_json = df.to_json(orient='records')
	#mongo might not like nans, so we are going to replace them with empty strings
	df.fillna('', inplace=True)
	return df





