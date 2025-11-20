from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler

def _help(_, msg: Message):
    text = (
        "🎮 **GameBot Help Menu**\n\n"
        "**General Commands**\n"
        "/start - Show menu\n"
        "/help - Show this help message\n"
        "/profile - View your profile\n"
        "/leaderboard - Top players\n\n"
        
        "**Mining System**\n"
        "/mine - Mine ores\n"
        "/sell - Sell ores\n"
        "/tools - View your tools\n"
        "/equip <tool> - Equip a tool\n"
        "/repair - Repair your tool\n\n"

        "**Economy & Items**\n"
        "/work - Earn bronze\n"
        "/shop - Buy items\n"
        "/buy <num> - Purchase an item\n"
        "/inv - View your inventory\n\n"

        "**Games**\n"
        "/flip - Coin flip\n"
        "/roll - Dice roll\n"
        "/fight - Fight another user\n"
        "/rob - Rob a user\n"
        "/guess - Guessing game\n"
    )

    msg.reply(text)

def init_help(bot: Client):
    bot.add_handler(MessageHandler(
        _help,
        filters.command("help") & filters.private
    ))
    print("[loaded] games.help")
