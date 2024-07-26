import time
from datetime import datetime, timedelta, timezone

import pymongo
from bson import ObjectId
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure

from database.mongo_client import db, connected_device_collection, x_collection, user_collection, insta_collection, \
    fb_collection

target_crawler = {
    'X': 'tweets',
    'facebook': "fb_posts",
    'Instagram': "insta_posts"
}

target_collection = {
    'X': x_collection,
    'facebook': fb_collection,
    'Instagram': insta_collection
}


# def try_this_approach():
# try:
# Find the user
# update_result = user_collection.update_one(
#     {"name": request.username},  # Assuming you want to update the user "sana"
#     {"$push": {"crawler.X": {"$each": tweet_data}}},
#     upsert=True  # Create the document if it doesn't exist
# )
#
# if update_result.modified_count > 0 or update_result.upserted_id:
#     return JSONResponse(content={"message": "Tweets have been saved to the user's crawler list."},
#                         status_code=200)
# else:
#     raise HTTPException(status_code=500, detail="Failed to update the user document with tweets.")

def update_docs_for_tracerout(inserted_id, hop_dict):
    filter_criteria = {"_id": inserted_id}

    # Specify the update operation to add a new key-value pair
    update_operation = {"$set": {"tracerout": hop_dict}}

    # Use update_one to update a single document
    result = connected_device_collection.update_one(filter_criteria, update_operation)

    # Print the result
    print(f"Matched {result.matched_count} document(s) and modified {result.modified_count} document(s)")


def add_user_to_db(user):
    index_fields = ["name", "email"]
    create_indexing(user_collection, index_fields)
    result = user_collection.insert_one(user)
    return result.inserted_id


def add_logs(email, logs):
    user = user_collection.find_one({"email": email})
    update_result = user_collection.update_one(
        {"_id": user["_id"]},
        {
            "$push": {
                "logs": logs
            }
        }
    )
    if update_result.modified_count > 0 or update_result.upserted_id:
        print("Logs have been saved to the user's document.")


def get_user_by_id(user_id):
    try:
        user = user_collection.find_one({"_id": ObjectId(user_id)})
        return user
    except Exception as e:
        print(f"Error retrieving user: {e}")
        return None


def add_crawler_data(request, scraped_data, crawler: str, email: str):
    # Check if the user exists
    try:
        user = user_collection.find_one({"email": email})

        if not user:
            return "User not found"

        for key, value in target_crawler.items():
            if key == crawler:
                index_fields = ["username", "hashtags"]
                create_indexing(target_collection[crawler], index_fields)
                document = {
                    "username": request.username,
                    "up_to": request.days,
                    value: scraped_data
                }
                insert_result = target_collection[crawler].insert_one(document)
                # Get the current timestamp in UTC
                current_timestamp = datetime.now(timezone.utc).isoformat()
                # Update the user's document with the new tweet ID and timestamp in the crawler.x field
                user_collection.update_one(
                    {"_id": user["_id"]},
                    {
                        "$push": {
                            f"crawler.{key}": {
                                f"{value}_id": insert_result.inserted_id,
                                "scraped_at": current_timestamp
                            }
                        }
                    }
                )
                if crawler != 'X':
                    return f"{len(scraped_data)} Posts inserted successfully"
                return f"{request.days} day Tweets inserted successfully"
    except (ServerSelectionTimeoutError, ConnectionFailure) as db_error:
        return db_error


def get_all_hashtags():
    # Query the collection and retrieve only the hashtags field using projection
    print("Query get_all_hashtags is in progress...")
    start = time.time()
    documents = x_collection.find({}, {"_id": 0, "hashtags": 1})
    end = time.time()
    print(f"Query took {round(end - start, 2)} s.")

    # Extract hashtags from each document
    hashtags = []
    for doc in documents:
        if 'hashtags' in doc:
            hashtags.extend(doc['hashtags'])

    return hashtags


def get_hashtags():
    # Query the collection and retrieve all documents without projection
    print("Query get_all_tweets is in progress...")
    start = time.time()
    documents = x_collection.find()
    end = time.time()
    print(f"Query took {round(end - start, 2)} s.")

    # Extract hashtags from each tweet
    hashtags = []
    for doc in documents:
        if 'hashtags' in doc:
            hashtags.extend(doc['hashtags'])

    return hashtags


def get_all_users():
    # Define the projection
    projection = {
        "_id": 1,  # Exclude the _id field
        "name": 1,
        "email": 1,
        "mobile_number": 1,
        "address": 1,
        "fb_username": 1,
        "insta_username": 1,
        "x_username": 1,
        "hashtags": 1,
        # Add other fields you want to retrieve
    }
    # Query the collection and retrieve all documents without projection
    print("Query get_all_users is in progress...")
    start = time.time()
    # documents = user_collection.find({}, projection)
    # without projection
    documents = user_collection.find()
    end = time.time()
    print(f"Query took {round(end - start, 2)} s.")

    return list(documents)


