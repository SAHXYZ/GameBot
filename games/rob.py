from pyrogram import Client, filters
from pyrogram.types import Message
from database.mongo import get_user, update_user
from utils.cooldown import check_cooldown, update_cooldown
import random, asyncio

def init_rob(bot: Client):

    @bot.on_message(filters.command("rob"))
    async def rob_game(_, msg: Message):
        if not msg.from_user:
            return

        if not msg.reply_to_message or not msg.reply_to_message.from_user:
            return await msg.reply("Reply to a user to rob them!")

        robber = msg.from_user
        victim = msg.reply_to_message.from_user

        if robber.id == victim.id:
            return await msg.reply("You cannot rob yourself.")

        robber_data = get_user(robber.id)
        victim_data = get_user(victim.id)

        ok, wait, pretty = check_cooldown(robber_data, "rob", 300)
        if not ok:
            return await msg.reply(f"⏳ You must wait **{pretty}** before robbing again.")

        rob_msg = await msg.reply("🕵️ Trying to rob...")
        await asyncio.sleep(1)

        chances = []
        if victim_data.get("bronze", 0) > 0:
            chances.append(("bronze", 100))
        if victim_data.get("silver", 0) > 0:
            chances.append(("silver", 80))
        if victim_data.get("gold", 0) > 0:
            chances.append(("gold", 50))
        if victim_data.get("platinum", 0) > 0:
            chances.append(("platinum", 1))

        if not chances:
            new_cd = update_cooldown(robber_data, "rob")
            update_user(robber.id, {"cooldowns": new_cd})
            return await rob_msg.edit("😶 Target has **no coins** to steal.")

        tier_choices = [t for t, w in chances]
        tier_weights = [w for t, w in chances]
        chosen_tier = random.choices(tier_choices, weights=tier_weights, k=1)[0]
        success_chance = [w for t, w in chances if t == chosen_tier][0]

        if random.randint(1, 100) > success_chance:
            penalty = random.randint(1, 30)
            new_bronze = max(0, robber_data.get("bronze", 0) - penalty)
            new_cd = update_cooldown(robber_data, "rob")
            update_user(robber.id, {"bronze": new_bronze, "cooldowns": new_cd})
            return await rob_msg.edit(
                f"🚨 **Robbery Failed!**\nYou lost **-{penalty} Bronze 🥉** as a penalty."
            )

        if chosen_tier == "bronze":
            amount = random.randint(1, min(50, victim_data.get("bronze", 0)))
        elif chosen_tier == "silver":
            amount = random.randint(1, min(10, victim_data.get("silver", 0)))
        elif chosen_tier == "gold":
            amount = random.randint(1, min(5, victim_data.get("gold", 0)))
        else:  # platinum
            amount = 1

        new_victim_amount = max(0, victim_data.get(chosen_tier, 0) - amount)
        new_robber_amount = robber_data.get(chosen_tier, 0) + amount
        new_cd = update_cooldown(robber_data, "rob")

        update_user(robber.id, {chosen_tier: new_robber_amount, "cooldowns": new_cd})
        update_user(victim.id, {chosen_tier: new_victim_amount})

        tier_emoji = {
            "bronze": "🥉",
            "silver": "🥈",
            "gold": "🥇",
            "platinum": "🏅",
        }[chosen_tier]

        await rob_msg.edit(
            f"💰 **Robbery Successful!**\n"
            f"You stole **{amount} {tier_emoji} {chosen_tier.capitalize()}**\n"
            f"from **{victim.first_name}**!"
        )
