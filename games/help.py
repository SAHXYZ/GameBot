# File: GameBot/games/help.py
from pyrogram import Client, filters
from pyrogram.types import Message
import traceback


def init_help(bot: Client):

    @bot.on_message(filters.command(["help", "commands"]))
    async def help_cmd(_, msg: Message):
        try:
            text = (
                "<b>🎮 GameBot Help Menu</b>\n\n"

                "<b>📌 General</b>\n"
                "/start - Main menu\n"
                "/help or /commands - Help menu\n"
                "/profile - Show your profile\n"
                "/inv - Show your inventory\n"
                "/work - Earn bronze\n"
                "/shop - Open shop\n"
                "/buy &lt;item&gt; - Purchase item\n"
                "/leaderboard - Show rankings\n\n"

                "<b>🎮 Games</b>\n"
                "/flip - Coin Flip\n"
                "/roll - Dice Roll\n"
                "/fight - Fight another player\n"
                "/rob - Rob a user\n"
                "/guess - Guessing game\n"
                "/mine - Mine ores\n\n"

                "ℹ️ Use commands in private chat for the best experience."
            )

            await msg.reply(text)

        except Exception:
            traceback.print_exc()
            try:
                await msg.reply("⚠️ Failed to load help menu.")
            except:
                pass
