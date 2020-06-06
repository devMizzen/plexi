import os
import sys
import json
import pymongo

from pymongo import MongoClient as mongo

id = str(sys.argv[1])

cluster = mongo(os.environ["MONGOLAB_URL"])

containers = cluster['Containers']
inventories = containers["Inventories"]

dependancies = cluster['Database']
values = dependancies['Values']
injectors = dependancies["Injectors"]

inventory = {}

userList = values.find_one({"_id":"UserList"})
if userList == None:
	values.insert_one({"_id": "UserList"})
	userList = values.find_one({"_id":"UserList"})
if id in userList:
	pre_existance = True
else:
	pre_existance = False
	values.update_one(
		{"_id": "UserList"},
		{"$set": {id: None}},
		upsert=True
	) 

if pre_existance == True:

	data = inventories.find_one({"_id": id})
	isEmpty = data["isEmpty"]
					
	if isEmpty == False:
		
		ctr = 1
		injector = {}
		for slot in data:
			if slot == "_id":
				continue

			name = slot

			if data[slot] == None:
				value = "--"
			else:
				value = data[slot]

			injector[name] = value

		'''inventory["lh"] = data["lh"]
		for i in range(32):
			slotNo = "slot"+ str(i+1)
			inventory[slotNo] = data[slotNo]
		inventory["head"] = data["head"]
		inventory["chest"] = data["chest"]
		inventory["torso"] = data["torso"]
		inventory["shoe"] = data["shoe"]
		inventory["isEmpty"] = "False"'''
		injectors.update_one(
			{"_id": "inventory"}, 
			{ "$set": injector},
			upsert=True
		)
			
				
	else:
		inv = injectors.update_one(
			{"_id": "inventory"},
			{"$set": {
				"isEmpty": True
				}
			},
			upsert=True
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

	ctr = 1
	injector = {}
	for slot in inventory:
		if slot == "_id":
			continue

		name = slot

		if data[slot] == None:
			value = "--"
		else:
			value = data[slot]

		injector[name] = value

	injectors.update_one(
		{"_id": "inventory"},
		{"$set": injector},
		upsert = True
	)

result = 0
print(result)
sys.stdout.flush()