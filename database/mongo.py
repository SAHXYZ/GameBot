from pymongo import MongoClient
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client["GameBot"]
users = db["users"]


def get_user(user_id):
    user_id = str(user_id)
    user = users.find_one({"_id": user_id})

    if not user:
        user = {
            "_id": user_id,
            "coins": 0,
            "group_msgs": 0,
            "cooldowns": {},
            "profile": {},
            "inventory": [],
            "badges": []
        }
        users.insert_one(user)

    return user


def update_user(user_id, data: dict):
    users.update_one(
        {"_id": str(user_id)},
        {"$set": data},
        upsert=True
    )
