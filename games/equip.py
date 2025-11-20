# File: GameBot/games/equip.py
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message
import traceback
from database.mongo import get_user, update_user

# Allowed tools
TOOLS = ["Wooden", "Stone", "Iron", "Platinum", "Diamond", "Emerald"]

def init_equip(bot: Client):

    # /equip command → show tools user owns
    @bot.on_message(filters.command("equip"))
    async def equip_cmd(_, msg: Message):
        try:
            user = get_user(msg.from_user.id)
            if not user:
                return await msg.reply("❌ Use /start first.")

            inventory = user.get("inventory", {})
            tools = inventory.get("tools", [])

            if not tools:
                return await msg.reply("❌ You don't own any tools.")

            # Generate buttons
            buttons = [
                [InlineKeyboardButton(t, callback_data=f"equip_tool:{t}")]
                for t in tools if t in TOOLS
            ]

            await msg.reply(
                "🔧 **Choose a tool to equip:**",
                reply_markup=InlineKeyboardMarkup(buttons)
            )

        except Exception:
            traceback.print_exc()
            await msg.reply("⚠️ Error loading tools.")

    # Button handler
    @bot.on_callback_query(filters.regex(r"^equip_tool:"))
    async def equip_tool(_, cq: CallbackQuery):
        try:
            tool = cq.data.split(":", 1)[1]

            user = get_user(cq.from_user.id)
            if not user:
                return await cq.answer("❌ Profile not found.")

            inventory = user.setdefault("inventory", {})
            owned = inventory.get("tools", [])

            if tool not in owned:
                return await cq.answer("❌ You don't own this tool.")

            # Equip tool
            user["equipped"] = tool
            update_user(cq.from_user.id, user)

            await cq.message.edit_text(f"✅ Equipped **{tool}** successfully!")
            await cq.answer()

        except Exception:
            traceback.print_exc()
            try:
                await cq.answer("⚠️ Error equipping tool.")
            except:
                pass

    print("[loaded] games.equip")
