#script to read data from mongodb, put into pandas dataframe and write to excel.
#will be similar to putting the data on the website, these may be combined at some point.
import pandas as pd



def mongo_to_dataframe(documents):
	mongo_df = pd.DataFrame(documents)
	#removes the mongodb id from the dataframe	
	#mongo_df.drop('_id', axis=1, inplace=True)
	return mongo_df

def send_to_excel(df, first_columns, excel_path):
	#for display purposes, doesn't actually change
	#NOTE, we could have the user input the columns, and have pandas order the columns that way
	df = df[first_columns + [c for c in list(df.columns) if c not in first_columns]]	
	df.to_excel(excel_path, index=False)

def get_from_excel(excel_path, sheet):
	#get the dataframe		
	df = pd.read_excel(excel_path, sheet_name=sheet)
	#df_json = df.to_json(orient='records')
	#mongo might not like nans, so we are going to replace them with empty strings
	df.fillna('', inplace=True)
	return df





