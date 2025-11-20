from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


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
        "/buy <item> - Purchase item\n"
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
    # /help in PRIVATE
    # -----------------------------
    @bot.on_message(filters.command("help") & filters.private)
    async def help_private(_, msg: Message):
        send_help_text(msg)

    # -----------------------------
    # /help in GROUP
    # -----------------------------
    @bot.on_message(filters.command("help") & filters.group)
    async def help_group(_, msg: Message):

        bot_user = await bot.get_me()

        btn = InlineKeyboardMarkup(
            [[InlineKeyboardButton("📬 View Help in DM", url=f"https://t.me/{bot_user.username}?start=help")]]
        )

        await msg.reply(
            "📬 **Help is available in DM. Tap the button below.**",
            reply_markup=btn
        )

    print("[loaded] games.help")
