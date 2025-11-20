from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database.mongo import get_user, update_user


START_TEXT = (
    "Hᴇʏ {name}\n\n"
    "✧༺━━━༻✧༺━━━༻✧\n"
    "     ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ɢᴀᴍᴇʙᴏᴛ\n"
    "✧༺━━━༻✧༺━━━༻✧\n\n"
    "● ʏᴏᴜ'ᴠᴇ sᴛᴇᴘᴘᴇᴅ ɪɴᴛᴏ ᴀ ᴘʀɪᴍᴇ-ᴛɪᴇʀ ᴅɪɢɪᴛᴀʟ ʀᴇᴀʟᴍ ~\n"
    "ғᴀsᴛᴇʀ. ʙᴏʟᴅᴇʀ. sᴍᴀʀᴛᴇʀ. ᴜɴᴅᴇɴɪᴀʙʟʏ sᴇxɪᴇʀ.\n\n"
    "✦ ᴇᴠᴇʀʏ ᴄʟɪᴄᴋ ɪɢɴɪᴛᴇs ᴘᴏᴡᴇʀ\n"
    "✦ ᴇᴠᴇʀʏ ᴄʜᴏɪᴄᴇ ᴄʀᴀғᴛs ʏᴏᴜʀ ʟᴇɢᴇɴᴅ\n"
    "✦ ᴇᴠᴇʀʏ ᴍᴏᴠᴇ ʟᴇᴀᴠᴇs ᴀ ᴍᴀʀᴋ\n\n"
    "ʟᴇᴠᴇʟ ᴜᴘ. ᴅᴏᴍɪɴᴀᴛᴇ. ᴄᴏɴǫᴜᴇʀ ᴛʜᴇ ɢʀɪᴅ.\n\n"
    "✧༺ ʟᴏᴀᴅɪɴɢ ʏᴏᴜʀ ɴᴇxᴛ ᴅᴇsᴛɪɴʏ… ༻✧\n\n"
    "◆ ᴘᴏᴡᴇʀᴇᴅ ʙʏ @PrimordialEmperor ◆"
)


def get_start_menu():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🕹 Commands", callback_data="start_cmds"),
                InlineKeyboardButton("👤 Profile", callback_data="start_profile"),
            ]
        ]
    )


def init_start(bot: Client):

    # -------------------------
    # /start command
    # -------------------------
    @bot.on_message(filters.command("start") & filters.private)
    async def start_handler(_, msg: Message):

        user = msg.from_user
        if not user:
            return

        user_id = user.id

        # Ensure user exists + fix structure
        u = get_user(user_id)
        update_user(user_id, u)

        await msg.reply(
            START_TEXT.format(name=user.first_name),
            reply_markup=get_start_menu()
        )

    # -------------------------
    # Callback: Show Commands
    # -------------------------
    @bot.on_callback_query(filters.regex("^start_cmds$"))
    async def show_commands(_, q: CallbackQuery):
        await q.message.edit_text(
            "🕹 **Commands Menu**\n\n"
            "/help — Full command list\n"
            "/profile — View your stats\n"
            "/mine — Start mining ores\n"
            "/sell — Sell your mined ores\n"
            "/work — Earn bronze\n"
            "/shop — Buy items\n"
            "\nUse /help for the full menu."
        )
        q.answer()

    # -------------------------
    # Callback: Show Profile
    # -------------------------
    @bot.on_callback_query(filters.regex("^start_profile$"))
    async def show_profile(_, q: CallbackQuery):

        user = get_user(q.from_user.id)

        bronze = user.get("bronze", 0)
        items = len(user.get("inventory", {}).get("items", []))
        ores = sum(user.get("inventory", {}).get("ores", {}).values())

        await q.message.edit_text(
            f"👤 **Your Profile**\n\n"
            f"🥉 Bronze: **{bronze}**\n"
            f"🪨 Total Ores: **{ores}**\n"
            f"🎒 Items: **{items}**\n"
            f"\nUse /profile for full details."
        )
        q.answer()

    print("[loaded] games.start")
