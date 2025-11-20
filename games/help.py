from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.handlers import MessageHandler


def send_help_text(msg: Message):
    text = (
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
        "/buy <num> - Purchase item\n"
        "/inv - Show inventory\n\n"

        "**Games**\n"
        "/flip - Coin flip\n"
        "/roll - Dice roll\n"
        "/fight - Fight users\n"
        "/rob - Rob users\n"
        "/guess - Word guessing game\n"
    )

    msg.reply(text)


def init_help(bot: Client):

    # -----------------------------
    # /help in PRIVATE (normal help)
    # -----------------------------
    @bot.on_message(filters.command("help") & filters.private)
    async def help_dm(_, msg: Message):
        send_help_text(msg)


    # -----------------------------
    # /help in GROUP (redirect to DM)
    # -----------------------------
    @bot.on_message(filters.command("help") & ~filters.private)
    async def help_group(_, msg: Message):

        username = (await msg._client.get_me()).username

        btn = InlineKeyboardMarkup(
            [[InlineKeyboardButton("📬 Open Help in DM", url=f"https://t.me/{username}?start=help")]]
        )

        await msg.reply(
            "📬 **Help is available in my DM. Tap below:**",
            reply_markup=btn
        )


    # -----------------------------
    # Register handler correctly
    # -----------------------------
    bot.add_handler(MessageHandler(help_dm, filters.command("help") & filters.private), group=0)

    print("[loaded] games.help")
