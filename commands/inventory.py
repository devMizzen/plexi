import os
import sys
import json
import pymongo
import discord

from discord.utils import get
from pymongo import MongoClient as mongo


async def log(ctx, dataType, data):

	color = 0x00ff00
	if dataType == "dict":
		emb = discord.Embed(title = "Your Inventory:", description="All stuff present in your inventory will be shown here:", color=color)
		for key in data:
			if key in ("_id", "isEmpty"):
				continue
			if key == "lh":
				name = "Left hand"
			elif "slot" in key:
				name = "Slot "+key[-1]
			else:
				name = key

			emb.add_field(name=name,value=data[key])

	elif dataType == "text":
		emb = discord.Embed(title = "Your Inventory:", description=text, color=color)
		
	await ctx.send(embed=emb)


cluster = mongo(os.environ["MONGOLAB_URL"])  #Same as process.env.MONGO_URL

containers = cluster['Containers']
inventories = containers["Inventories"]

dependancies = cluster['Dependancies']
values = dependancies["Values"]

ctx = sys.argv[1]
id = str(sys.argv[2])

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
		
		log(ctx, "dict", data)
				
	else:
		msg = "Your inventory is empty."
		log(ctx, "text", msg)
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
	
	log(ctx, "dict", inventory)

result = 0
print(result)
sys.stdout.flush()