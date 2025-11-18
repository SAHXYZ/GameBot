# filename: games/work.py

from pyrogram import Client, filters
from pyrogram.types import Message

# ✅ Use MongoDB instead of data.json
from database.mongo import get_user, update_user

from utils.cooldown import check_cooldown, update_cooldown
import random
import asyncio

WORK_TASKS = [
    "Delivering parcels 📦",
    "Fixing a computer 🖥️",
    "Cleaning a mansion 🧹",
    "Helping at a store 🏪",
    "Repairing a car 🚗",
    "Cooking in a restaurant 🍳",
    "Gardening in the yard 🌱",
    "Tuning a bike 🚴",
]


def init_work(bot: Client):

    @bot.on_message(filters.command("work"))
    async def work_cmd(_, msg: Message):

        if not msg.from_user:
            return

        user_id = msg.from_user.id
        user = get_user(user_id)

        ok, wait, pretty = check_cooldown(user, "work", 300)
        if not ok:
            return await msg.reply(f"⏳ You must wait **{pretty}** before working again.")

        # Choose a random work task
        task = random.choice(WORK_TASKS)

        working_msg = await msg.reply(
            f"🔧 You start: **{task}**\n⏳ Working..."
        )

        # Work animation
        await asyncio.sleep(1.2)

        # Reward bronze (1–100)
        reward = random.randint(1, 100)
        new_bronze = user.get("bronze", 0) + reward

        # Update cooldown + save to MongoDB
        new_cd = update_cooldown(user, "work")

        update_user(user_id, {
            "bronze": new_bronze,
            "cooldowns": new_cd
        })

        # Final message
        await working_msg.edit(
            f"💼 **Work Completed!**\n"
            f"✨ You earned **{reward} Bronze** 🥉"
        )
