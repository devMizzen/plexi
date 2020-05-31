import os
import sys
import json
import pymongo

from pymongo import MongoClient as mongo

id = str(sys.argv[1])

cluster = mongo(os.environ["MONGOLAB_URL"])  #Same as process.env.MONGO_URL
db = cluster['plexi_users']
player = db.id
dependancies = db['Dependancies']

inventory = {}

userList = dependancies.find_one({"_id":"UserList"})
if userList == None:
	dependancies.insert_one({"_id": "UserList"})
	userList = dependancies.find_one({"_id":"UserList"})
if id in userList:
	pre_existance = True
else:
	pre_existance = False
	userList = dependancies.find_one_and_update(
		{"_id": "UserList"},
		{
			"$set": {id: None}
		},
		upsert=True
	) 

result = 0
print(result)
sys.stdout.flush()

