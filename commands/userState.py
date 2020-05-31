import pymongo
import os 
import sys

from pymongo import MongoClient as mongo

io = sys.argv[1]
id = sys.argv[2]

cluster = (os.Environ["MONGO_URL"])
db = cluster["plexi_users"]
dependancies = db["Dependancies"]

if io == "read":
	userState = dependancies.find_one({"_id": "userState"}, projection = {id: True})
	dependancies.update_one(
		{"_id": "injector"},
		{
			"$set" {
				"userState" = userState
			}
		}
	)
elif io == "mine":
	dependancies.update_one(
		{"_id": "userState"},
		{
			"$set" {
				id = "mining"
			}
		}
	)
else:
	dependancies.update_one(
		{"_id": "userState"},
		{
			"$set" {
				id = "idle"
			}
		}