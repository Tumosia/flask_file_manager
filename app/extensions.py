from pymongo import MongoClient

client = MongoClient(<mongo_uri>)
db = client['FileSystem']
