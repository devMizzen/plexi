#---------------------------------------------------------#
#						Libraries						  #
#---------------------------------------------------------#

import sys
import pymongo

from pymongo import MongoClient as mongo

#---------------------------------------------------------#
#						Dependancies					  #
#---------------------------------------------------------#

id = sys.argv[1]

global cluster = mongo(os.environ["MONGO_URL"])  #Same as process.env.MONGO_URL
global db = cluster["Containers"] 
global player = db["Inventories"]

global dpd = cluster["Dependancies"]
global dependancies = dpd["Database"]
global injectors = dpd["Injectors"]

global numOfEntities = len(dependancies.find_one({"_id": "entityIDs"},))

#---------------------------------------------------------#
#						Functions						  #
#---------------------------------------------------------#

def getSize(item):
	itemSizes = dependancies.find_one(
		{"_id": "ItemSizes"}
		projection={item: True}
	) 
	return itemSizes

def getQty(item):
	playerInv = player.find_one({"_id": id})
	invQty = 0
	for slot in playerInv:
		if slot == "isEmpty":
			continue
		itemQty = ''
		if item in playerInv[slot]:
			for ch in playerInv[slot]:
				if ch == 'x' or ch == '-':
					break
				itemQty += ch
			invQty += int(itemQty)
	return(invQty)
	
def setQty(item, method, invQty, qty):

	playerInv.find_one(
		{"_id": id},
		projection={
			"_id": False,
			"isEmpty": False
		}
	)
	if method == "sub":
		while qty != 0:
			for slot in playerInv:
				if item in playerInv[slot] and qty != 0:
					itemQty = ''
					for ch in playerInv[slot]:
						if ch == 'x':
							break
						itemQty += ch
					itemQty = int(itemQty)
					if itemQty == 64:
						continue
					if itemQty-qty in range(1, 65):
						player.update_one(
							{"_id": id},
							"$set": {slot: str(itemQty-qty)+"x "+item}}
						)
						qty = 0
						break
					
					elif itemQty-qty = 0:
						player.update_one(
							{"_id": id},
							"$set": {slot: None}	
						)
						qty = 0
						break
					
					else:
						player.update_one(
							{"_id": id},
							"$set": {slot: None}
						)
						qty -= (64-itemQty)
	
	elif method == 'add':
#		while qty != 0:
			for slot in playerInv:
				if item in playerInv[slot] and qty != 0:
					itemQty = ''
					for ch in playerInv[slot]:
						if ch == 'x':
							break
						itemQty += ch
					itemQty = int(itemQty)
					if itemQty == 64:
						continue
					if itemQty+qty <= 64:
						player.update_one(
							{"_id": id},
							"$set": {slot: str(itemQty+qty)+"x "+item}}
						)
						qty = 0
						break
					
					else:
						player.update_one(
							{"_id": id},
							"$set": {slot: "64x "+item}	
						)
						qty -= (64-itemQty)
					
			while qty != 0:
				for slot in playerInv and qty != 0:
					if playerInv[slot] == None:
						if qty <= 64:
							player.update_one(
								{"_id": id},
								"$set": {slot: str(qty)+"x "+item}
							)
							qty = 0
							break
							
						else:
							player.update_one(
								{"_id": id},
								"$set": {slot: "64x "+item}
							)
							qty -= 64
							
def price(item):
	itemPrices = dependancies.find_one({"_id": "itemPrices"})
	itemPrice = int(itemPrices[item])
	return itemPrice
	
def inventory(method, itemName, *arg):
	if method == 'chk':
		invQty = getQty(itemName)
		if invQty >= qty:
			return True
		else:
			return False

	elif method == "sub":
		SubQty = args[0]
		invQty = getQty(itemName)
		setQty(itemName, method, invQty, SubQty)
		
	elif method == 'add':
		addQty = args[0]
		invQty = getQty(itemName)
		setQty(itemName, method, invQty, addQty)
		
	else:
		item = itemName
		reqSpace = args[0]
		size = args[1]
		
		invQty = getQty(item)
		if invQty >= reqSpace*size:
			return True
		else:
			return False
	
def balance(id, method, amnt):
	economy = cluster["Economy"]
	bal = economy["Balance"]
	
	if method == "chk":
		playerBal = bal.find_one(
			{"_id": id},
			projection={money: True}
		)
		return playerBal
	
	elif method == "add":
		crntBal = bal.find_one(
			{"_id": id},
			projection = {money: True}
		)
		bal.update_one(
			{"_id": id},
			"$set": {money: crntBal+amnt}
		)
	
	elif method == 'sub':
		crntBal = bal.find_one(
			{"_id": id},
			projection = {money: True}
		)
		bal.update_one(
			{"_id": id},
			"$set": {money: crntBal-amnt}
		)
#---------------------------------------------------------#
#						  Main  						  #
#---------------------------------------------------------#

item = sys.argv[3]
if sys.argv[2].lower() != "price":
	qty = sys.argv[4]
	
	size = getSize(item)

if sys.argv[1].lower() == 'sell':	
	itemPrice = price(item)
	Credit = itemPrice*qty
	if inventory(id, "chk", itemName, qty) == True:
		balance(id, "add", Credit)
		inventory(id, "sub", itemName, qty)
	else:
		injectors.insert_one(
			{"_id": "ErrorCode",
			"Error": "Not enough items in inventory"}
		)
	
elif sys.argv[1].lower() == 'buy':
	itemPrice = price(item)
	Credit = itemPrice*qty
	
	bal = balance(id, "chk", Credit)
	inv = inventory(id, "space", item, qty, size)
	if bal == True and inv == True:
		balance(id, "sub", Credit)
		inventory(id, "add", itemName, qty, size)
	
	elif bal == True and inv == False:
		injectors.insert_one(
			{"_id": "ErrorCode",
			"Error": "Not enough space in inventory"}
		)
		
	else:
		injectors.insert_one(
			{"_id": "ErrorCode",
			"Error": "Not enough balance to make the purchase"},
		)
		
elif sys.argv[1].lower() == "price":
	itemPrice = price(item)
	injectors.insert_one(
		{"_id": "Result", 
		"Output": itemPrice}
	)
	