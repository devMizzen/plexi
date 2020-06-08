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

max_slots = 33
max_slot_size = 64


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

probabilities = {
	"Dirt": 0.81,
	"Gravel": 0.65,
	"Andesite": 0.81,
	"Diorite": 0.81,
	"Granite": 0.81,
	"Coal Ore": 1.22,
	"Redstone Ore": 0.99,
	"Iron Ore": 0.75,
	"Gold Ore": 0.15,
	"Diamond Ore": 0.12,
	"Lapis Lazuli Ore": 0.10
}

population = (
	"Stone",
	"Dirt",
	"Gravel",
	"Andesite",
	"Diorite",
	"Granite",
	"Coal Ore",
	"Redstone Ore",
	"Iron Ore",
	"Gold Ore",
	"Diamond Ore",
	"Lapis Lazuli Ore"
)

weight = (
	92.78,	#Stone
	0.81,	#Dirt
	0.65,	#Gravel
	0.81,	#Andesite
	0.81,	#Diorite
	0.81,	#Granite
	1.22,	#Coal Ore
	0.99,	#Redstone Ore
	0.75,	#Iron Ore
	0.15,	#Gold Ore
	0.12,	#Diamond Ore
	0.10	#Lapis
)


def roll(pickaxeGrade):
	while True:
		selection = random.choice(population, weights=weight)
		for _array in probs:
			if _array == selection:
				if _array[3] < pickaxeGrade:
					continue
				else:
					return selection

def load_item_data():
    return values.find_one({"_id": "itemIDs"})

def get_field(_dict, *key_wrods, default=None):
    if _dict is not None:
        for kw in key_wrods:
            if kw in _dict:
                _dict = _dict[kw]
            else:
                _dict = None
                break
    return default if _dict is None else _dict

class Item:
    def __init__(self, id_and_size, items_data=None):
        self.id, self.size = id_and_size
        self.name, self.amount = None, None
        if items_data is None:
            items_data = load_item_data()
        item_data = get_field(items_data, str(self.id))
        base_size = get_field(item_data, "size")
        if base_size is not None:
            self.amount = self.size // base_size
        self.name = get_field(item_data, "name")
    
    def __str__(self):
        return f"ID: {self.id}\nName: {self.name}\nAmount: {self.amount}\n"

#---------------------------------------------------------------+
#    Class Inventory (initialises via Player.get_inventory)     |
#---------------------------------------------------------------+
class Inventory:
    def __init__(self, data):
        self.id = get_field(data, "_id")
        self.slots = get_field(data, "slots", default=[None for _ in range(max_slots)])
        self.lh = get_field(data, "slots[0]")
        self.head = get_field(data, "head")
        self.chest = get_field(data, "chest")
        self.torso = get_field(data, "torso")
        self.shoes = get_field(data, "shoes")
    
    def refresh_slots(self):
        collection = db["inventories"]
        self.slots = get_field(
            collection.find_one(
                {"_id": self.id},
                projection={"slots": True}
            ),
            "slots", default=[None for _ in range(max_slots)]
        )
    
    def refresh_head(self):
        collection = db["inventories"]
        self.slots = get_field(
            collection.find_one(
                {"_id": self.id},
                projection={"head": True}
            ),
            "head"
        )
    
    def refresh_chest(self):
        collection = db["inventories"]
        self.slots = get_field(
            collection.find_one(
                {"_id": self.id},
                projection={"chest": True}
            ),
            "chest"
        )
    
    def refresh_torso(self):
        collection = db["inventories"]
        self.slots = get_field(
            collection.find_one(
                {"_id": self.id},
                projection={"torso": True}
            ),
            "torso"
        )
    
    def refresh_shoes(self):
        collection = db["inventories"]
        self.slots = get_field(
            collection.find_one(
                {"_id": self.id},
                projection={"shoes": True}
            ),
            "shoes"
        )

    def expanded_slots(self):
        item_data = load_item_data()
        output = []
        for slot in self.slots:
            if slot is None:
                output.append(None)
            else:
                output.append(Item(slot, item_data))
        return output

#---------------------------------------------------------------+
#      Class Player (operations with player inv. and etc.)      |
#---------------------------------------------------------------+

class Player:
    def __init__(self, user_id):
        self.id = user_id
    
    def get_inventory(self, **projection):
        collection = dependancies["inventories"]
        if projection == {}:
            projection = None
        result = collection.find_one({"_id": self.id}, projection=projection)
        if result is None:
            result = {"_id": self.id}
        return Inventory(result)

    def add_item(self, item_id):
        collection = dependancies["inventories"]
        slots = self.get_inventory(slots=True).slots
        item_was_added = False

        item_data = load_item_data()
        item_size = get_field(item_data, str(item_id), "size")
        del item_data

        if item_size is None:
            return False
        else:
            for i, slot in enumerate(slots):
                if slot is None or slot[0] == item_id:
                    if slot is None:
                        slots[i] = (item_id, item_size)
                        item_was_added = True
                        break
                    elif slot[1] + item_size <= max_slot_size:
                        slots[i][1] += item_size
                        item_was_added = True
                        break
            if item_was_added:
                collection.update_one(
                    {"_id": self.id},
                    {"$set": {"slots": slots}},
                    upsert=True
                )
            return item_was_added

    def equip_helmet(self, _index):
        collection = dependancies["inventories"]
        inv = self.get_inventory(slots=True, head=True)

        slot = inv.slots[_index]
        wrong_item = False
        if slot is None:
            wrong_item = True
        else:
            slot = Item(slot)
            if slot.name is None:
                wrong_item = True
            elif "helmet" not in slot.name.lower():
                wrong_item = True
        
        if not wrong_item:
            inv.slots[_index], inv.head = inv.head, inv.slots[_index]
            collection.update_one(
                {"_id": self.id},
                {"$set": {
                    "slots": inv.slots,
                    "head": inv.head
                }},
                upsert=True
            )
            return True
        else:
            return False

    def clear_slot(self, _index):
        collection = dependancies["inventories"]
        collection.update_one(
            {"_id": self.id},
            {"$set": {f"slots.{_index}": None}}
        )

    def clear_slots(self):
        collection = dependancies["inventories"]
        collection.update_one(
            {"_id": self.id},
            {"$unset": {"slots": ""}}
        )



	
countdown = time

while countdown != 0:

#--------------------------------------#
#				Item				   #
#--------------------------------------#

	itemName = roll(pickaxeGrade)
	
#--------------------------------------#
#				OreQty				   #
#--------------------------------------#

	for _array in probs:
		if itemName == _array[0]:	 #{  qty  }
			oreQty = random.randint(1,array[1])
			break
			
#--------------------------------------#
#				InvSpace			   #
#--------------------------------------#

	invSpace = getSpace(id)
	
#--------------------------------------#
#				itemQty				   #
#--------------------------------------#

	if itemName in ("Redstone Ore", "Lapis Lazuli Ore"):
		itemQty = oreQty * random.choice((4,5))
	else:
		itemQty = oreQty
		
	if itemQty > countdown:
		itemQty = countdown:
		
	if itemQty >= invSpace:
		itemQty = invSpace
		
#--------------------------------------#
#			  Inventorize			   #
#--------------------------------------#

	