def get_all_tweets():
    # Query the collection and retrieve all documents without projection
    print("Query get_all_tweets is in progress...")
    start = time.time()
    documents = x_collection.find()
    end = time.time()
    print(f"Query took {round(end - start, 2)} s.")

    return list(documents)


def get_pc_from_db(system_uuid, current_page):
    # Define the number of entries per page and the current page number
    entries_per_page = 10

    # Specify the System_UUID for which you want to retrieve entries
    # target_system_uuid = "6fhjyty022bafgh4d6cb46a80dfhu25f836"  # Replace with your desired System_UUID

    # Aggregate pipeline for pagination with a specific System_UUID
    pipeline = [
        {
            "$match": {
                "System_UUID": system_uuid
            }
        },
        {
            "$sort": {
                "timestamp": -1
            }
        },
        {
            "$skip": (current_page - 1) * entries_per_page
        },
        {
            "$limit": entries_per_page
        }
    ]

    # Execute the aggregation pipeline
    print("Query get_pc is in progress...")
    start = time.time()
    # connected_device_collection.create_index([("System_UUID", 1), ("timestamp", -1)])
    result = list(connected_device_collection.aggregate(pipeline))
    end = time.time()
    print(f"Query took {round(end - start, 2)} s.")
    return result


def get_latest_unique_pcs():
    # Projection definition
    projection = {
        "_id": 0,  # Exclude the _id field
        "timestamp": 1,
        "base64_image": 1,
        "System_UUID": 1,
        "match_found": 1,  # Assuming "match_found" is a new field added in the pipeline
        "platform_info.username": 1  # Access nested fields using dot notation
    }

    # Aggregate to get the latest document for each System_UUID
    pipeline = [
        {
            "$sort": {
                "timestamp": -1
            }
        },
        {
            "$group": {
                "_id": "$System_UUID",
                "latestDocument": {"$first": "$$ROOT"},
                "count": {"$sum": 1}
            }
        },
        {
            "$match": {
                "count": {"$gt": 1}
            }
        },
        {
            "$replaceRoot": {
                "newRoot": {
                    "$mergeObjects": ["$latestDocument", {"match_found": "$count"}]
                }
            }
        },
        {
            "$project": projection  # Apply the projection
        }
    ]

    # Execute the aggregation pipeline
    result = list(connected_device_collection.aggregate(pipeline))
    # result = connected_device_collection.aggregate(pipeline)
    return result


def get_documents_in_time_range(minutes):
    # Calculate timestamps
    current_time = datetime.now()
    start_time = current_time - timedelta(minutes=minutes)

    # Convert timestamps to datetime objects
    start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
    current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

    # MongoDB query to retrieve documents within the time range
    query = {"timestamp": {"$gte": start_time, "$lte": current_time}}
    result = connected_device_collection.find(query)

    # Convert the result to a list of dictionaries
    documents = list(result)

    return documents


def create_indexing(collection, index_fields):
    print("indexing...")

    # Create indexes for the collection
    # print("Indexing is in progress...")
    # start_idx = time.time()
    for field in index_fields:
        collection.create_index([(field, pymongo.ASCENDING)])
        collection.create_index([(field, pymongo.ASCENDING)])
    # end_idx = time.time()
    # print(f"Indexing Took {round(end_idx - start_idx, 2)} s.")


def find_column_name_not_empty(name, collection):
    query = {
        name: {"$ne": ""},
    }

    # Define the projection
    projection = {
        "_id": 0,  # Exclude the _id field
        "full_name": 1,
        "emails": 1,
        name: 1,
        # Add other fields you want to retrieve
    }

    results = collection.find(query, projection).limit(5)

    print("Result:")
    for result in results:
        print(result)


def get_all_documents_from_db(collection_name):
    # Define the projection
    projection = {
        "_id": 0,  # Exclude the _id field
        "full_name": 1,
        "industry": 1,
        "job_title": 1,
        "emails": 1,
        "country": collection_name
        # Add other fields you want to retrieve
    }

    # Query the collection and retrieve all documents with the specified projection
    print("Query is in progress...")
    start = time.time()
    documents = db[collection_name].find({}, projection)
    end = time.time()
    print(f"query Took {round(end - start, 2)} s.")

    return documents


def delete_invalid_emails(collection):
    query = {
        "emails": {
            "$not": {
                "$regex": "@"
            }
        }
    }
    result = collection.delete_many(query)
    # Print the number of documents deleted
    print(f"Deleted {result.deleted_count} documents. \n\n")
