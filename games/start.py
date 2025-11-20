@bot.on_callback_query(filters.regex("^help_show$"))
async def help_show(_, q):
    try:
        commands_text = (
            "📜 **Available Commands**\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "👤 **Profile**\n"
            "• /profile – View your profile\n"
            "• /inventory – View your items\n"
            "• /stats – View your statistics\n\n"
            
            "🎮 **Games**\n"
            "• /flip – Coin flip\n"
            "• /roll – Dice roll\n"
            "• /fight – Battle another user\n"
            "• /guess – Guess the word\n\n"

            "⛏ **Mining**\n"
            "• /mine – Mine ores\n"
            "• /sell – Sell mined ores\n\n"

            "🛒 **Shop**\n"
            "• /buy – Purchase items\n\n"

            "📊 **Other**\n"
            "• /top – Leaderboard\n"
            "• /help – Show help menu\n"
        )

        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="help_menu")]
        ])

        await safe_edit(q.message, commands_text, kb)
        await q.answer()

    except Exception:
        traceback.print_exc()
