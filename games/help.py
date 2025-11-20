# File: GameBot/games/help.py
from pyrogram import Client, filters
from pyrogram.types import Message
import traceback


def init_help(bot: Client):

    @bot.on_message(filters.command(["help", "commands"]))
    async def help_cmd(_, msg: Message):
        try:
            text = (
                "⟦⟡⟧  H E L P   C E N T E R  ⟦⟡⟧\n"
                "Your command arsenal.\n"
                "Mᴀꜱᴛᴇʀ ᴛʜᴇ Gʀɪᴅ. Cᴏɴᴛʀᴏʟ ᴛʜᴇ Pʟᴀʏ. ⚡\n\n"

                "▐█▌  P R O F I L E\n"
                "• /profile — Vɪᴇᴡ Yᴏᴜʀ Pʀᴏꜰɪʟᴇ\n"
                "▞━━━━━━━━━━━━━━━━━━━━▚\n\n"

                "▐█▌  G A M E S\n"
                "• /flip — Cᴏɪɴ Fʟɪᴘ Dᴜᴇʟ\n"
                "• /roll — Dɪᴄᴇ Rᴏʟʟ\n"
                "• /fight — Fɪɢʜᴛ Aɴᴏᴛʜᴇʀ Pʟᴀʏᴇʀ\n"
                "• /rob — Rᴏʙ A Pʟᴀʏᴇʀ (Rɪꜱᴋ + Rᴇᴡᴀʀᴅ)\n"
                "• /guess — Gᴜᴇꜱꜱ Tʜᴇ Hɪᴅᴅᴇᴅ Wᴏʀᴅ\n"
                "▞━━━━━━━━━━━━━━━━━━━━▚\n\n"

                "▐█▌  M I N I N G\n"
                "• /mine — Mɪɴᴇ Oʀᴇꜱ\n"
                "• /sell — Sᴇʟʟ Yᴏᴜʀ Mɪɴᴇᴅ Oʀᴇꜱ\n"
                "▞━━━━━━━━━━━━━━━━━━━━▚\n\n"

                "▐█▌  S H O P\n"
                "• /shop — Vɪᴇᴡ Sʜᴏᴘ Iᴛᴇᴍꜱ\n"
                "• /buy <item> — Bᴜʏ Iᴛᴇᴍꜱ/Tools\n"
                "▞━━━━━━━━━━━━━━━━━━━━▚\n\n"

                "▐█▌  O T H E R\n"
                "• /leaderboard — Tᴏᴘ Pʟᴀʏᴇʀꜱ\n"
                "• /work — Eᴀʀɴ Bʀᴏɴᴢᴇ Cᴏɪɴꜱ\n"
                "▞━━━━━━━━━━━━━━━━━━━━▚\n\n"

                "⟡ Tɪᴘ: Uꜱᴇ ᴄᴏᴍᴍᴀɴᴅꜱ ɪɴ ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ ꜰᴏʀ ᴘᴇᴀᴋ ᴘᴇʀꜰᴏʀᴍᴀɴᴄᴇ.\n"
                "Wᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ Pʀɪᴍᴇ-ᴛɪᴇʀ Rᴇᴀʟᴍ. ⚡"
            )

            await msg.reply_text(text)

        except Exception:
            traceback.print_exc()
            try:
                await msg.reply_text("⚠️ Failed to load help menu.")
            except:
                pass
