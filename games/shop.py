# filename: games/shop.py

from pyrogram import Client, filters
from pyrogram.types import Message

# ✅ Use MongoDB
from database.mongo import get_user, update_user

from utils.cooldown import check_cooldown, update_cooldown
import asyncio

# Prices are in BRONZE ONLY
SHOP_ITEMS = [
    ("Lucky Charm 🍀", 200),
    ("Golden Key 🔑", 350),
    ("Magic Potion 🧪", 500),
    ("Royal Crown 👑", 900),
]


def init_shop(bot: Client):

    @bot.on_message(filters.command("shop"))
    async def shop(_, msg: Message):

        if not msg.from_user:
            return

        text = "🛒 **Shop Items:**\n\n"
        for i, (name, price) in enumerate(SHOP_ITEMS, start=1):
            text += f"**{i}.** {name} — **{price} 🥉 Bronze**\n"

        text += "\nUse **/buy <item_number>** to purchase."
        await msg.reply(text)

    @bot.on_message(filters.command("buy"))
    async def buy(_, msg: Message):

        if not msg.from_user:
            return

        parts = msg.text.split()
        if len(parts) < 2:
            return await msg.reply("Usage: /buy <item_number>")

        # Validate index
        try:
            idx = int(parts[1]) - 1
        except:
            return await msg.reply("❌ Invalid item number.")

        if idx < 0 or idx >= len(SHOP_ITEMS):
            return await msg.reply("❌ Invalid item number.")

        item_name, price = SHOP_ITEMS[idx]

        user_id = msg.from_user.id
        user = get_user(user_id)

        bronze = user.get("bronze", 0)

        if bronze < price:
            return await msg.reply(
                f"❌ You need **{price} Bronze 🥉** to buy **{item_name}**, "
                f"but you only have **{bronze} Bronze**."
            )

        # Deduct Bronze
        new_bronze = bronze - price

        # Add item to inventory
        inventory = user.get("inventory", [])
        inventory.append(item_name)

        # Badge check (5 items)
        badges = user.get("badges", [])
        if len(inventory) >= 5 and "🛍️" not in badges:
            badges.append("🛍️")

        # Save to MongoDB
        update_user(user_id, {
            "bronze": new_bronze,
            "inventory": inventory,
            "badges": badges
        })

        await msg.reply(
            f"✅ **Purchased:** {item_name}\n"
            f"💰 **Remaining Bronze:** `{new_bronze}` 🥉"
        )
