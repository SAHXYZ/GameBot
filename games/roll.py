# filename: games/roll.py

from pyrogram import Client, filters
from pyrogram.types import Message
from database_main import db
import random
import asyncio

def init_roll(bot: Client):

    @bot.on_message(filters.command(["roll", "dice"]))
    async def roll_cmd(_, msg: Message):

        if not msg.from_user:
            return

        user = db.get_user(msg.from_user.id)

        # Temporary “rolling…” message
        anim = await msg.reply("🎲 Rolling...")

        # Pyrogram v2: use bot.send_dice()
        dice_msg = await bot.send_dice(msg.chat.id)

        # Wait for dice animation to finish
        await asyncio.sleep(3)

        value = dice_msg.dice.value
        reward = value * 10

        # Reward Bronze only
        user["bronze"] = user.get("bronze", 0) + reward
        db.update_user(msg.from_user.id, user)

        await anim.edit(
            f"🎲 **You rolled:** `{value}`\n"
            f"🥉 **Reward:** `{reward} Bronze`"
        )

    # When user taps telegram's dice button
    @bot.on_message(filters.dice)
    async def dice_msg(_, msg: Message):

        if not msg.from_user:
            return

        user = db.get_user(msg.from_user.id)
        value = msg.dice.value
        reward = value * 10

        user["bronze"] = user.get("bronze", 0) + reward
        db.update_user(msg.from_user.id, user)

        await msg.reply(
            f"🎲 Dice rolled: `{value}`\n"
            f"🥉 Reward: `{reward} Bronze`"
        )
