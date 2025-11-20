from pyrogram import Client, filters
from pyrogram.types import Message

def init_help(bot: Client):

    @bot.on_message(filters.command("help") & filters.private)
    async def help_cmd(_, msg: Message):
        text = (
            "🎮 **GameBot Help Menu**\n\n"
            "**General Commands**\n"
            "/start - Show menu\n"
            "/help - Show this help message\n"
            "/profile - View your profile\n"
            "/leaderboard - View top players\n\n"
            "**Coin & Inventory**\n"
            "/work - Earn bronze by working\n"
            "/shop - Purchase special items\n"
            "/buy <item_number> - Buy an item\n"
            "/inv - View your items/ores\n\n"
            "**Mining System**\n"
            "/mine - Mine ores using your equipped pickaxe\n"
            "/sell - Sell ores using inline buttons\n"
            "/tools - View your tools\n"
            "/equip <tool> - Equip a pickaxe\n"
            "/repair - Repair your equipped tool\n\n"
            "**Games**\n"
            "/flip - Coin flip game\n"
            "/roll - Random dice roll\n"
            "/fight - Fight a user\n"
            "/rob - Rob a player\n"
            "/guess - Guess the word\n"
        )

        await msg.reply(text)
