from dotenv import load_dotenv
from pymongo import MongoClient
import os
import re
import pandas as pd

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_URL = os.getenv("DB_URL")
DB_NAME = os.getenv("DB_NAME")
ITEM_COLLECTION = os.getenv("ITEM_COLLECTION")

# MongoDB connection
client = MongoClient(f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@{DB_URL}")
db = client[DB_NAME]
item_collection = db[ITEM_COLLECTION]

def find_by_keyword(keyword):
    query = {
    'title': {
        '$regex': re.compile(keyword, re.IGNORECASE),
        } 
    }
    return list(item_collection.find(query))


# Use this
def find_from_index(keyword):
    pipeline = [
        {
            "$search": {
                "index": "default",
                "text": {
                    "query": keyword,
                    "path": {
                        "wildcard": "*"
                    }
                }
            }
        }
    ]
    return list(item_collection.aggregate(pipeline))

def get_dataframe_for_item(item_description):

    item_data_df = pd.DataFrame(find_from_index(item_description))

    return item_data_df

query1 = {
    'title': {
        '$regex': re.compile("a", re.IGNORECASE),
        } 
    }
