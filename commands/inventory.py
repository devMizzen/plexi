import os
import sys
import json
import pymongo
import discord

from discord.utils import get
from discord.ext import commands
from pymongo import MongoClient as mongo

token = os.environ["token"]

bot = commands.Bot(command_prefix='/')

'''

async def log(bot, id, dataType, data):
	
	slotCtr = 0
	color = 0x00ff00
	if dataType == "dict":
		emb = discord.Embed(title = "Your Inventory:", description="All stuff present in your inventory will be shown here:", color=color)
		for key in data:
			if key in ("_id", "isEmpty"):
				continue
			if key == "lh":
				name = "Left hand"
			elif "slot" in key:
				slotCtr += 1
				if slotCtr >= 10:
					name = "Slot "+ key[-2]+key[-1]
				else:
					name = "Slot "+key[-1]
				
			else:
				name = key

			emb.add_field(name=name,value=data[key])

	elif dataType == "text":
		emb = discord.Embed(title = "Your Inventory:", description=data, color=color)

	user = bot.get_user(int(id))

	await user.send("h")
	
	dmChannel = user.dm_channel()
	if dmChannel == None:
		dmChannel = user.create_dm()
	await dmChannel.send(embed=emb)

	#ctx.send(embed=emb)'''

'''cluster = mongo(os.environ["MONGOLAB_URL"])  #Same as process.env.MONGO_URL

containers = cluster['Containers']
inventories = containers["Inventories"]

dependancies = cluster['Dependancies']
values = dependancies["Values"]

id = str(sys.argv[1])

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
		
		log(bot, id, "dict", data)
				
	else:
		msg = "Your inventory is empty."
		log(bot, id, "text", msg)
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
	msg = "Your inventory is empty."
	log(bot, id, "text", msg)
'''
@bot.event
async def on_ready():
	result = 0
	print(result)
	sys.stdout.flush()	

bot.run(token)