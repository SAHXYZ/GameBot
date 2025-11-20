from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
import random
import time

from database.mongo import get_user, update_user


# -------------------------
# CONFIG
# -------------------------
TOOLS = {
    "Wooden": {"power": 1, "durability": 50, "price": 50},
    "Stone": {"power": 2, "durability": 100, "price": 150},
    "Iron": {"power": 3, "durability": 150, "price": 400},
    "Gold": {"power": 4, "durability": 200, "price": 1200},
    "Platinum": {"power": 5, "durability": 275, "price": 3000},
    "Diamond": {"power": 7, "durability": 350, "price": 8000},
    "Emerald": {"power": 9, "durability": 450, "price": 20000},
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


# -------------------------
# UTILITIES
# -------------------------
def weighted_choice(options):
    total = sum(o["weight"] for o in options)
    pick = random.uniform(0, total)
    cur = 0
    for o in options:
        if cur + o["weight"] >= pick:
            return o
        cur += o["weight"]
    return options[-1]


def ensure_user(u: dict):
    """Ensure all required fields exist."""
    u.setdefault("inventory", {})
    u["inventory"].setdefault("ores", {})
    u["inventory"].setdefault("items", [])

    u.setdefault("tools", {"Wooden": 1})
    u.setdefault("equipped", "Wooden")
    u.setdefault("tool_durabilities", {"Wooden": 50})
    u.setdefault("last_mine", 0)

    return u


# -------------------------
# MINE LOGIC
# -------------------------
def mine_action(user_id):
    user = ensure_user(get_user(user_id))
    now = time.time()

    if now - user["last_mine"] < MINE_COOLDOWN:
        return {"success": False, "message": "⏳ You're mining too fast. Wait a moment."}

    tool = user.get("equipped")
    if not tool or tool not in TOOLS:
        return {"success": False, "message": "❌ You have no valid tool equipped."}

    durability = user["tool_durabilities"].get(tool, TOOLS[tool]["durability"])
    if durability <= 0:
        return {"success": False, "message": f"⚠️ Your {tool} is broken. Repair it first."}

    power = TOOLS[tool]["power"]
    available = [o for o in ORES if power >= o["min_power"]]

    ore = weighted_choice(available)
    amount = 1 + random.choice([0, 1, 2]) + (power // 3)

    # update inventory
    ores = user["inventory"]["ores"]
    ores[ore["name"]] = ores.get(ore["name"], 0) + amount

    # durability drop
    user["tool_durabilities"][tool] = max(0, durability - random.randint(1, 4))

    user["last_mine"] = now
    update_user(user_id, user)

    return {
        "success": True,
        "message": (
            f"⛏️ You mined **{amount}x {ore['name']}** using your **{tool}**!\n"
            f"🪵 Durability left: `{user['tool_durabilities'][tool]}`"
        )
    }


# -------------------------
# HANDLERS
# -------------------------
def mine_cmd(_, msg: Message):
    if not msg.from_user:
        return

    result = mine_action(msg.from_user.id)
    msg.reply_text(result["message"])


def sell_menu(_, msg: Message):
    buttons = []
    row = []

    for ore in ORES:
        row.append(InlineKeyboardButton(ore["name"], callback_data=f"sell_{ore['name']}"))
        if len(row) == 2:
            buttons.append(row)
            row = []

    if row:
        buttons.append(row)

    msg.reply(
        "🛒 **Choose an ore to sell:**",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


def sell_handler(_, q: CallbackQuery):
    ore_name = q.data.replace("sell_", "")
    user = ensure_user(get_user(q.from_user.id))

    ores = user["inventory"]["ores"]

    if ore_name not in ores or ores[ore_name] <= 0:
        return q.answer("❌ You don't have this ore.", show_alert=True)

    amount = ores[ore_name]
    value = next(o for o in ORES if o["name"] == ore_name)["value"]
    gained = amount * value

    user["bronze"] = user.get("bronze", 0) + gained
    del ores[ore_name]

    update_user(q.from_user.id, user)

    q.message.edit_text(
        f"🛒 Sold **{amount}x {ore_name}** for **{gained} Bronze 🥉**!"
    )
    q.answer()


# -------------------------
# LOADER
# -------------------------
def init_mine(bot: Client):
    bot.add_handler(MessageHandler(mine_cmd, filters.command("mine")), group=0)
    bot.add_handler(MessageHandler(sell_menu, filters.command("sell")), group=0)
    bot.add_handler(CallbackQueryHandler(sell_handler, filters.regex("^sell_")), group=0)
    print("[loaded] games.mine")
