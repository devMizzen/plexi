import os
import sys
import json

id = str(sys.argv[1])
inventory = {}

f = open("userlist.txt", "a+")
f.close()

f = open("userlist.txt", "r")
if id in f.read():
	f.close()
	pre_existance = True
else:
	f.close()
	pre_existance = False
	f = open("userlist.txt", "a")
	f.write(id + '\n')
	f.close()
	
fileDir = "./commands/Database/"+id
try:
	os.mkdir(fileDir)
except:
	pass
fileName = fileDir+"/playerInventory.json"
f = open(fileName,'a+')
f.close()
if pre_existance == True:
	with open(fileName,"r",encoding="utf-8") as userFile:
		data = json.load(userFile)
		
		isEmpty = True
		for slot in data:
			if (data[slot] != "--"):
				if slot != "check":
					isEmpty = False
					
		if isEmpty == False:
			with open("./commands/inventory.json", "w",encoding="utf-8") as fil:
				inventory["lh"] = data["lh"]
				for i in range(32):
					slotNo = "slot"+ str(i+1)
					inventory[slotNo] = data[slotNo]
				inventory["head"] = data["head"]
				inventory["chest"] = data["chest"]
				inventory["torso"] = data["torso"]
				inventory["shoe"] = data["shoe"]
				inventory["check"] = "--"

				fil.write(json.dumps(inventory))
			fil.close()
			result = 0
				
		else:
			with open("./commands/inventory.json", "w",encoding="utf-8") as inv:
				inventory["check"] = '-'
				inv.write(json.dumps(inventory))
			inv.close()
			result = 0
	userFile.close()
			#print(result)
			#sys.stdout.flush()

else:
	
	inventory["lh"] = '--'
	for i in range(32):
		slotNo = "slot"+ str(i+1)
		inventory[slotNo] = '--'
	inventory["head"] = '--'
	inventory["chest"] = '--'
	inventory["torso"] = '--'
	inventory["shoe"] = '--'

	with open(fileName,"w",encoding="utf-8") as UserFile:
		UserFile.write(json.dumps(inventory))
	UserFile.close()
	inventory["check"] = '-'
	
	with open("./commands/inventory.json","w",encoding="utf-8") as UserFile:
		UserFile.write(json.dumps(inventory))
	UserFile.close()

	result = 0
print(result)
sys.stdout.flush()