#script to move things to and from mongo
import sys
sys.path.insert(0, r"Z:\CEG\Software Development\python_config\inventor")

import time

import pymongo
from pprint import pprint
from bson.objectid import ObjectId
#for connecting to remote database:
from sshtunnel import SSHTunnelForwarder

from mongo_remote_config import MONGO_HOST, SSH_USER, SSH_PASSWORD, REMOTE_IP, REMOTE_PORT


#connection = f'mongodb://{MONGO_HOST}'
#client = pymongo.MongoClient(connection)
#conn = 'mongodb://localhost:27017'
#client = pymongo.MongoClient(conn)

#Database is now located on srv01!
#NOTE, not sure if I'll do it this way
def connect_to_remote(db_name, coll_name):			
	server = SSHTunnelForwarder(
			MONGO_HOST,
			ssh_username=SSH_USER,
			ssh_password=SSH_PASSWORD,
			remote_bind_address=(REMOTE_IP, REMOTE_PORT)
			)
	server.start()
	time.sleep(5)
	
	client = pymongo.MongoClient(REMOTE_IP, server.local_bind_port)

	return server, client, #db, collection


#need to pass in the database and collection that you want to insert values into
def first_to_mongo(items, db_ident, coll_ident):
	#get the remote server connection, database and collection
	mongo_tuple = connect_to_remote(db_ident, coll_ident)
	server = mongo_tuple[0]	
	client = mongo_tuple[1]	
	db = client[db_ident] 
	coll = db[coll_ident]	
	#NOTE this assumes that items contains multiple documents.  For the most part, I assume this is how things will go.  If this changes, we'll have to
	#put an if statement in or something.
	inserted_ids = coll.insert_many(items).inserted_ids
	#close the ssh connection	
	client.close()		
	server.close()	
	return inserted_ids 


#NOTE this works ONLY if we have 1 column and 1 criteria but it is a start.
def from_mongo(db_ident, coll_ident, df, query={}):
	#reads from mongodb
	mongo_tuple = connect_to_remote(db_ident, coll_ident)
	server = mongo_tuple[0]	
	client = mongo_tuple[1]
	db = client[db_ident]
	coll = db[coll_ident]

	#if the passed in dataframe is not empty, construct the query
	if not df.empty:https://www.youtube.com/watch?v=UUUVi3BKLto
		print(df)		
		#NOTE this is the column name, not the collection
		col = str(list(df.columns)[0])	
		value = str(df[col].values[0])
		query = {col: value}
	
	cursor = list(coll.find(query))
	#for doc in list(cursor):	
		#pprint(doc)
	#NOTE, why is the close() function not working but del does?	
	client.close()		
	server.close()		
	#del client
	#del server
	#pprint(threading.enumerate())	
	return list(cursor)


def update_mongo(db_ident, coll_ident, df):	
	mongo_tuple = connect_to_remote(db_ident, coll_ident)
	server = mongo_tuple[0]	
	client = mongo_tuple[1]	
	db = client[db_ident]
	coll = db[coll_ident]

	i = 0	
	for _id in df['_id']:
		for prop in list(df.columns):
			if prop != '_id':	
				coll.update(
						{'_id': ObjectId(_id)},
						{'$set': 
							{prop: df[df['_id'] == _id][prop].item()}})	
	client.close()		
	server.close()		
	return None
						












