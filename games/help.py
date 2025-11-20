# games/help.py
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.handlers import MessageHandler

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

    "**Economy & Items**\n"
    "/work - Earn bronze\n"
    "/shop - Buy items\n"
    "/buy <name> - Purchase item\n"
    "/inv - Show inventory\n\n"

    "**Games**\n"
    "/flip - Coin flip\n"
    "/roll - Dice roll\n"
    "/fight - Fight users\n"
    "/rob - Rob users\n"
    "/guess - Word guessing game\n"
)

def send_help_msg(target_msg: Message):
    # send the help text as a reply in the message context provided
    target_msg.reply(HELP_TEXT)

def init_help(bot: Client):
    # /help in private DM
    async def help_private(_, msg: Message):
        if not msg.from_user:
            return
        await msg.reply(HELP_TEXT)

    # /help in group - show short message + button that opens DM to the bot
    async def help_group(_, msg: Message):
        if not msg.from_user:
            return
        me = await msg._client.get_me()
        username = me.username or None
        if username:
            url = f"https://t.me/{username}?start=help"
            kb = InlineKeyboardMarkup([[InlineKeyboardButton("📬 Open Help in DM", url=url)]])
            await msg.reply("📬 Help is available in my DM. Tap below:", reply_markup=kb)
        else:
            await msg.reply("📬 Please open my DM to see the help message.")

    # Add handlers consistently using add_handler (matches your main loader)
    bot.add_handler(MessageHandler(help_private, filters.command("help") & filters.private), group=0)
    bot.add_handler(MessageHandler(help_group, filters.command("help") & ~filters.private), group=0)

    print("[loaded] games.help")
