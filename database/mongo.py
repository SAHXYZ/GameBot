from pymongo import MongoClient
from config import MONGO_URI, DB_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
users = db["users"]

def get_user(uid):
    uid = str(uid)
    user = users.find_one({"_id": uid})
    if not user:
        user = {
            "_id": uid,
            "black_gold": 0,
            "platinum": 0,
            "gold": 0,
            "silver": 0,
            "bronze": 0,
            "messages": 0,
            "badges": [],
            "inventory": []
        }
        users.insert_one(user)
    return user

def update_user(uid, data: dict):
    users.update_one({"_id": str(uid)}, {"$set": data})
