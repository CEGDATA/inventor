#script to move things to and from mongo
#this is ideally the only script that will ever be directly executed by a user.  But who knows.

import pymongo
from pprint import pprint
from bson.objectid import ObjectId

#NOTE if mongo is not running, check Ampps
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)


#need to pass in the database and collection that you want to insert values into
def first_to_mongo(items, db_ident, coll_ident):
	#print(db_ident)
	db = client[db_ident]
	coll = db[coll_ident]
	#NOTE this assumes that items contains multiple documents.  For the most part, I assume this is how things will go.  If this changes, we'll have to
	#put an if statement in or something.
	inserted_ids = coll.insert_many(items).inserted_ids
	return inserted_ids 
	

def from_mongo(db_ident, coll_ident, query={}):
	#reads from mongodb
	db = client[db_ident]
	coll = db[coll_ident]

	cursor = coll.find(query)
	return list(cursor)


def update_mongo(db_ident, coll_ident, df):
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










