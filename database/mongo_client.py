import pymongo

import utils
import certifi

# Establish a connection to the MongoDB server
# client = pymongo.MongoClient(utils.get_database_url(), tlsCAFile=certifi.where())
client = pymongo.MongoClient('localhost', 27017)

# Create/select a database
db = client["social_media"]

# Create/select a collection
x_collection = db["X"]
# x_collection.insert_one({"test": "ing"})
insta_collection = db["instagram"]
tiktok_collection = db["tiktok"]
fb_collection = db["facebook"]
user_collection = db["user"]


def close_mongo_client():
    print("db connection is closed due to progress complete")
    client.close()
