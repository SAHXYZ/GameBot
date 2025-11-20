# File: GameBot/GameBot/games/start.py
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import traceback

from database.mongo import get_user, create_user_if_not_exists

# ==========================================================
# 📌 START TEXT (Home Page)
# ==========================================================
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

# ==========================================================
# 📌 MAIN MENU (Only 2 buttons)
# ==========================================================
def get_start_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("👤 Profile", callback_data="open_profile")],
        [InlineKeyboardButton("❓ Commands", callback_data="help_show")],
    ])

# ==========================================================
# 📌 Async safe editor
# ==========================================================
async def safe_edit(message, text, markup=None):
    try:
        if markup:
            return await message.edit_text(text, reply_markup=markup)
        return await message.edit_text(text)
    except:
        return

# ==========================================================
# 📌 Start Handler
# ==========================================================
def init_start(bot: Client):

    @bot.on_message(filters.command("start"))
    async def start_cmd(_, msg: Message):
        try:
            create_user_if_not_exists(msg.from_user.id, msg.from_user.first_name)

            await msg.reply(
                START_TEXT.format(name=msg.from_user.first_name),
                reply_markup=get_start_menu()
            )
        except Exception:
            traceback.print_exc()
            try:
                await msg.reply("⚠️ Error while starting the bot.")
            except:
                pass

    # ======================================================
    # 📌 FULL COMMAND LIST
    # ======================================================
    @bot.on_callback_query(filters.regex("^help_show$"))
    async def help_show(_, q):
        try:
            commands_text = (
    "⚙️ ● <b><i>HELP CENTER</i></b>\n\n"
    "⟡ <b><i>Profile</i></b>\n"
    "• /profile — View Your Profile\n\n"
    "⟡ <b><i>Games</i></b>\n"
    "• /flip — Coin Flip Duel\n"
    "• /roll — Dice Roll\n"
    "• /fight — Fight Another Player\n"
    "• /rob — Rob a Player (Risk + Reward)\n"
    "• /guess — Guess the Hidden Word\n\n"
    "⟡ <b><i>Mining</i></b>\n"
    "• /mine — Mine Ores\n"
    "• /sell — Sell Your Mined Ores\n\n"
    "⟡ <b><i>Shop</i></b>\n"
    "• /shop — View Shop Items\n"
    "• /buy — Buy Items/Tools\n\n"
    "⟡ <b><i>Other</i></b>\n"
    "• /leaderboard — Top Players\n"
    "• /work — Earn Bronze Coins\n\n"
    "⟡ <i>Tip: You Should Use These Commands In Bot's Personal Chat "
    "For Better Performance.</i> ⚡️"
)

            kb = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back", callback_data="back_to_home")]
            ])

            await safe_edit(q.message, commands_text, kb)
            await q.answer()

        except Exception:
            traceback.print_exc()

    # Back button → return to start menu
    @bot.on_callback_query(filters.regex("^back_to_home$"))
    async def back_to_home(_, q):
        await safe_edit(
            q.message,
            START_TEXT.format(name=q.from_user.first_name),
            get_start_menu()
        )
        await q.answer()

    print("[loaded] games.start")
