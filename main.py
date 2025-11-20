from pyrogram import Client
import importlib
import traceback
from config import API_ID, API_HASH, BOT_TOKEN
from database.mongo import client  # ensure MongoDB initializes first

bot = Client(
    "GameBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=32
)

def safe_init(module_name: str):
    """Load game modules safely."""
    try:
        module = importlib.import_module(f"games.{module_name}")
        init_fn = getattr(module, f"init_{module_name}", None)

        if callable(init_fn):
            init_fn(bot)
            print(f"[loaded] games.{module_name}")
        else:
            print(f"[skipped] games.{module_name} (no init function)")

    except Exception as e:
        print(f"[ERROR] Failed loading module: {module_name} -> {e}")
        traceback.print_exc()

# Required modules (DO NOT load callbacks twice)
required_modules = [
    "start", "flip", "roll", "rob",
    "fight", "top"
]

# Optional modules
optional_modules = [
    "profile", "work", "shop",
    "guess", "help", "mine"
]

if __name__ == "__main__":
    print("Initializing GameBot...\n")

    for module in required_modules:
        safe_init(module)

    for module in optional_modules:
        safe_init(module)

    # Load callbacks LAST
    safe_init("callbacks")

    print("\n✔ GameBot is running with MongoDB!")
    bot.run()
