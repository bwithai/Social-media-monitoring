import time
from datetime import datetime, timedelta

import pymongo

from database.mongo_client import db, connected_device_collection, x_collection


def update_docs_for_tracerout(inserted_id, hop_dict):
    filter_criteria = {"_id": inserted_id}

    # Specify the update operation to add a new key-value pair
    update_operation = {"$set": {"tracerout": hop_dict}}

    # Use update_one to update a single document
    result = connected_device_collection.update_one(filter_criteria, update_operation)

    # Print the result
    print(f"Matched {result.matched_count} document(s) and modified {result.modified_count} document(s)")


def add_system(system_info):
    create_indexing()
    # Insert the entire list with timestamp
    insert_result = connected_device_collection.insert_one(system_info)
    return insert_result.inserted_id


def get_all_documents_of_connected_pc():
    # Query the collection and retrieve all documents without projection
    print("Query get_all_documents_of_connected_pc is in progress...")
    start = time.time()
    documents = connected_device_collection.find()
    end = time.time()
    print(f"Query took {round(end - start, 2)} s.")

    return documents


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


def create_indexing():
    print("indexed on System_UUID, timestamp")
    index_fields = ["System_UUID", "timestamp"]

    # Create indexes for the collection
    # print("Indexing is in progress...")
    # start_idx = time.time()
    for field in index_fields:
        connected_device_collection.create_index([(field, pymongo.DESCENDING)])
        connected_device_collection.create_index([(field, pymongo.ASCENDING)])
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
