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

cluster = mongo(os.environ["MONGO_URL"])  #Same as process.env.MONGO_URL
db = cluster.plexi_users 
player = db.id
dependancies = db.Dependancies

numOfEntities = len(dependancies.find_one({"_id": "entityIDs"},))

#---------------------------------------------------------#
#						Functions						  #
#---------------------------------------------------------#

def price(item):
	itemPrices = dependancies.find_one({"_id": "itemPrices"})
	itemPrice = int(itemPrices[item])
	return itemPrice
	
def inventory(id, method, itemName, *arg):
	if method == 'chk':
		playerInv = player.find_one({"_id": "inventory"})
		inventoryQty = 0
		for slot in playerInv:
			itemQty = ''
			if itemName in playerInv[slot]:
				for ch in playerInv[slot]:
					if ch == 'x' or ch == '-':
						break
					itemQty += ch
				inventoryQty += int(itemQty)
		if inventoryQty >= qty:
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
		filename = "./commands/Database/"+id+".xlsx"
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
					SubQty -= itemQty

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

if argv[1].lower() != "price":
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