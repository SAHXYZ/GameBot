from pyrogram import Client, filters
from pyrogram.types import Message
from database.mongo import get_user, update_user
from utils.cooldown import check_cooldown, update_cooldown
import random, asyncio


ROB_COOLDOWN = 300   # 5 minutes
VICTIM_PROTECTION = 180  # victim cannot be robbed repeatedly


def init_rob(bot: Client):

    @bot.on_message(filters.command("rob") & filters.private)
    async def rob_game(_, msg: Message):
        if not msg.from_user:
            return

        # must reply to rob
        if not msg.reply_to_message or not msg.reply_to_message.from_user:
            return await msg.reply("⚠️ Reply to a user's message to rob them!")

        robber = msg.from_user
        victim = msg.reply_to_message.from_user

        # cannot rob self
        if robber.id == victim.id:
            return await msg.reply("😑 You cannot rob yourself.")

        # cannot rob bots
        if victim.is_bot:
            return await msg.reply("🤖 You cannot rob a bot.")

        robber_data = get_user(robber.id)
        victim_data = get_user(victim.id)

        # robber cooldown
        ok, wait, pretty = check_cooldown(robber_data, "rob", ROB_COOLDOWN)
        if not ok:
            return await msg.reply(f"⏳ Wait **{pretty}** before robbing again.")

        # victim protection from repeated robbery
        ok2, wait2, pretty2 = check_cooldown(victim_data, "robbed", VICTIM_PROTECTION)
        if not ok2:
            return await msg.reply(
                f"🛡 **{victim.first_name}** is protected for **{pretty2}**."
            )

        rob_msg = await msg.reply("🕵️ Attempting robbery...")
        await asyncio.sleep(1.2)

        # determine what can be stolen
        lootable = []
        if victim_data.get("bronze", 0) > 0:
            lootable.append(("bronze", 60))
        if victim_data.get("silver", 0) > 0:
            lootable.append(("silver", 40))
        if victim_data.get("gold", 0) > 0:
            lootable.append(("gold", 20))
        if victim_data.get("platinum", 0) > 0:
            lootable.append(("platinum", 5))  # extremely rare
        if victim_data.get("black_gold", 0) > 0:
            lootable.append(("black_gold", 1))  # nearly impossible

        if not lootable:
            # apply robber cooldown anyway
            new_cd = update_cooldown(robber_data, "rob")
            update_user(robber.id, {"cooldowns": new_cd})
            return await rob_msg.edit("😶 Target has **no currency to steal!**")

        tiers = [t for t, w in lootable]
        weights = [w for t, w in lootable]
        chosen = random.choices(tiers, weights=weights, k=1)[0]

        # actual success rate
        success_chance = {
            "bronze": 70,
            "silver": 50,
            "gold": 25,
            "platinum": 5,
            "black_gold": 1
        }[chosen]

        if random.randint(1, 100) > success_chance:
            # FAILURE
            penalty = random.randint(20, 60)
            new_bronze = max(0, robber_data.get("bronze", 0) - penalty)

            cds = update_cooldown(robber_data, "rob")

            update_user(robber.id, {
                "bronze": new_bronze,
                "cooldowns": cds
            })

            return await rob_msg.edit(
                f"🚨 **Robbery Failed!**\n"
                f"Penalty: **-{penalty} Bronze 🥉**"
            )

        # SUCCESS — Calculate stolen amount
        max_cap = {
            "bronze": 80,
            "silver": 15,
            "gold": 5,
            "platinum": 1,
            "black_gold": 1
        }[chosen]

        amount = random.randint(1, min(max_cap, victim_data.get(chosen, 0)))

        # apply changes
        update_user(victim.id, {chosen: victim_data.get(chosen, 0) - amount})
        update_user(robber.id, {chosen: robber_data.get(chosen, 0) + amount})

        # update cooldowns for robber & victim
        robber_cd = update_cooldown(robber_data, "rob")
        victim_cd = update_cooldown(victim_data, "robbed")

        update_user(robber.id, {"cooldowns": robber_cd})
        update_user(victim.id, {"cooldowns": victim_cd})

        emoji = {
            "bronze": "🥉",
            "silver": "🥈",
            "gold": "🥇",
            "platinum": "🏅",
            "black_gold": "🎖️"
        }[chosen]

        await rob_msg.edit(
            f"💰 **Robbery Successful!**\n"
            f"You stole **{amount} {emoji} {chosen.replace('_', ' ').title()}**\n"
            f"from **{victim.first_name}**!"
        )
