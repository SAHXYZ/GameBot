# filename: games/flip.py

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

# ✅ Use MongoDB, not data.json
from database.mongo import get_user, update_user

from utils.cooldown import check_cooldown, update_cooldown
import random
import asyncio


def init_flip(bot: Client):

    @bot.on_message(filters.command("flip"))
    async def flip_cmd(_, msg):

        if not msg.from_user:
            return

        user = get_user(msg.from_user.id)

        ok, wait, pretty = check_cooldown(user, "flip", 300)
        if not ok:
            return await msg.reply(f"⏳ You must wait **{pretty}** before flipping again!")

        # Choose side buttons
        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🙂 Heads", callback_data="flip_heads"),
                    InlineKeyboardButton("⚡ Tails", callback_data="flip_tails"),
                ]
            ]
        )

        await msg.reply("🎮 **Choose your side:**", reply_markup=buttons)

    # Callback for the coin flip result
    @bot.on_callback_query(filters.regex(r"flip_"))
    async def flip_result(_, cq: CallbackQuery):

        choice = cq.data.replace("flip_", "")  # heads / tails
        user_id = cq.from_user.id
        user = get_user(user_id)

        ok, wait, pretty = check_cooldown(user, "flip", 30)
        if not ok:
            return await cq.answer(f"⏳ Wait {pretty}!", show_alert=True)

        await cq.answer()

        # Animation before result
        anim_msg = await cq.message.reply("🪙 Flipping coin...")
        await asyncio.sleep(1.2)

        actual = random.choice(["heads", "tails"])

        reward = random.randint(1, 100)
        penalty = random.randint(1, 40)

        bronze = user.get("bronze", 0)

        # Win condition
        if choice == actual:
            new_bronze = bronze + reward
            outcome_text = (
                f"🎉 **You Won!**\n"
                f"🪙 Coin was **{actual.upper()}**\n"
                f"🥉 You earned **+{reward} Bronze**!"
            )

        # Lose condition
        else:
            new_bronze = max(0, bronze - penalty)
            outcome_text = (
                f"😢 **You Lost!**\n"
                f"🪙 Coin was **{actual.upper()}**\n"
                f"🥉 You lost **-{penalty} Bronze**."
            )

        # Update cooldown + bronze in MongoDB
        new_cooldowns = update_cooldown(user, "flip")

        update_user(user_id, {
            "bronze": new_bronze,
            "cooldowns": new_cooldowns
        })

        await anim_msg.edit(outcome_text)
