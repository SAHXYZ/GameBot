# File: games/daily.py

from pyrogram import Client, filters
from pyrogram.types import Message
from datetime import datetime, timedelta
import random
import asyncio

from database.mongo import get_user, update_user


BRONZE_REWARD = 100


def random_crate():
    """
    Returns (crate_name, reward_amount)
    Probability:
        80% Bronze
        15% Gold
        5% Diamond
    """
    roll = random.random() * 100  # 0–100%

    if roll <= 80:
        return ("Bronze Crate", random.randint(80, 140))
    elif roll <= 95:
        return ("Gold Crate", random.randint(300, 500))
    else:
        return ("Diamond Crate", random.randint(1000, 1500))


@Client.on_message(filters.command("daily"))
async def daily_handler(client: Client, msg: Message):
    user_id = msg.from_user.id
    user = await get_user(user_id)

    # First time user safety
    last_time = user.get("last_daily", None)

    if last_time is not None:
        # Cooldown check
        available_time = last_time + timedelta(hours=24)
        if datetime.now() < available_time:
            remaining = available_time - datetime.now()
            hours = remaining.seconds // 3600
            minutes = (remaining.seconds % 3600) // 60
            return await msg.reply(
                f"⏳ **Daily already claimed!**\n"
                f"Come back in **{hours}h {minutes}m**."
            )

    # STEP 1: animation — spinning crate
    anim_msg = await msg.reply("🎁 | Opening daily crate...")
    await asyncio.sleep(1)

    await anim_msg.edit("📦 | Crate received...")
    await asyncio.sleep(1)

    await anim_msg.edit("🔄 | Crate is shaking...")
    await asyncio.sleep(1)

    await anim_msg.edit("✨ | Crate is opening...")
    await asyncio.sleep(1)

    # STEP 2: decide reward
    crate_name, reward_amount = random_crate()

    # Update database (important)
    await update_user(user_id, {
        "bronze": user.get("bronze", 0) + reward_amount,
        "last_daily": datetime.now()
    })

    # STEP 3: reveal
    await anim_msg.edit(
        f"🎉 **DAILY REWARD CLAIMED!**\n\n"
        f"📦 **{crate_name} Unlocked!**\n"
        f"💰 **+{reward_amount} Bronze** added to your wallet.\n\n"
        f"Come back again after **24 hours**!"
    )
