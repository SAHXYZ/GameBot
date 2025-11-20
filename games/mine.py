from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import random
import time

try:
    from database.mongo import get_user, update_user
except Exception:
    def get_user(user_id):
        return {
            "_id": str(user_id),
            "bronze": 0,
            "tools": {"Wooden": 1},
            "equipped": "Wooden",
            "inventory": {"ores": {}, "items": []},
            "tool_durabilities": {},
            "last_mine": 0,
        }
    def update_user(user_id, data):
        pass

TOOLS = {
    "Wooden": {"power": 1, "durability": 50, "tier": "Common", "price": 50},
    "Stone": {"power": 2, "durability": 100, "tier": "Common", "price": 150},
    "Iron": {"power": 3, "durability": 150, "tier": "Uncommon", "price": 400},
    "Gold": {"power": 4, "durability": 200, "tier": "Rare", "price": 1200},
    "Platinum": {"power": 5, "durability": 275, "tier": "Rare", "price": 3000},
    "Diamond": {"power": 7, "durability": 350, "tier": "Epic", "price": 8000},
    "Emerald": {"power": 9, "durability": 450, "tier": "Legendary", "price": 20000},
}

ORES = [
    {"name": "Stone", "min_power": 0, "weight": 50, "value": 1},
    {"name": "Coal", "min_power": 1, "weight": 40, "value": 2},
    {"name": "Iron", "min_power": 2, "weight": 30, "value": 5},
    {"name": "Gold", "min_power": 3, "weight": 15, "value": 25},
    {"name": "Ruby", "min_power": 4, "weight": 8, "value": 60},
    {"name": "Sapphire", "min_power": 5, "weight": 6, "value": 90},
    {"name": "Emerald", "min_power": 6, "weight": 3, "value": 250},
    {"name": "Diamond", "min_power": 7, "weight": 2, "value": 500},
    {"name": "Mythic Crystal", "min_power": 8, "weight": 1, "value": 1500},
]

MINE_COOLDOWN = 5


def weighted_choice(options):
    total = sum(o["weight"] for o in options)
    pick = random.uniform(0, total)
    cur = 0
    for o in options:
        if cur + o["weight"] >= pick:
            return o
        cur += o["weight"]
    return options[-1]


def ensure_user(user):
    user.setdefault("bronze", 0)
    user.setdefault("tools", {})
    user.setdefault("equipped", None)
    user.setdefault("tool_durabilities", {})
    inv = user.setdefault("inventory", {})
    inv.setdefault("ores", {})
    inv.setdefault("items", [])
    user.setdefault("last_mine", 0)
    return user


def mine_action(user_id):
    user = ensure_user(get_user(user_id))
    now = time.time()

    if now - user["last_mine"] < MINE_COOLDOWN:
        return {"success": False, "message": "⏳ Please wait before mining again."}

    eq = user.get("equipped")
    if not eq or eq not in TOOLS:
        return {"success": False, "message": "❌ No valid tool equipped. Use /equip."}

    dur = user["tool_durabilities"].setdefault(eq, TOOLS[eq]["durability"])
    if dur <= 0:
        return {"success": False, "message": f"⚠️ Your {eq} is broken. Repair it."}

    usable = [o for o in ORES if TOOLS[eq]["power"] >= o["min_power"]]
    chosen = weighted_choice(usable)
    amount = 1 + random.choice([0, 1, 2]) + (TOOLS[eq]["power"] // 3)

    ores = user["inventory"]["ores"]
    ores[chosen["name"]] = ores.get(chosen["name"], 0) + amount

    user["tool_durabilities"][eq] = max(0, dur - random.randint(1, 4))
    user["last_mine"] = now
    update_user(user_id, user)

    return {
        "success": True,
        "message": f"⛏️ You mined **{amount}x {chosen['name']}** using your {eq}!\n🪵 Durability: {user['tool_durabilities'][eq]}"
    }


def _mine(c: Client, m: Message):
    res = mine_action(m.from_user.id)
    m.reply_text(res["message"])


def _sell_menu(c: Client, m: Message):
    keyboard = []
    row = []
    for ore in ORES:
        row.append(InlineKeyboardButton(ore["name"], callback_data=f"sell_{ore['name']}") )
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    m.reply_text(
        "🛒 **Choose an ore to sell:**",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


def _sell_handler(c: Client, q: CallbackQuery):
    ore_name = q.data.replace("sell_", "")
    user = ensure_user(get_user(q.from_user.id))
    ores = user["inventory"]["ores"]

    if ore_name not in ores or ores[ore_name] <= 0:
        return q.answer("❌ You don't have this ore.", show_alert=True)

    amount = ores[ore_name]
    price = next(o for o in ORES if o["name"] == ore_name)["value"]
    gained = amount * price

    user["bronze"] += gained
    del ores[ore_name]
    update_user(q.from_user.id, user)

    q.message.edit_text(f"🛒 Sold **{amount}x {ore_name}** for **{gained} Bronze 🥉**!")
    q.answer()


def init_mine(bot: Client):
    bot.add_handler(filters.command("mine") & filters.private, _mine)
    bot.add_handler(filters.command("sell") & filters.private, _sell_menu)
    bot.add_handler(filters.regex(r"^sell_"), _sell_handler)
    print("[loaded] games.mine")
