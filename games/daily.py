# File: GameBot/games/daily.py

from pyrogram import Client, filters
from pyrogram.types import Message
from datetime import datetime
import random

from database.mongo import get_user, update_user

BRONZE_REWARD = 100


def random_crate():
    roll = random.random() * 100

    if roll <= 80:
        return ("1000 Bronze Coins", {"bronze": 1000})
    elif roll <= 95:
        return ("100 Silver Coins", {"silver": 100})
    else:
        gold = random.randint(1, 50)
        return (f"{gold} Gold Coins", {"gold": gold})


def init_daily(bot: Client):

    @bot.on_message(filters.command("daily"))
    async def daily_cmd(_, msg: Message):
        user_id = msg.from_user.id
        user = get_user(user_id)

        today = datetime.utcnow().date()
        last_claim = user.get("last_daily")

        if last_claim:
            last_claim = datetime.strptime(last_claim, "%Y-%m-%d").date()

        streak = user.get("daily_streak", 0)

        # -------------------------------
        # ❌ Missed OR First Ever → Day 1
        # -------------------------------
        if not last_claim or (today - last_claim).days > 1:
            streak = 1
            reward_msg = (
                f"🎉 <b>Daily Login — Day 1</b>\n"
                f"You received <b>{BRONZE_REWARD} Bronze Coins</b>!"
            )

            # Apply reward
            new_bronze = user.get("bronze", 0) + BRONZE_REWARD
            update_user(user_id, {"bronze": new_bronze})

        # -------------------------------
        # ⏳ Already claimed today
        # -------------------------------
        elif (today - last_claim).days == 0:
            await msg.reply(
                "⏳ <b>You already claimed your daily reward today!</b>\n"
                "Come back tomorrow for more rewards."
            )
            return

        # -------------------------------
        # 🔥 Continue Streak
        # -------------------------------
        else:
            streak += 1

            # Days 2–6 → Bronze reward
            if streak < 7:
                reward_msg = (
                    f"🎉 <b>Daily Login — Day {streak}</b>\n"
                    f"You received <b>{BRONZE_REWARD} Bronze Coins</b>!"
                )

                new_bronze = user.get("bronze", 0) + BRONZE_REWARD
                update_user(user_id, {"bronze": new_bronze})

            # Day 7 → Crate
            else:
                crate_name, crate_reward = random_crate()

                reward_msg = (
                    f"🎁 <b>Daily Login — Day 7</b>\n"
                    f"✨ <b>Random Crate Reward:</b> {crate_name}!\n\n"
                    f"Your streak has been reset!"
                )

                # Apply crate reward safely
                new_user = get_user(user_id)
                for k, v in crate_reward.items():
                    update_user(user_id, {k: new_user.get(k, 0) + v})

                streak = 0  # reset AFTER day 7

        # Save streak + last claim
        update_user(user_id, {
            "daily_streak": streak,
            "last_daily": today.strftime("%Y-%m-%d")
        })

        await msg.reply(reward_msg)
