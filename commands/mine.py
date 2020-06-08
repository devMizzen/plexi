#---------------------------------------------------------#
#						Libraries						  #
#---------------------------------------------------------#

import pymongo
import os
import random
import sys
import math

from pymongo import MongoClient as mongo

cluster = mongo(os.environ["MONGO_LAB"])

containers = cluster['Containers']
inventories = containers["Inventories"]

dependancies = cluster['Database']
values = dependancies['Values']
injectors = dependancies["Injectors"]

#---------------------------------------------------------#
#						Database						  #
#---------------------------------------------------------#

probs = [#			  	qty    prob    pick    break time
	['Dirt',			33,		10,		0,		0.5],
	['Gravel',			33,		8,		0,		0.6],
	['Granite',			33,		10,		1,		1.5],
	['Diorite',			33,		10,		1,		1.5],
	['Andesite',		33,		10,		1,		1.5],
	['Coal Ore',		17,		20,		2,		3],
	['Iron Ore',		9,		20,		2,		3],
	['Redstone Ore',	8,		8,		3,		3],
	['Lapis Lazuli Ore',7,		1,		3,		3],
	['Gold Ore',		9,		2,		3,		3],
	['Diamond Ore',		8,		1,		3,		3]
]

pickSpeed = [
	1.5,#hand
	0.75,#wooden
	0.4,#stone
	0.25,#iron
	0.2,#diamond
	0.15#gold
]

pickBlocks = [
	'hand',
	59,#wooden
	131,#stone
	250,#iron
	1561,#diamond
	32,#gold
]

pickIDs = {
	"Wood Pickaxe": 1,
	"Stone Pickaxe": 2,
	"Iron Pickaxe": 3,
	"Diamond Pickaxe": 4,
	"Gold Pickaxe": 5
}

#itemGained = []
itemGained = {}

#---------------------------------------------------------#
#						  Input							  #
#---------------------------------------------------------#

'''user = str(sys.argv[1])
t = sys.argv[2]

playerInv = inventories.find_one({"_id": user})
numPicks = 0

for slot in playerInv:
	if slot in ("_id", "isEmpty"):
		continue
	entity = playerInv[slot]
	if "Pickaxe" in entity:
		toolType = entity[3::]
		numPicks += 1
		
if numPicks == 0:
	eq = 0
else:
	eq = pickIDs[toolType]'''

user = input("Enter name: ")
eq = int(input("Enter equipment: "))
t = input("Enter Time in seconds: ")
numPicks = int(input("Enter num of picks: "))


#---------------------------------------------------------#
#						Functions						  #
#---------------------------------------------------------#

def mine_start(user,time,eq,numPicks):
	dur = time
	eq = int(eq)
	space = availableSpace(user)
	breakTime = pickSpeed[eq]*1.5
	#hold = math.ceil(dur/layerTime)
	print("Time: "+str(dur))
	print("Blocks: "+str(math.floor(dur/breakTime)))
	print("----------------------")
	timer = 0
	try:
		durability = pickBlocks[eq]*numPicks
	except:
		durability = 'inf'
	while timer < math.floor(dur/breakTime) and space > 0:
		for entity in range(len(probs)):
			if timer >= math.floor(dur/breakTime)-1:
				return
			space = availableSpace(user)
			itemName = probs[entity]
			hit = random.randint(1,100)
			prob = itemName[2]
			print(durability)
			try:
				if durability == 'inf':
					eq = 0
			except:
				eq = 0
			if durability != 'inf':
				if durability > 0:
					durability -= 1
				else:
					durability = 'inf'
					eq = 0
					breakTime = 1.5
			if hit <= prob:
				if itemName[3] <= eq:
					qty = random.randint(1,itemName[1])
					for i in range(qty):
						if timer <dur:
							timer += itemName[4]*pickSpeed[eq]
						else:
							qty = math.floor(timer)
							break
					if itemName[0] in ('Redstone Ore', 'Lapis Lazuli Ore'):
						if itemName[0] == 'Redstone Ore':
							fac = random.randint(4,5)
							qty = fac
						elif itemName[0] == 'Lapis Lazuli Ore':
							fac = random.randint(4,9)
							qty = fac

					if timer >= math.floor(dur/breakTime):
						#qty = math.floor(dur/breakTime)
						qty = timer
						
						if itemName[0] in itemGained:
							#for x in range(len(itemGained)):
							for x in itemGained:
								#if itemName[0] == itemGained[x] and itemGained[x+1] <64:
								if itemName[0] == x and itemGained[x] <64:
									#if itemGained[x+1] + qty <= 64:
									if itemGained[x] + qty <= 64:
										#itemGained[x+1] += qty
										itemGained[x] += qty
										qty = 0
										break
									else:
										#itemGained[x+1] = 64
										itemGained[x] = 64
										#qty = qty - (64-itemGained[x+1])
										qty = qty - (64-itemGained[x])
										continue
											
								else:
									continue

							while qty != 0:
								if space >= qty:
									if qty <= 64:
										#itemGained.extend([itemName[0],qty])
										itemGained[itemName[0]] = qty
										qty = 0
									else:
										#itemGained.extend([itemName[0],64])
										itemGained[itemName[0]] =64
										qty -= 64
								elif space < qty:
									qty = space
									if qty <= 64:
										#itemGained.extend([itemName[0],qty])
										itemGained[itemName[0]] = qty
										qty = 0
									else:
										itemGained[itemName[0]]= 64
										qty -= 64
										
						else:
							while qty!=0:
								if space >= qty:
									if qty <= 64:
										itemGained[itemName[0]]=qty
										qty = 0
									else:
										itemGained[itemName[0]]=64
										qty -= 64
								else:
									qty = space
									if qty <= 64:
										itemGained[itemName[0]]=qty
										qty = 0
									else:
										itemGained[itemName[0]]=64
										qty -= 64
									
						return
					else:
						timer += qty
						if itemName[0] in itemGained:
							#for x in range(len(itemGained)):
							for x in itemGained:
								if itemName[0] == x and itemGained[x] <64:
									if itemGained[x] + qty <= 64:
										itemGained[x] += qty
										qty = 0
										
									elif itemGained[x] + qty > 64:
										itemGained[x] = 64
										qty -= (64-itemGained[x])
										continue
							while qty != 0:
								if space >= qty:
									if qty <= 64:
										itemGained[itemName[0]]=qty
										qty = 0
									else:
										itemGained[itemName[0]]=64	
										qty -= 64
								else:
									qty = space
									if qty <= 64:
										itemGained[itemName[0]]=qty
										qty = 0
									else:
										itemGained[itemName[0]]=64
										qty -= 64
												
						else:
							while qty > 0:
								if space >= qty:
									if qty <= 64:
										itemGained[itemName[0]]=qty
										qty = 0
									else:
										itemGained[itemName[0]]=64
										qty -= 64
								else:
									qty = space
									if qty <= 64:
										itemGained[itemName[0]]=qty
										qty = 0
									else:
										itemGained[itemName[0]]=64
										qty -= 64								
				else:
					continue
			else:
				if eq > 0:
					if timer >= math.floor(dur/breakTime):
						return
					if 'Stone' in itemGained:
						qty = 1
						timer += 1
						for x in itemGained:
							if 'Stone' == x:
								if itemGained[x] < 64:
									itemGained[x] += 1
									qty = 0

							else:
								continue
						if qty == 1 and space != 0:
							itemGained['Stone']=1
					else:
						if space != 0:
							itemGained['Stone']=1

		

