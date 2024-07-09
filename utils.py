import json
import os
from bson import ObjectId


def serialize_object_id(dic):
    dic = [
        {**doc, '_id': str(doc['_id'])} for doc in dic
    ]
    return dic


def get_path(relative_path):
    # Get the full path
    full_path = os.path.abspath(relative_path)

    return full_path


def get_database_url():
    url = "mongodb+srv://tika:tik@cluster0.g7xf0kd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    return url


def save_json_file(system_info):
    # Save the system_info dictionary as a JSON file
    with open(get_path('system_info.json'), 'w') as json_file:
        json.dump(system_info, json_file, indent=4)
