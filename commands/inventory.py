import os
import sys
import json
import pymongo

from pymongo import MongoClient as mongo

id = str(sys.argv[1])

cluster = mongo(os.environ["MONGOLAB_URL"])  #Same as process.env.MONGO_URL
db = cluster['plexi_users']
player = db.id
dependancies = db['Dependancies']

inventory = {}

result = 0
print(result)
sys.stdout.flush()

