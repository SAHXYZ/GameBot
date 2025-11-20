from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
import random, time

# ----------------------------------------
# DATABASE
# ----------------------------------------
try:
    from database.mongo import get_user, update_user
except:
    def get_user(uid):
        return {
            "_id": str(uid),
            "bronze": 0,
            "tools": {"Wooden": 1},
            "equipped": "Wooden",
            "inventory": {"ores": {}, "items": []},
            "tool_durabilities": {},
            "last_mine": 0,
        }
    def update_user(uid, data): pass

# ----------------------------------------
# TOOL DEFINITIONS
# ----------------------------------------
TOOLS = {
    "Wooden": {"power": 1, "durability": 50, "price": 50},
    "Stone": {"power": 2, "durability": 100, "price": 150},
    "Iron": {"power": 3, "durability": 150, "price": 400},
    "Gold": {"power": 4, "durability": 200, "price": 1200},
    "Platinum": {"power": 5, "durability": 275, "price": 3000},
    "Diamond": {"power": 7, "durability": 350, "price": 8000},
    "Emerald": {"power": 9, "durability": 450, "price": 20000},
}

# ----------------------------------------
# ORES
# ----------------------------------------
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

# ----------------------------------------
# HELPERS
# ----------------------------------------
def weighted_choice(options):
    total = sum(o["weight"] for o in options)
    pick = random.uniform(0, total)
    cur = 0
    for o in options:
        if cur + o["weight"] >= pick:
            return o
        cur += o["weight"]
    return options[-1]

def ensure_user(u):
    u.setdefault("bronze", 0)
    u.setdefault("tools", {})
    u.setdefault("equipped", None)
    u.setdefault("tool_durabilities", {})
    inv = u.setdefault("inventory", {})
    inv.setdefault("ores", {})
    inv.setdefault("items", [])
    u.setdefault("last_mine", 0)
    return u

# ----------------------------------------
# MINE ACTION
# ----------------------------------------
def mine_logic(uid):
    user = ensure_user(get_user(uid))
    now = time.time()

    # Cooldown
    if now - user["last_mine"] < MINE_COOLDOWN:
        return None, "⏳ Please wait before mining again."

    eq = user.get("equipped")
    if not eq or eq not in TOOLS:
        return None, "❌ You have no valid tool equipped."

    dur = user["tool_durabilities"].setdefault(eq, TOOLS[eq]["durability"])
    if dur <= 0:
        return None, f"⚠️ Your {eq} is broken. Repair it."

    usable_ores = [o for o in ORES if TOOLS[eq]["power"] >= o["min_power"]]
    chosen = weighted_choice(usable_ores)

    amount = 1 + random.choice([0, 1, 2]) + (TOOLS[eq]["power"] // 3)

    user["inventory"]["ores"][chosen["name"]] = \
        user["inventory"]["ores"].get(chosen["name"], 0) + amount

    user["tool_durabilities"][eq] = max(0, dur - random.randint(1, 4))
    user["last_mine"] = now
    update_user(uid, user)

    msg = (
        f"⛏️ You mined **{amount}x {chosen['name']}** using your {eq}!\n"
        f"🪵 Durability left: **{user['tool_durabilities'][eq]}**"
    )

    return True, msg

# ----------------------------------------
# HANDLERS
# ----------------------------------------
async def _mine(client, message: Message):
    ok, text = mine_logic(message.from_user.id)
    await message.reply_text(text)

async def _sell_menu(client, message: Message):
    keyboard = []
    row = []

    for ore in ORES:
        row.append(
            InlineKeyboardButton(ore["name"], callback_data=f"sell_{ore['name']}")
        )
        if len(row) == 2:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)

    await message.reply_text(
        "🛒 **Choose an ore to sell:**",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def _sell_handler(client, query: CallbackQuery):
    name = query.data.replace("sell_", "")
    user = ensure_user(get_user(query.from_user.id))
    ores = user["inventory"]["ores"]

    if ores.get(name, 0) <= 0:
        return await query.answer("❌ You don't have this ore.", show_alert=True)

    amount = ores[name]
    price = next(o for o in ORES if o["name"] == name)["value"]
    gained = amount * price

    user["bronze"] += gained
    del ores[name]

    update_user(query.from_user.id, user)

    await query.message.edit_text(
        f"🛒 Sold **{amount}x {name}** for **{gained} Bronze 🥉**!"
    )
    await query.answer()

# ----------------------------------------
# INIT (LOADER)
# ----------------------------------------
def init_mine(bot: Client):
    bot.add_handler(MessageHandler(_mine, filters.command("mine") & filters.private), group=1)
    bot.add_handler(MessageHandler(_sell_menu, filters.command("sell") & filters.private), group=1)
    bot.add_handler(CallbackQueryHandler(_sell_handler, filters.regex("^sell_")), group=1)
    print("[loaded] games.mine")
