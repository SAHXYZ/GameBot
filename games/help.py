# games/help.py

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


HELP_TEXT = (
    "🎮 **GameBot Help Menu**\n\n"
    "**General Commands**\n"
    "/start - Main menu\n"
    "/help - Help menu\n"
    "/profile - Your stats\n"
    "/leaderboard - Top players\n\n"

    "**Mining System**\n"
    "/mine - Mine ores\n"
    "/sell - Sell ores\n"
    "/tools - View tools\n"
    "/equip <tool> - Equip tool\n"
    "/repair - Repair tool\n\n"

    "**Economy**\n"
    "/work - Earn bronze\n"
    "/shop - Buy items\n"
    "/buy <item> - Purchase item\n"
    "/inv - Inventory\n\n"

    "**Games**\n"
    "/flip - Coin flip\n"
    "/roll - Dice roll\n"
    "/fight - Fight users\n"
    "/rob - Rob users\n"
    "/guess - Word guessing game\n"
)


def init_help(bot: Client):

    # -----------------------
    # HELP IN PRIVATE
    # -----------------------
    @bot.on_message(filters.command("help") & filters.private)
    async def help_private(_, msg: Message):
        await msg.reply(HELP_TEXT)

    # -----------------------
    # HELP IN GROUP
    # -----------------------
    @bot.on_message(filters.command("help") & filters.group)
    async def help_group(client, msg: Message):

        bot_username = (await client.get_me()).username

        btn = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(
                    "📬 Open Help in DM",
                    url=f"https://t.me/{bot_username}?start=help"
                )]
            ]
        )

        await msg.reply(
            "📬 **Help is available in my DM. Tap below:**",
            reply_markup=btn
        )

    print("[loaded] help module")
