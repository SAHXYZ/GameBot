# File: GameBot/games/sell.py
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
import traceback
from database.mongo import get_user, update_user

# Ore values (must match mine.py)
ORE_VALUES = {
    "Coal": 2,
    "Copper": 5,
    "Iron": 12,
    "Gold": 25,
    "Diamond": 100,
}

def init_sell(bot: Client):

    # 💰 Sell ore (button callback)
    @bot.on_callback_query(filters.regex(r"^sell_ore:"))
    async def sell_ore(_, cq: CallbackQuery):
        try:
            ore = cq.data.split(":", 1)[1]

            user = get_user(cq.from_user.id)
            if not user:
                return await cq.answer("❌ Profile not found.")

            user.setdefault("inventory", {})
            user["inventory"].setdefault("ores", {})
            ores = user["inventory"]["ores"]

            amount = ores.get(ore, 0)

            if amount <= 0:
                return await cq.answer("❌ You don't have this ore.")

            price = ORE_VALUES.get(ore, 1)
            earned = amount * price

            # Add bronze
            user["bronze"] = user.get("bronze", 0) + earned

            # Remove ores
            ores.pop(ore, None)

            update_user(cq.from_user.id, user)

            try:
                await cq.message.edit_text(
                    f"🛒 Sold **{amount}× {ore}** for **{earned} Bronze 🥉**!"
                )
            except:
                pass

            await cq.answer()

        except Exception:
            traceback.print_exc()
            try:
                await cq.answer("⚠️ Error selling ore.")
            except:
                pass

    print("[loaded] games.sell")
