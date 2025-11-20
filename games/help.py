# File: GameBot/GameBot/games/help.py
from pyrogram import Client, filters
from pyrogram.types import Message
import traceback

def init_help(bot: Client):

    @bot.on_message(filters.command(["help", "commands"]))
    async def help_cmd(_, msg: Message):
        try:
            text = (
                "🎮 **GameBot Help Menu**\n\n"

                "<b>✧༺━━━༻✧  C O M M A N D S  ✧༺━━━༻✧</b>\n\n"
                "👤 <b>P R O F I L E</b>\n"
                "• <code>/profile</code> – View your profile\n"
                "• <code>/inventory</code> – View your items\n"
                "• <code>/stats</code> – View statistics\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n\n"

                "🎮 <b>G A M E S</b>\n"
                "• <code>/flip</code> – Coin flip\n"
                "• <code>/roll</code> – Dice roll\n"
                "• <code>/fight</code> – Fight\n"
                "• <code>/guess</code> – Guess the word\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n\n"

                "⛏ <b>M I N I N G</b>\n"
                "• <code>/mine</code> – Mine ores\n"
                "• <code>/sell</code> – Sell ores\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n\n"

                "🛒 <b>S H O P</b>\n"
                "• <code>/buy</code> – Buy items\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n\n"

                "📊 <b>O T H E R</b>\n"
                "• <code>/leaderboard</code> – Leaderboard\n"

                "ℹ️ *Tip:* Some features require a profile. Use /start if you haven't."
            )

            await msg.reply_text(text, parse_mode="markdown")

        except Exception:
            traceback.print_exc()
            try:
                await msg.reply_text("⚠️ Error showing help menu.")
            except:
                pass
