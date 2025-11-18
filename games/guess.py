# filename: games/guess.py

from pyrogram import Client, filters
from pyrogram.types import Message
from database_main import db
import random

# Active games:
# { user_id: { "word": "apple", "hint": "a fruit...", "answer_mode": False } }
active_games = {}

# Dictionary of REAL hints for each word
HINTS = {
    "apple": "A popular fruit that keeps doctors away.",
    "brain": "The control center of the human body.",
    "chair": "Object used to sit on.",
    "dream": "Something you see while sleeping.",
    "eagle": "A large bird known for its sharp eyesight.",
    "flame": "The visible, glowing part of a fire.",
    "globe": "A 3D model of Earth.",
    "heart": "The organ that pumps blood.",
    "island": "A landmass surrounded entirely by water.",
    "joker": "A funny character or a wild playing card.",
    "knife": "A tool used for cutting.",
    "lemon": "A sour yellow fruit.",
    "magic": "Supernatural or illusion-based actions.",
    "night": "The time of darkness after sunset.",
    "ocean": "A vast body of saltwater.",
    "piano": "A musical instrument with black and white keys.",
    "queen": "A female ruler or a chess piece.",
    "river": "A natural flowing stream of water.",
    "stone": "A hard solid material from the ground.",
    "train": "A fast vehicle running on tracks.",
    "urban": "Something related to cities.",
    "vivid": "Bright, clear, and full of life.",
    "whale": "The largest mammal on Earth.",
    "xenon": "A noble gas used in bright lamps.",
    "yacht": "A luxurious boat.",
    "zebra": "A black and white striped animal.",
    "nose": "The body part used for breathing and smelling.",
}

WORD_LIST = list(HINTS.keys())

def init_guess(bot: Client):

    # -------------------------
    # START GAME
    # -------------------------
    @bot.on_message(filters.command("guess"))
    async def start_guess(_, msg: Message):
        if not msg.from_user:
            return

        user_id = str(msg.from_user.id)

        if user_id in active_games:
            return await msg.reply("You already have an active game.\nUse /stop to end it.")

        # Pick random word
        word = random.choice(WORD_LIST)
        hint = HINTS[word]

        active_games[user_id] = {
            "word": word,
            "hint": hint,
            "answer_mode": False,
        }

        await msg.reply(
            f"🧩 **Guess The Word!**\n\n"
            f"🔎 **Hint:** {hint}\n\n"
            f"Type **/answer** to start guessing mode."
        )

    # -------------------------
    # ENTER ANSWER MODE
    # -------------------------
    @bot.on_message(filters.command("answer"))
    async def enable_answer_mode(_, msg: Message):
        user_id = str(msg.from_user.id)

        if user_id not in active_games:
            return await msg.reply("No active game.\nStart one with /guess.")

        active_games[user_id]["answer_mode"] = True

        await msg.reply(
            "📝 **Answer mode enabled!**\n"
            "Now send your guess normally.\n"
            "Type /stop to end the game."
        )

    # -------------------------
    # PROCESS USER MESSAGES (ANSWER MODE)
    # -------------------------
    @bot.on_message(filters.text & ~filters.command(["guess", "answer", "stop"]))
    async def check_guess(_, msg: Message):

        user_id = str(msg.from_user.id)
        if user_id not in active_games:
            return  # not playing

        # Only accept input if user enabled answer mode
        if not active_games[user_id]["answer_mode"]:
            return

        guess = msg.text.strip().lower()
        correct = active_games[user_id]["word"]

        if guess == correct:
            user = db.get_user(msg.from_user.id)
            reward = random.randint(20, 120)

            # Reward in bronze only
            user["bronze"] = user.get("bronze", 0) + reward
            db.update_user(msg.from_user.id, user)

            del active_games[user_id]

            return await msg.reply(
                f"🎉 **Correct!**\n"
                f"You earned **{reward} Bronze 🥉**."
            )

        # Wrong guess
        await msg.reply("❌ Wrong guess. Try again!")

    # -------------------------
    # STOP GAME
    # -------------------------
    @bot.on_message(filters.command("stop"))
    async def stop_guess(_, msg: Message):
        user_id = str(msg.from_user.id)

        if user_id in active_games:
            del active_games[user_id]
            return await msg.reply("🛑 Guess game stopped.")

        await msg.reply("You have no active game.")
