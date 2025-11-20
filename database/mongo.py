from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "GameBot")

client = MongoClient(
    MONGO_URI,
    tls=True,
    tlsAllowInvalidCertificates=True
)

db = client[DB_NAME]
users = db["users"]


# -------------------------------------------------
# DEFAULT USER TEMPLATE (Single Source of Truth)
# -------------------------------------------------
DEFAULT_USER = {
    "black_gold": 0,
    "platinum": 0,
    "gold": 0,
    "silver": 0,
    "bronze": 0,

    "messages": 0,
    "fight_wins": 0,
    "rob_success": 0,
    "rob_fail": 0,

    "cooldowns": {},

    "inventory": {
        "ores": {},
        "items": []
    },

    "tools": {"Wooden": 1},
    "equipped": "Wooden",
    "tool_durabilities": {"Wooden": 50},
    "last_mine": 0,

    "badges": []
}


# -------------------------------------------------
# GET USER (Load + Fix Structure Automatically)
# -------------------------------------------------
def get_user(user_id):
    user_id = str(user_id)
    user = users.find_one({"_id": user_id})

    # Create new user
    if not user:
        new_user = {"_id": user_id}
        new_user.update(DEFAULT_USER)
        users.insert_one(new_user)
        return new_user

    # Fix existing user
    updated = False
    fixed_user = {"_id": user_id}

    for key, default_value in DEFAULT_USER.items():

        # If key missing → use default
        if key not in user:
            fixed_user[key] = default_value
            updated = True
            continue

        value = user[key]

        # Deep-fix inventory
        if key == "inventory":
            if not isinstance(value, dict):
                value = {"ores": {}, "items": []}
                updated = True

            value.setdefault("ores", {})
            value.setdefault("items", [])

            fixed_user[key] = value
            continue

        # Copy as-is for other fields
        fixed_user[key] = value

    # Update DB if any fixes applied
    if updated:
        users.update_one({"_id": user_id}, {"$set": fixed_user})

    return fixed_user


# -------------------------------------------------
# UPDATE USER
# -------------------------------------------------
def update_user(user_id, data: dict):
    users.update_one(
        {"_id": str(user_id)},
        {"$set": data},
        upsert=True
    )
