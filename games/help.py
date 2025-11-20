from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

def _help(_, msg: Message):
    text = (
        "🎮 **GameBot Help Menu**\n\n"
        "**General Commands**\n"
        "/start - Show main menu\n"
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
        "/buy <num> - Purchase an item\n\n"
        "**Games**\n"
        "/flip - Coin flip\n"
        "/roll - Dice roll\n"
        "/fight - Fight another user\n"
        "/rob - Rob a user\n"
        "/guess - Guessing game\n"
    )

    msg.reply(text)

def init_help(bot: Client):

    # -------------------------
    # /help in PRIVATE chat
    # -------------------------
    @bot.on_message(filters.command("help") & filters.private)
    async def help_private(_, msg: Message):
        _help(_, msg)

    # -------------------------
    # /help in GROUP → redirect to DM
    # -------------------------
    @bot.on_message(filters.command("help") & ~filters.private)
    async def help_group(_, msg: Message):

        bot_username = (await msg._client.get_me()).username

        await msg.reply(
            "📬 **The help menu is available in DM!**\n"
            "Click below to open the bot.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("📥 Open Help Menu", url=f"https://t.me/{bot_username}?start=help")]
                ]
            )
        )
        return

    print("[loaded] games.help")