def getSize(itemName):						#  <------- WIP
	itemSize = values.find_one(
		{"_id": "sizeList"}, 
		projection = {itemName: True}
	)
	return int(itemSize)
	
def availableSpace(id):
	data = inventories.find_one({"_id": id})

	
	inventorySpace = 0

	for slot in data:
		qty = ''
		if slot in ("_id", 'head','chest','torso','shoe','isEmpty'):
			continue

		if data[slot] != None:
			for ch in data[slot]:
				if ch == 'x':
					break
				else:
					qty += ch
			ctr = 1
			for ch in data[slot]:
				if ch != " ":
					ctr += 1
					continue
				else:
					break
			itemName = data[slot][ctr::]
			#size = getSize(itemName)
			#slotSpace = 64 - (int(qty)*size)
			slotSpace = 64 - int(qty)
		else:
			slotSpace = 64
		inventorySpace += slotSpace
	return inventorySpace

def inventorize(id, _dict):
	playerInv = inventories.find_one(
		{"_id": id}
	)
	
	
	playerInv.pop('_id')
	playerInv.pop('head')
	playerInv.pop('chest')
	playerInv.pop('torso')
	playerInv.pop('shoe')
	playerInv.pop('isEmpty')
	for item in _dict:
		qty = _dict[item]
		for slot in playerInv:
			if playerInv[slot] == None or slot in ("_id","head","chest","torso","shoe","isEmpty"):
				continue
			if item in playerInv[slot]:
				slotqty = ''
				for ch in playerInv[slot]:
					if ch == "x":
						break
					slotqty += ch
				slotqty = int(slotqty)
				if slotqty + qty <= 64:
					playerInv[slot] = str(slotqty+qty)+"x "+item
					qty = 0
					break
				else:
					playerInv[slot] = "64x "+item
					qty -= (64-slotqty)
		while qty != 0:
			for Slot in playerInv:
				if qty == 0:
					break
				if playerInv[Slot] == None:
					if qty <= 64:
						playerInv[Slot] = str(qty)+"x "+item
						qty = 0
						break
					else:
						playerInv[Slot] = "64x "+item
						qty -= (64-slotqty)	
	
	inventories.update_one(
		{"_id": id},
		{"$set": playerInv}
	)

#---------------------------------------------------------#
#					Main Function						  #
#---------------------------------------------------------#

def mine(user, *args):
	
	if args[0] == 'stop':
		mine_stop(user)
	
	eq = args[0]
	time = int(args[1])
	numPicks = args[2]
	mine_start(user,time,eq,numPicks)

#---------------------------------------------------------#
#						  Run							  #
#---------------------------------------------------------#

if eq == 0:
	numPicks = 0
mine(user, eq, t, numPicks)	

injector = {}
print(itemGained)
for x in itemGained:
	print(x,itemGained[x])

inventorize(user, itemGained)

	
	


	