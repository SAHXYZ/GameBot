# File: GameBot/games/profile.py

from database.mongo import get_user
from games.start import START_TEXT

# --------------------------------------
# Total bronze value calculator
# --------------------------------------
def total_bronze_value(user: dict) -> int:
    black = int(user.get("black_gold", 0)) * 100000000
    plat  = int(user.get("platinum", 0)) * 1000000
    gold  = int(user.get("gold", 0)) * 10000
    sil   = int(user.get("silver", 0)) * 100
    bron  = int(user.get("bronze", 0))
    return black + plat + gold + sil + bron


# --------------------------------------
# BUILD PROFILE TEXT
# --------------------------------------
def build_profile_text_for_user(user: dict, mention: str):

    # Currency
    black_gold = int(user.get("black_gold", 0))
    platinum   = int(user.get("platinum", 0))
    gold       = int(user.get("gold", 0))
    silver     = int(user.get("silver", 0))
    bronze     = int(user.get("bronze", 0))
    total_val  = total_bronze_value(user)

    # Stats
    messages   = user.get("messages", 0)
    wins       = user.get("fight_wins", 0)
    rob_s      = user.get("rob_success", 0)
    rob_f      = user.get("rob_fail", 0)

    # Badges
    badges = " ".join(user.get("badges", [])) or "None"

    # Inventory
    inv = user.get("inventory", {})
    ores = inv.get("ores", {})
    items = inv.get("items", [])

    ore_summary = ", ".join([f"{k}({v})" for k, v in ores.items()]) or "No ores"
    items_summary = ", ".join(items) or "No items"

    # Tools
    tools = user.get("tools", {})
    equipped = user.get("equipped") or "None"
    dur = user.get("tool_durabilities", {}).get(equipped, "N/A")

    text = (
        f"👤 **Profile of {mention}**\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"

        f"💰 **Currency**\n"
        f"🎖 Black Gold: `{black_gold}`\n"
        f"🏅 Platinum: `{platinum}`\n"
        f"🥇 Gold: `{gold}`\n"
        f"🥈 Silver: `{silver}`\n"
        f"🥉 Bronze: `{bronze}`\n"
        f"🔢 Total Value: `{total_val}`\n\n"

        f"📊 **Stats**\n"
        f"💬 Messages: `{messages}`\n"
        f"🥊 Fight Wins: `{wins}`\n"
        f"🕵️ Rob Success: `{rob_s}`\n"
        f"🚨 Rob Failures: `{rob_f}`\n\n"

        f"⛏️ **Mining**\n"
        f"🧰 Equipped Tool: `{equipped}`\n"
        f"🔧 Durability: `{dur}`\n\n"

        f"⛏️ Ores: {ore_summary}\n"
        f"🛒 Items: {items_summary}\n\n"

        f"🏅 **Badges:** {badges}\n"
    )

    return text


# --------------------------------------
# Profile Markup (buttons)
# --------------------------------------
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_profile_markup():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back", callback_data="back_to_home")]
    ])
