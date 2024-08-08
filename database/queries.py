import pprint
import time
from datetime import datetime, timedelta, timezone

import pymongo
from bson import ObjectId
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure

from database.mongo_client import db, connected_device_collection, x_collection, user_collection, insta_collection, \
    fb_collection
from utils import serialize_datetime, get_highest_match_category, separate_users_by_category, aggregate_keyword_counts

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


def get_analysis_report():
    user_projection = {"_id": 1, "analysis_report": 1, "highest_match_category": 1}
    user_cursor = user_collection.find({}, user_projection)
    analysis_report = list(user_cursor)

    # Separate users for table view
    separate_users = separate_users_by_category(analysis_report)

    # user_count for percentage graph
    total_users = user_collection.count_documents({})

    # keyword_counts for percentage graph
    keyword_counts = aggregate_keyword_counts(analysis_report)

    return separate_users, total_users, keyword_counts


def add_user_analysis(user_id, analysis_report):
    try:
        user_id_obj = ObjectId(user_id)
        user_exists = user_collection.find_one({"_id": user_id_obj})

        if not user_exists:
            return f"User ID {user_id} not found in the database."

        highest_match_category = get_highest_match_category(analysis_report)

        update_result = user_collection.update_one(
            {"_id": user_exists["_id"]},
            {
                "$set": {
                    "analysis_report": analysis_report,
                    'highest_match_category': highest_match_category
                }
            }
        )
        create_indexing(user_collection, ["analysis_report", "highest_match_category"])
        if update_result.modified_count > 0 or update_result.upserted_id:
            return "Analysis report has been saved to the user's document."
        else:
            return f"User ID {user_id} was not found in user collection."
    except Exception as e:
        return f"Error retrieving user for add analysis report : {str(e)}"


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


def get_x_by_id(tweets_id):
    try:
        tweets = x_collection.find_one({"_id": ObjectId(tweets_id)})
        return tweets
    except Exception as e:
        print(f"Error retrieving user: {e}")
        return None


def get_fb_posts_by_id(posts_id):
    try:
        fb_posts = fb_collection.find_one({"_id": ObjectId(posts_id)})
        return fb_posts
    except Exception as e:
        print(f"Error retrieving user: {e}")
        return None


def get_user_by_id(user_id):
    try:
        user = user_collection.find_one({"_id": ObjectId(user_id)})
        return user
    except Exception as e:
        print(f"Error retrieving user: {e}")
        return str(e)


def delete_user_by_id(user_id):
    try:
        user_id_obj = ObjectId(user_id)
        user_exists = user_collection.find_one({"_id": user_id_obj})

        if not user_exists:
            print(f"User ID {user_id} not found in the database.")
            return None

        # Delete the user document from both collections
        result = user_collection.delete_one({"_id": user_id_obj})
        if result.deleted_count > 0:
            return f"User ID {user_id} has been successfully deleted."
        else:
            return f"User ID {user_id} was not found in user collection."
    except Exception as e:
        print(f"Error retrieving user: {e}")
        return str(e)


def get_user_by_id_extend_posts(user_id):
    try:
        user = user_collection.find_one({"_id": ObjectId(user_id)})

        x_list = user["crawler"]["X"]
        fb_list = user["crawler"]["facebook"]
        X = x_collection.find_one({"_id": ObjectId(x_list[0]["tweets_id"])})
        FB = fb_collection.find_one({"_id": ObjectId(fb_list[0]["fb_posts_id"])})

        user["crawler"]["X"] = serialize_datetime(X['tweets'])
        user["crawler"]["facebook"] = serialize_datetime(FB['fb_posts'])

        return user
    except Exception as e:
        print(f"Error retrieving user: {e}")
        return None


def get_user_by_email(email):
    try:
        user = user_collection.find_one({"email": email})
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
                index_fields = ["username", "hashtags", "original_description"]
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


from bson import ObjectId


