from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database.mongo import get_user, update_user
from utils.cooldown import check_cooldown, update_cooldown
import random
import asyncio


FLIP_COOLDOWN = 30  # seconds


def init_flip(bot: Client):

    # ---------------------------
    # /flip command
    # ---------------------------
    @bot.on_message(filters.command("flip") & filters.private)
    async def flip_cmd(_, msg):
        if not msg.from_user:
            return

        user = get_user(msg.from_user.id)

        ok, wait, pretty = check_cooldown(user, "flip", FLIP_COOLDOWN)
        if not ok:
            return await msg.reply(f"⏳ You must wait **{pretty}** before flipping again!")

        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🙂 Heads", callback_data="flip_heads"),
                    InlineKeyboardButton("⚡ Tails", callback_data="flip_tails"),
                ]
            ]
        )

        await msg.reply("🎮 **Choose your side:**", reply_markup=buttons)

    # ---------------------------
    # Flip callback
    # ---------------------------
    @bot.on_callback_query(filters.regex(r"^flip_"))
    async def flip_result(_, cq: CallbackQuery):
        choice = cq.data.replace("flip_", "")
        user_id = cq.from_user.id

        user = get_user(user_id)

        ok, wait, pretty = check_cooldown(user, "flip", FLIP_COOLDOWN)
        if not ok:
            return await cq.answer(f"⏳ Wait {pretty}!", show_alert=True)

        await cq.answer()

        # Animation
        anim = await cq.message.reply("🪙 Flipping coin...")
        await asyncio.sleep(1.2)

        actual = random.choice(["heads", "tails"])
        bronze = user.get("bronze", 0)

        reward = random.randint(20, 70)
        penalty = random.randint(5, 30)

        if choice == actual:
            bronze += reward
            text = (
                f"🎉 **You Won!**\n"
                f"🪙 Coin was **{actual.upper()}**\n"
                f"🥉 You earned **+{reward} Bronze**!"
            )
        else:
            bronze = max(0, bronze - penalty)
            text = (
                f"😢 **You Lost!**\n"
                f"🪙 Coin was **{actual.upper()}**\n"
                f"🥉 You lost **-{penalty} Bronze**."
            )

        # Update cooldown safely
        cds = update_cooldown(user, "flip")

        update_user(
            user_id,
            {
                "bronze": bronze,
                "cooldowns": cds,
            }
        )

        await anim.edit(text)
