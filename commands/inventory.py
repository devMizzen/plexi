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

if pre_existance == True:

	data = player.find_one("_id": "inventory")
	isEmpty = data["isEmpty"]
	'''isEmpty = "True"
	for slot in data:
		if (data[slot] != "--"):
			if slot != "isEmpty" or slot != "_id":
				isEmpty = "False"'''
					
	if isEmpty == False:
		
		inventory["_id"] = "inventory"
		inventory["lh"] = data["lh"]
		for i in range(32):
			slotNo = "slot"+ str(i+1)
			inventory[slotNo] = data[slotNo]
		inventory["head"] = data["head"]
		inventory["chest"] = data["chest"]
		inventory["torso"] = data["torso"]
		inventory["shoe"] = data["shoe"]
		inventory["isEmpty"] = "False"
		dependancies.find_one_and_replace(
			{"_id": "inventory", inventory}
		)
			
				
	else:
		inv = dependancies.update_one(
			{"_id": "inventory"}.
			{
				"$set" {
					"_id": id
					"isEmpty": True
				}
			}
	

	
			#print(result)
			#sys.stdout.flush()

else:
	
	inventory["_id"] = "inventory"
	inventory["lh"] = None
	for i in range(32):
		slotNo = "slot"+ str(i+1)
		inventory[slotNo] = None
	inventory["head"] = None
	inventory["chest"] = None
	inventory["torso"] = None
	inventory["shoe"] = None
	inventory["isEmpty"] = True
	player.insert_one(inventory)
	tempInv = dependancies.find_one_and_replace(
		{"_id": "inventory"},
		inventory
	)

result