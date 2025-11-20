from pyrogram import Client, filters

def init_help(bot: Client):

    @bot.on_message(filters.command("help"))
    async def help_cmd(_, msg):

        text = (
            "🎮 **GameBot Help Menu**\n\n"
            
            "📌 **General Commands**\n"
            "/start - Main menu\n"
            "/help - Help menu\n"
            "/profile - Your stats\n"
            "/leaderboard - Top players\n\n"

            "⛏️ **Mining System**\n"
            "/mine - Mine ores\n"
            "/sell - Sell ores\n"
            "/tools - View tools\n"
            "/equip <tool> - Equip tool\n"
            "/repair - Repair tool\n\n"

            "💰 **Economy**\n"
            "/work - Earn bronze\n"
            "/shop - Buy items\n"
            "/buy <item> - Purchase item\n"
            "/inv - Inventory\n\n"

            "🎮 **Games**\n"
            "/flip - Coin flip\n"
            "/roll - Dice roll\n"
            "/fight - Fight users\n"
            "/rob - Rob users\n"
            "/guess - Word guessing game\n"
        )

        await msg.reply(text)
