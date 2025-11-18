from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "GameBot")

# Ensure TLS on Heroku + allow if certificate issues
client = MongoClient(
    MONGO_URI,
    tls=True,
    tlsAllowInvalidCertificates=True
)

db = client[DB_NAME]
users = db["users"]


def get_user(user_id):
    user_id = str(user_id)
    user = users.find_one({"_id": user_id})

    if not user:
        user = {
            "_id": user_id,
            # coins
            "black_gold": 0,
            "platinum": 0,
            "gold": 0,
            "silver": 0,
            "bronze": 0,
            # stats
            "messages": 0,
            "fight_wins": 0,
            "rob_success": 0,
            "rob_fail": 0,
            # other
            "cooldowns": {},
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
