# File: games/daily.py

import time
import random
import traceback

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


def claim_daily(user_id: int) -> str:
    """Handles calculation & database update for the daily reward."""
    from database.mongo import get_user, update_user

    user = get_user(user_id)
    now = int(time.time())
    last = user.get("last_daily")

    if last is not None and (now - last) < 86400:
        remaining = 86400 - (now - last)
        hrs = remaining // 3600
        mins = (remaining % 3600) // 60
        return (
            "⏳ You already claimed your daily bonus!\n"
            f"Try again in **{hrs}h {mins}m**."
        )

    reward = random.randint(100, 300)
    user["coins"] = user.get("coins", 0) + reward
    user["last_daily"] = now
    update_user(user_id, user)

    return f"🎁 You claimed **{reward} coins**!"


def init_daily(bot: Client):

    @bot.on_message(filters.command("daily"))
    async def daily_cmd(_, msg: Message):
        try:
            # --------- FINAL PRIVATE DETECTION ----------
            chat_type = str(msg.chat.type).lower()
            PRIVATE = ("private" in chat_type)

            # --------- PRIVATE → Give reward directly ----------
            if PRIVATE:
                user_id = msg.from_user.id
                text = claim_daily(user_id)
                await msg.reply_text(text)
                return

            # --------- GROUP/SUPERGROUP → Deep-link button ----------
            group_msg = (
                "🕹️ <b>Daily Reward Available!</b>\n"
                "You must claim it in my personal chat.\n\n"
                "Click the button below 👇"
            )

            me = await bot.get_me()
            deep_link = f"https://t.me/{me.username}?start=daily"

            kb = InlineKeyboardMarkup(
                [[InlineKeyboardButton("🎁 Claim Daily in DM", url=deep_link)]]
            )

            await msg.reply_text(
                group_msg,
                reply_markup=kb,
                disable_web_page_preview=True
            )

        except Exception:
            traceback.print_exc()
            try:
                await msg.reply_text("⚠️ Failed to load daily menu.")
            except:
                pass

    print("[loaded] games.daily")
