# games/shop.py

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database.mongo import get_user, update_user

# --------------------------
# SHOP DATABASE
# --------------------------
ITEMS = [
    ("Lucky Charm 🍀", 200),
    ("Golden Key 🔑", 350),
    ("Magic Potion 🧪", 500),
    ("Royal Crown 👑", 900),
]

TOOLS = [
    ("Wooden", 50),
    ("Stone", 150),
    ("Iron", 400),
    ("Gold", 1200),
    ("Platinum", 3000),
    ("Diamond", 8000),
    ("Emerald", 20000),
]


# --------------------------
# BUILD SHOP BUTTONS
# --------------------------
def build_shop_buttons():
    item_rows = []
    row = []

    for name, _ in ITEMS:
        row.append(InlineKeyboardButton(name, callback_data=f"buy_item:{name}"))
        if len(row) == 2:
            item_rows.append(row)
            row = []
    if row:
        item_rows.append(row)

    tool_rows = []
    row = []
    for name, _ in TOOLS:
        row.append(InlineKeyboardButton(name, callback_data=f"buy_tool:{name}"))
        if len(row) == 2:
            tool_rows.append(row)
            row = []
    if row:
        tool_rows.append(row)

    keyboard = [
        [InlineKeyboardButton("🛒 ITEMS", callback_data="section_items")],
        *item_rows,
        [InlineKeyboardButton("🛠 TOOLS", callback_data="section_tools")],
        *tool_rows,
    ]

    return InlineKeyboardMarkup(keyboard)


# --------------------------
# INIT SHOP
# --------------------------
def init_shop(bot: Client):

    # --- Show Shop ---
    @bot.on_message(filters.command("shop"))
    async def shop_cmd(_, msg: Message):
        await msg.reply(
            "🛒 **GAMEBOT SHOP**\n\n"
            "Tap buttons to buy OR use:\n"
            "`/buy <item name>`\n\n"
            "**Sections:**\n"
            "⭐ Items\n"
            "🔧 Tools",
            reply_markup=build_shop_buttons()
        )

    # --- BUY via TEXT: /buy Lucky Charm ---
    @bot.on_message(filters.command("buy"))
    async def buy_text(_, msg: Message):
        if len(msg.text.split()) < 2:
            return await msg.reply("Usage: `/buy Lucky Charm`", quote=True)

        query = msg.text.split(maxsplit=1)[1].strip().lower()
        user = get_user(msg.from_user.id)

        # ITEMS
        for name, price in ITEMS:
            if name.lower() == query:
                return await purchase_item(msg, user, name, price)

        # TOOLS
        for name, price in TOOLS:
            if name.lower() == query:
                return await purchase_tool(msg, user, name, price)

        return await msg.reply("❌ Item not found. Use /shop")

    # --- BUY via BUTTON ---
    @bot.on_callback_query(filters.regex(r"^buy_item:"))
    async def buy_item_button(_, cq: CallbackQuery):
        name = cq.data.split(":", 1)[1]
        price = next(p for n, p in ITEMS if n == name)
        user = get_user(cq.from_user.id)
        result = await purchase_item(cq.message, user, name, price, is_callback=True)
        await cq.answer()

    @bot.on_callback_query(filters.regex(r"^buy_tool:"))
    async def buy_tool_button(_, cq: CallbackQuery):
        name = cq.data.split(":", 1)[1]
        price = next(p for n, p in TOOLS if n == name)
        user = get_user(cq.from_user.id)
        result = await purchase_tool(cq.message, user, name, price, is_callback=True)
        await cq.answer()


# --------------------------
# PURCHASE HELPERS
# --------------------------
async def purchase_item(msg, user, name, price, is_callback=False):
    if user["bronze"] < price:
        return await msg.reply(f"❌ Not enough Bronze.\nNeeded: {price}\nYou have: {user['bronze']}")

    inv = user["inventory"]["items"]
    inv.append(name)
    user["bronze"] -= price

    update_user(user["_id"], {"inventory": user["inventory"], "bronze": user["bronze"]})

    return await msg.reply(f"✅ **Purchased:** {name}\nRemaining Bronze: {user['bronze']}")


async def purchase_tool(msg, user, name, price, is_callback=False):
    if user["bronze"] < price:
        return await msg.reply(f"❌ Not enough Bronze.\nNeeded: {price}\nYou have: {user['bronze']}")

    user["bronze"] -= price

    # Add or increase tool count
    tools = user["tools"]
    tools[name] = tools.get(name, 0) + 1

    # Durability
    from games.mine import TOOLS as MINE_TOOLS
    default_dur = MINE_TOOLS[name]["durability"]
    user["tool_durabilities"][name] = default_dur

    update_user(user["_id"], {
        "bronze": user["bronze"],
        "tools": user["tools"],
        "tool_durabilities": user["tool_durabilities"]
    })

    return await msg.reply(f"🛠 **Purchased Tool:** {name}\nUse `/equip {name}` to equip it.\nRemaining Bronze: {user['bronze']}")
