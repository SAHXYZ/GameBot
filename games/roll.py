# filename: games/roll.py

from pyrogram import Client, filters
from pyrogram.types import Message

# ✅ Use MongoDB
from database.mongo import get_user, update_user

import random
import asyncio


def init_roll(bot: Client):

    @bot.on_message(filters.command(["roll", "dice"]))
    async def roll_cmd(_, msg: Message):

        if not msg.from_user:
            return

        user_id = msg.from_user.id

        # Temporary “rolling…” animation
        anim = await msg.reply("🎲 Rolling...")

        # Telegram native dice animation
        dice_msg = await bot.send_dice(msg.chat.id)

        # Wait for animation to complete
        await asyncio.sleep(3)

        value = dice_msg.dice.value
        reward = value * 10

        # Update user bronze
        user = get_user(user_id)
        new_bronze = user.get("bronze", 0) + reward

        update_user(user_id, {"bronze": new_bronze})

        await anim.edit(
            f"🎲 **You rolled:** `{value}`\n"
            f"🥉 **Reward:** `{reward} Bronze`"
        )

    # When user taps Telegram’s native dice emoji
    @bot.on_message(filters.dice)
    async def dice_msg(_, msg: Message):

        if not msg.from_user:
            return

        user_id = msg.from_user.id
        value = msg.dice.value
        reward = value * 10

        user = get_user(user_id)
        new_bronze = user.get("bronze", 0) + reward

        update_user(user_id, {"bronze": new_bronze})

        await msg.reply(
            f"🎲 Dice rolled: `{value}`\n"
            f"🥉 Reward: `{reward} Bronze`"
        )
