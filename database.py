import pymongo
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = pymongo.MongoClient(MONGO_URI)
db = client.get_database()
sweets_collection = db.sweets


def get_all_sweets():
    """Fetches all sweets from the MongoDB collection."""
    sweets = list(sweets_collection.find({}, {"_id": 0}))
    return sweets