def get_crawlers_ids(user_id):
    if not user_collection.find_one({"_id": ObjectId(user_id)}):
        print("User not found from communication")
    else:
        query = {"_id": ObjectId(user_id)} if user_id else {}
        user_cursor = list(user_collection.find(query, {"_id": 0, "crawler": 1}))
        x_id = user_cursor[0]['crawler']['X'][0]['tweets_id']
        fb_id = user_cursor[0]['crawler']['facebook'][0]['fb_posts_id']
        return {'x_id': x_id, 'fb_id': fb_id}


def get_post_caption(tweets_id=None, fb_posts_id=None):
    # Validate if the IDs exist in the database
    tweet_captions = None
    fb_post_captions = None
    if tweets_id:
        if not x_collection.find_one({"_id": ObjectId(tweets_id)}):
            print(f"Tweet ID {tweets_id} not found in the database.")
            tweet_captions = None
        else:
            x_query = {"_id": ObjectId(tweets_id)} if tweets_id else {}
            x_projection = {"_id": 0, "tweets.original_description": 1, "tweets.images": 1, "tweets.links": 1}
            x_cursor = x_collection.find(x_query, x_projection)
            tweet_captions = list(x_cursor)[0]['tweets']

    if fb_posts_id:
        if not fb_collection.find_one({"_id": ObjectId(fb_posts_id)}):
            print(f"Facebook Post ID {fb_posts_id} not found in the database.")
            fb_post_captions = None
        else:
            fb_query = {"_id": ObjectId(fb_posts_id)} if fb_posts_id else {}
            fb_projection = {"_id": 0, "fb_posts.original_description": 1, "fb_posts.images": 1, "fb_posts.links": 1}
            fb_cursor = fb_collection.find(fb_query, fb_projection)
            fb_post_captions = list(fb_cursor)[0]['fb_posts']

    return tweet_captions, fb_post_captions


def get_all_hashtags(tweets_id=None, fb_posts_id=None):
    """
    Retrieve all hashtags from the tweets and Facebook posts in the database collections.

    Parameters:
    tweets_id (str): The optional ID to filter documents in the tweets collection.
    fb_posts_id (str): The optional ID to filter documents in the Facebook posts collection.

    Returns:
    tuple: Two lists containing hashtags from tweets and Facebook posts, respectively.
    """

    x_hashtags, fb_hashtags = None, None

    def extract_hashtags(cursor, post_key):
        return [
            hashtag
            for doc in cursor
            if post_key in doc
            for post in doc[post_key]
            if 'hashtags' in post
            for hashtag in post['hashtags']
        ]

    print("Query get_all_hashtags is in progress...")
    start_time = time.time()

    # Validate if the IDs exist in the database
    if tweets_id:
        if not x_collection.find_one({"_id": ObjectId(tweets_id)}):
            print(f"Tweet ID {tweets_id} not found in the database.")
            x_hashtags = None
        else:
            x_query = {"_id": ObjectId(tweets_id)} if tweets_id else {}
            # Query the collections
            x_cursor = x_collection.find(x_query, {"_id": 0, "tweets.hashtags": 1})
            # Extract hashtags from tweets and Facebook posts
            x_hashtags = extract_hashtags(x_cursor, 'tweets')

    if fb_posts_id:
        if not fb_collection.find_one({"_id": ObjectId(fb_posts_id)}):
            print(f"Facebook Post ID {fb_posts_id} not found in the database.")
            fb_hashtags = None
        else:
            fb_query = {"_id": ObjectId(fb_posts_id)} if fb_posts_id else {}
            fb_cursor = fb_collection.find(fb_query, {"_id": 0, "fb_posts.hashtags": 1})
            fb_hashtags = extract_hashtags(fb_cursor, 'fb_posts')

    end_time = time.time()
    print(f"Query took {round(end_time - start_time, 2)} seconds.")

    return x_hashtags, fb_hashtags


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
