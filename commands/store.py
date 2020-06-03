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
global db = cluster.plexi_users 
global player = db.id
global dependancies = db.Dependancies

global numOfEntities = len(dependancies.find_one({"_id": "entityIDs"},))

#---------------------------------------------------------#
#						Functions						  #
#---------------------------------------------------------#

def getQty(item):
	playerInv = player.find_one({"_id": "inventory"})
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
	
def setQty(item, qty)
	playerInv = player.find_one({"_id": "inventory"})
	locs = []
	while qty > 0
		for slot in playerInv:		#For each slot in inventory
			if slot == "isEmpty":
				continue
			itemQty = ''
			if item in playerInv[slot]:	
				locs.append(slot)
				for ch in playerInv[slot]: #for each character in the value
					if ch == 'x' or ch == ':
						break
					itemQty += ch
				itemQty = int(itemQty)
				
				if itemQty+qty <= 64:
					playerInv[slot] = str(itemQty+qty) + "x " + item
					qty = 0
					
			elif qty!= 0:
				for slot in playerInv:
					if slot == "isEmpty":
						continue
					if playerInv[slot] == None:
						break
				emptySlot = slot
				if itemQty+qty <= 64:
					player.update_one(
						{"_id" : "inventory"},
						"$set" {
							emptySlot: str(itemQty+qty) + "x " + item
						}
					)
				else
					
			
			
			
				
				

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

		'''filename = "./commands/Database/"+id+".xlsx"
		wb = openpyxl.load_Workbook(filename)
		ws = wb[Inventory]
		
		for row in range(1,int(numOfEntities)):
			currentItem = "A"+str(row)
			itemQty = "B"+str(row)
			if ws[currentItem].value == itemName:
				if int(ws[itemQty].value) >= int(qty):
					return True
		return False'''
		
	elif method == "sub":
		SubQty = qty
		playerInv = player.find_one({"_id": "inventory"})
		invQty = getQty(itemName)
		
		'''filename = "./commands/Database/"+id+".xlsx"
		wb = openpyxl.load_Workbook(filename)
		ws = wb[Inventory]
		
		for row in range(1,int(numOfEntities)):
			currentItem = "A"+str(row)
			itemQty = "B"+str(row)
			if ws[currentItem].value == itemName:
				if qty < ws[itemQty]:
					ws[itemQty] -= SubQty
					wb.save(filename)
					return True
				elif qty == ws[itemQty]:
					ws[itemQty] = None
					ws[currentItem] = None
				elif qty > ws[itemQty]:
					ws[itemQty] = None
					ws[currentItem] = None
					SubQty -= itemQty'''

	elif method == 'add':
		addQty = qty
		filename = "./commands/Database/"+id+".xlsx"
		wb = openpyxl.load_Workbook(filename)
		ws = wb[Inventory]
		
		for row in range(1,int(numOfEntities)):
			currentItem = "A"+str(row)
			itemQty = "B"+str(row)
			if ws[currentItem].value == itemName:
				if ws[itemQty].value + (addQty*size) <= 64:
					ws[itemQty] += addQty*size[0]
					wb.save(filename)
					return True
				
				elif ws[itemQty].value + (addQty*size) > 64:
					ws[itemQty] = 64
					addQty = ws[itemQty].value + (addQty*size) - 64
		return False
		
	else:
		reqSpace = qty
		filename = "./commands/Database/"+id+".xlsx"
		wb = openpyxl.load_Workbook(filename)
		ws = wb[Inventory]
		
		for row in range(1,int(numOfEntities)):
			itemQty = "B"+str(row)
			space = (64*33+4) - reqSpace*size
			if space < 0:
				return False:
			else:
				return True
	
def balance(id, method, amnt):
	fileName = "./commands/Database/"+id+".xlsx"
	wb = openpyxl.load_Workbook(fileName)
	ws = wb[balance]
	
	if method == "chk":
		return ws["A1"].value
	
	elif method == "add":
		try:
			ws["A1"] = ws["A1"].value + amnt
			wb.save(fileName)
			return True
		except:
			return False
	
	elif method == 'sub':
		try:
			ws["A1"] = ws["A1"].value - amnt
			wb.save(fileName)
			return True
		except:
			return False

def raiseError(errorCode):
	print(errorCode)
	sys.stdout.flush()

#---------------------------------------------------------#
#						  Main  						  #
#---------------------------------------------------------#

if argv[2].lower() != "price":
	item = sys.argv[3]
	qty = sys.argv[4]
	size = sys.argv[5]
else:
	item = argv[4]

if sys.argv[1].lower() == 'sell':	
	itemPrice = price(item)
	Credit = itemPrice*qty
	if inventory(id, "chk", itemName, qty) == True:
		balance(id, "add", Credit)
		inventory(id, "sub", itemName, qty)
	else:
		errorCode = "Not enough items in inventory."
		raiseError(errorCode)
	
elif sys.argv[1].lower() == 'buy':
	itemPrice = price(item)
	Credit = itemPrice*qty
	
	bal = balance(id, "chk", Credit)
	inv = inventory(id, "space", qty, size)
	if bal == True and inv == True:
		balance(id, "sub", Credit)
		inventory(id, "add", itemName, qty, size)
	
	elif bal == True and inv == False:
		raiseError("Not enough space in inventory.")
		
	else:
		raiseError("Not enough balance to make the purchase.")
		
elif sys.argv[1].lower() == "price":
	itemPrice = price(item)
	result = itemPrice
	sys.stdout.flush()