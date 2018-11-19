import pymongo
from pprint import pprint

#NOTE if mongo is not running, check AMPPS
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

#dictionary, database identifier and collection identifier all passed in here.
#The function checks if the database exists or not
def dict_to_mongo(d, db_ident, coll_ident):
	db = client[db_ident]
	coll = db[coll_ident]
	coll.insert_one(d)
	print(db.list_collection_names())
	results = coll.find()
	for result in results:
		pprint(result)
	#client.drop_database('Test')
	

"""test_dict = {
		'Part Number': [249903, 783920, 756874],
		'Vendor': ['Vendor1', 'Vendor5', 'Vendor265'],
		'Location': ['Some Path1', 'Some Path 2']}

dict_to_mongo(test_dict, 'Test', 'iProp_conv_test')

db = client['Test']
coll = db['iProp_conv_test']

results = coll.find()
for result in results:
	print('After function:')
	pprint(result['Part Number'])
"""






