# filename: games/work.py
from pyrogram import Client, filters
from pyrogram.types import Message
from database_main import db
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

        user = db.get_user(msg.from_user.id)

        ok, wait, pretty = check_cooldown(user, "work", 300)
        if not ok:
            return await msg.reply(f"⏳ You must wait **{pretty}** before working again.")

        # Choose random task
        task = random.choice(WORK_TASKS)

        working_msg = await msg.reply(f"🔧 You start: **{task}**\n⏳ Working...")

        # Simulate work time
        await asyncio.sleep(1.2)

        # Bronze reward 1–100
        reward = random.randint(1, 100)
        bronze = user.get("bronze", 0)
        user["bronze"] = bronze + reward

        # Update cooldown & save
        user = update_cooldown(user, "work")
        db.update_user(msg.from_user.id, user)

        # Final message
        await working_msg.edit(
            f"💼 **Work Completed!**\n"
            f"✨ You earned **{reward} Bronze** 🥉"
        )
