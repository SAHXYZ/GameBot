# File: GameBot/GameBot/games/help.py
from pyrogram import Client, filters
from pyrogram.types import Message

def init_help(bot: Client):

    @bot.on_message(filters.command("help"))
    async def help_cmd(_, msg: Message):

        text = (
            "🎮 **GameBot Help Menu**\n\n"

            "📌 **General Commands**\n"
            "/start - Main menu\n"
            "/help - Help menu\n"
            "/profile - Show your profile\n"
            "/inv - Show inventory\n"
            "/work - Earn bronze\n"
            "/shop - Buy items\n"
            "/buy <item> - Purchase item\n\n"

            "🎮 **Games**\n"
            "/flip - Coin flip\n"
            "/roll - Dice roll\n"
            "/fight - Fight users\n"
            "/rob - Rob users\n"
            "/guess - Word guessing game\n"
            "/mine - Mine ores (earn resources)\n"
        )

        await msg.reply(text)
