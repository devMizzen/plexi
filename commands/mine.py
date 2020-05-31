#---------------------------------------------------------#
#						Libraries						  #
#---------------------------------------------------------#

import pymongo
import os
import random
import sys
import math

from pymongo import MongoClient as mongo

cluster = mongo(os.environ["MONGO_URL"])
db = cluster["plexi_users"]
player = db[id]
dependancies = db["Dependancies"]

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
	"Wood Pickaxe": 1
	"Stone Pickaxe": 2
	"Iron Pickaxe": 3
	"Diamond Pickaxe": 4
	"Gold Pickaxe": 5
}

itemGained = []

#---------------------------------------------------------#
#						  Input							  #
#---------------------------------------------------------#

user = sys.argv[1]
#eq = sys.argv[2]
t = sys.argv[2]

playerInv = player.find_one({"_id": "inventory"})
numPicks = 0

for slot in playerInv:
	entity = playerInv[slot]
	if "Pickaxe" in entity:
		toolType = entity[3::]
		numPicks += 1
		
if numPicks == 0:
	eq = 0
else:
	eq = pickIDs[toolType]



'''user = input("Enter name: ")
eq = input("Enter equipment: ")
t = input("Enter Time in seconds: ")
numPicks = int(input("Enter num of picks: "))'''


#---------------------------------------------------------#
#						Functions						  #
#---------------------------------------------------------#

def mine_start(user,time,eq,numPicks):
	dur = time
	eq = int(eq)
	space = availableSpace(user)
	breakTime = pickSpeed[eq]*1.5
	#hold = math.ceil(dur/layerTime)
	print(dur, round(dur/breakTime))
	print("----------------------")
	timer = 0
	try:
		durability = pickBlocks[eq]*numPicks
	except:
		durability = 'inf'
	while timer < round(dur/breakTime) and space > 0:
		for entity in range(len(probs)):
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
							break
					if itemName[0] in ('Redstone Ore', 'Lapis Lazuli Ore'):
						if itemName[0] == 'Redstone Ore':
							fac = random.randint(4,5)
							qty = fac
						elif itemName[0] == 'Lapis Lazuli Ore':
							fac = random.randint(4,9)
							qty = fac

					if timer >= round(dur/breakTime):
						qty = round(dur/breakTime)
						
						if itemName[0] in itemGained:
							for x in range(len(itemGained)):
								if itemName[0] == itemGained[x] and itemGained[x+1] <64:
									if itemGained[x+1] + qty <= 64:
										itemGained[x+1] += qty
										qty = 0
										break
									else:
										itemGained[x+1] = 64
										qty = qty - (64-itemGained[x+1])
										continue
											
								else:
									continue

							while qty != 0:
								if space >= qty:
									if qty <= 64:
										itemGained.extend([itemName[0],qty])
										qty = 0
									else:
										itemGained.extend([itemName[0],64])
										qty -= 64
								elif space < qty:
									qty = space
									if qty <= 64:
										itemGained.extend([itemName[0],qty])
										qty = 0
									else:
										itemGained.extend([itemName[0],64])
										qty -= 64
										
						else:
							while qty!=0:
								if space >= qty:
									if qty <= 64:
										itemGained.extend([itemName[0],qty])
										qty = 0
									else:
										itemGained.extend([itemName[0],64])
										qty -= 64
								else:
									qty = space
									if qty <= 64:
										itemGained.extend([itemName[0],qty])
										qty = 0
									else:
										itemGained.extend([itemName[0],64])
										qty -= 64
									
						break
					else:
						if itemName[0] in itemGained:
							for x in range(len(itemGained)):
								if itemName[0] == itemGained[x] and itemGained[x+1] <64:
									if itemGained[x+1] + qty <= 64:
										itemGained[x+1] += qty
										qty = 0
										
									elif itemGained[x+1] + qty > 64:
										itemGained[x+1] = 64
										qty -= (64-itemGained[x+1])
										continue
							while qty != 0:
								if space >= qty:
									if qty <= 64:
										itemGained.extend([itemName[0],qty])
										qty = 0
									else:
										itemGained.extend([itemName[0],64])	
										qty -= 64
								else:
									qty = space
									if qty <= 64:
										itemGained.extend([itemName[0],qty])
										qty = 0
									else:
										itemGained.extend([itemName[0],64])	
										qty -= 64
												
						else:
							while qty > 0:
								if space >= qty:
									if qty <= 64:
										itemGained.extend([itemName[0],qty])
										qty = 0
									else:
										itemGained.extend([itemName[0],64])
										qty -= 64
								else:
									qty = space
									if qty <= 64:
										itemGained.extend([itemName[0],qty])
										qty = 0
									else:
										itemGained.extend([itemName[0],64])
										qty -= 64								
				else:
					continue
			else:
				if eq > 0:
					if 'Stone' in itemGained:
						qty = 1
						for x in range(len(itemGained)):
							if 'Stone' == itemGained[x]:
								if itemGained[x+1] < 64:
									itemGained[x+1] += 1
									qty = 0

							else:
								continue
						if qty == 1 and space != 0:
							itemGained.extend(['Stone',1])
					else:
						if space != 0:
							itemGained.extend(['Stone',1])

		timer += 1

def raiseError(ctx, errorCode):
	print(errorCode)

def getSize(itemName):
	itemSize = dependancies.find_one(
		{"_id": "sizeList"}, 
		projection = {itemName: True}
	)
	return int(itemSize)
	
def availableSpace(id):
	data = player.find_one({"_id": "inventory"})

	qty = ''
	inventorySpace = 0

	for slot in data:
		if slot in ('head','chest','torso','shoe','isEmpty'):
			continue
		for ch in data[slot]:
			if ch == 'x' or ch == '-':
				break
			else:
				qty += ch
		ctr = 1
		for ch in data[slot]
			if ch != " ":
				ctr += 1
				continue
			else:
				break
		itemName = data[slot][ctr::]
		size = getSize(itemName)
		slotSpace = 64 - (int(qty)*size)
		inventorySpace += slotSpace
	return inventorySpace

#---------------------------------------------------------#
#					Main Function						  #
#---------------------------------------------------------#

def mine(user, *args):
	
	if args[0] == 'stop':
		mine_stop(user)
	
	time = int(t)
	numPicks = args[2]
	mine_start(user,time,eq,numPicks)

#---------------------------------------------------------#
#						  Run							  #
#---------------------------------------------------------#

if eq == 0:
	numPicks = 0
mine(user, eq, t, numPicks)	

for x in range(len(itemGained)):
	if x%2 == 1:
		continue
	print(itemGained[x],itemGained[x+1])