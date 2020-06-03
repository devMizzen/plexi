import os
import sys
import json
import pymongo

from pymongo import MongoClient as mongo

id = str(sys.argv[1])

cluster = mongo(os.environ["MONGOLAB_URL"])  #Same as process.env.MONGO_URL

'''db = cluster['plexi_users']
player = db[str(id)]
dependancies = db['Dependancies']'''

containers = cluster['Containers']
inventories = db["Inventories"]

dependancies = cluster['Dependancies']
injectors = dependancies["Injectors"]

inventory = {}

userList = injectors.find_one({"_id":"UserList"})
if userList == None:
	injectors.insert_one({"_id": "UserList"})
	userList = injectors.find_one({"_id":"UserList"})
if id in userList:
	pre_existance = True
else:
	pre_existance = False
	injectors.update_one(
		{"_id": "UserList"},
		{
			"$set": {str(id): None}}
		},
		upsert=True
	) 

result = 0
print(result)
sys.stdout.flush()

'''if pre_existance == True:

	data = inventories.find_one({"_id": id})
	isEmpty = data["isEmpty"]
	'''isEmpty = "True"
	for slot in data:
		if (data[slot] != "--"):
			if slot != "isEmpty" or slot != "_id":
				isEmpty = "False"'''
					
	if isEmpty == False:
		
		inventory["_id"] = id
		inventory["lh"] = data["lh"]
		for i in range(32):
			slotNo = "slot"+ str(i+1)
			inventory[slotNo] = data[slotNo]
		inventory["head"] = data["head"]
		inventory["chest"] = data["chest"]
		inventory["torso"] = data["torso"]
		inventory["shoe"] = data["shoe"]
		inventory["isEmpty"] = "False"
		injectors.replace_one(
			{"_id": "inventory"}, 
			{ "$set": inventory}
		)
			
				
	else:
		inv = injectors.update_one(
			{"_id": "inventory"},
			{"$set": {
				"ID": id,
				"isEmpty": True
				}
			}
		)
			#print(result)
			#sys.stdout.flush()
else:	
	inventory["_id"] = id
	inventory["lh"] = None
	for i in range(32):
		slotNo = "slot"+ str(i+1)
		inventory[slotNo] = None
	inventory["head"] = None
	inventory["chest"] = None
	inventory["torso"] = None
	inventory["shoe"] = None
	inventory["isEmpty"] = True
	inventories.insert_one(inventory)
	injectors.replace_one(
		{"_id": "inventory"},
		{ "$set": inventory} 
	)

result = 0
print(result)
sys.stdout.flush()'''