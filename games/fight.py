from pyrogram import Client, filters
from pyrogram.types import Message
from database.mongo import get_user, update_user
from utils.cooldown import check_cooldown, update_cooldown
import random, asyncio


FIGHT_COOLDOWN = 60        # attacker cooldown
DEFENDER_PROTECT = 40      # defender cannot be attacked instantly again
MAX_STEAL = 50             # max bronze stolen in win


def init_fight(bot: Client):

    @bot.on_message(filters.command("fight") & filters.private)
    async def fight_game(_, msg: Message):
        if not msg.from_user:
            return

        if not msg.reply_to_message or not msg.reply_to_message.from_user:
            return await msg.reply("⚔️ Reply to a user's message to start a fight!")

        attacker = msg.from_user
        defender = msg.reply_to_message.from_user

        if attacker.id == defender.id:
            return await msg.reply("🤨 You cannot fight yourself!")

        if defender.is_bot:
            return await msg.reply("🤖 You cannot fight a bot!")

        a_data = get_user(attacker.id)
        d_data = get_user(defender.id)

        # attacker cooldown
        ok, wait, pretty = check_cooldown(a_data, "fight", FIGHT_COOLDOWN)
        if not ok:
            return await msg.reply(f"⏳ You must wait **{pretty}** before fighting again.")

        # defender protection
        ok2, wait2, pretty2 = check_cooldown(d_data, "fight_protect", DEFENDER_PROTECT)
        if not ok2:
            return await msg.reply(
                f"🛡 **{defender.first_name}** is protected for **{pretty2}**."
            )

        # Animation
        fight_msg = await msg.reply("🥊 The fight has begun...")
        await asyncio.sleep(1.2)

        # Balanced fight power
        a_power = random.randint(20, 150)
        d_power = random.randint(20, 150)

        a_bronze = a_data.get("bronze", 0)
        d_bronze = d_data.get("bronze", 0)

        # ----------------------------------
        # ATTACKER WINS
        # ----------------------------------
        if a_power >= d_power:

            steal = random.randint(5, MAX_STEAL)
            steal = min(steal, d_bronze)

            new_a = a_bronze + steal
            new_d = max(0, d_bronze - steal)

            a_wins = a_data.get("fight_wins", 0) + 1

            update_user(attacker.id, {"bronze": new_a, "fight_wins": a_wins})
            update_user(defender.id, {"bronze": new_d})

            result = (
                f"🏆 **Victory!**\n"
                f"You defeated **{defender.first_name}**!\n"
                f"🥉 You claimed **{steal} Bronze**."
            )

        # ----------------------------------
        # DEFENDER WINS
        # ----------------------------------
        else:
            penalty = random.randint(3, 30)
            penalty = min(penalty, a_bronze)

            new_a = max(0, a_bronze - penalty)
            new_d = d_bronze + penalty

            d_wins = d_data.get("fight_wins", 0) + 1

            update_user(attacker.id, {"bronze": new_a})
            update_user(defender.id, {"bronze": new_d, "fight_wins": d_wins})

            result = (
                f"😢 **Defeat!**\n"
                f"**{defender.first_name}** overpowered you.\n"
                f"🥉 You lost **{penalty} Bronze**."
            )

        # ----------------------------------
        # COOLDOWN UPDATE
        # ----------------------------------
        a_cd = update_cooldown(a_data, "fight")
        d_cd = update_cooldown(d_data, "fight_protect")

        update_user(attacker.id, {"cooldowns": a_cd})
        update_user(defender.id, {"cooldowns": d_cd})

        await fight_msg.edit(result)
