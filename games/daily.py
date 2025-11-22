# File: games/daily.py
from database.mongo import get_user, update_user
import time
import random
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def claim_daily(user_id: int) -> str:
    """Handles calculation & database update for the daily reward."""
    user = get_user(user_id)
    now = int(time.time())

    last = user.get("last_daily")

    # Check cooldown (24 hours)
    if last is not None and (now - last) < 86400:
        remaining = 86400 - (now - last)
        hrs = remaining // 3600
        mins = (remaining % 3600) // 60
        return f"⏳ You already claimed your daily bonus!\nTry again in **{hrs}h {mins}m**."

    # Reward range
    reward = random.randint(100, 300)

    # Update user
    new_data = {
        "coins": user.get("coins", 0) + reward,
        "last_daily": now
    }
    update_user(user_id, new_data)

    return f"🎁 You claimed **{reward} coins**!"


async def handle_daily(client, msg):
    """Unified handler used for both normal & edited messages."""
    chat_type = msg.chat.type

    # Group chat → send button redirecting to DM
    if chat_type in ("supergroup", "group"):
        bot_username = (await client.get_me()).username
        text = (
            "🕹️ **Daily Reward Available!**\n"
            "You must claim it in my DM.\n\n"
            "Click the button below 👇"
        )

        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton(
                "🎁 Claim Daily in DM",
                url=f"https://t.me/{bot_username}?start=daily"
            )]]
        )

        await msg.reply(text, reply_markup=keyboard)
        return

    # Ensure user exists (channel posts, etc.)
    if not msg.from_user:
        return await msg.reply("❌ Cannot identify user.")

    # Private chat → give reward
    try:
        result = claim_daily(msg.from_user.id)
        await msg.reply(result)
    except Exception as e:
        print("Daily error:", e)
        await msg.reply("⚠️ Error while processing your daily reward.")


def init_daily(bot: Client):
    """Initializes daily command handlers."""

    # Handle /daily in normal messages
    @bot.on_message(filters.command("daily", prefixes="/"))
    async def daily_cmd_msg(client, msg):
        await handle_daily(client, msg)

    # Handle edited messages containing /daily
    @bot.on_edited_message(filters.regex(r"^/daily(@[A-Za-z0-9_]+)?(\s|$)"))
    async def daily_cmd_edit(client, msg):
        await handle_daily(client, msg)
