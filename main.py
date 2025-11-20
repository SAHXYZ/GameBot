# File: GameBot/main.py
from pyrogram import Client
import importlib
import traceback
import sys
import os
from config import API_ID, API_HASH, BOT_TOKEN
from database.mongo import client  # ensure MongoDB initializes first

# Ensure project root is on sys.path so "games.*" imports work whether run as:
#  - python GameBot/main.py
#  - python main.py
#  - python -m GameBot (package)
#  - python -m main  (if user tries that)
_this_dir = os.path.dirname(os.path.abspath(__file__))      # .../GameBot
_project_root = os.path.dirname(_this_dir)                   # parent of GameBot folder
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

# Also add _this_dir so relative imports resolve when running from that directory
if _this_dir not in sys.path:
    sys.path.insert(0, _this_dir)

bot = Client(
    "GameBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=32
)

def safe_init(module_name: str):
    """
    Load game modules safely.
    Tries a few candidate import paths to be resilient to different run modes.
    """
    candidates = []

    # Common: games.<module>
    candidates.append(f"games.{module_name}")

    # Package-style: GameBot.games.<module> (if folder name is GameBot)
    top_pkg = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
    candidates.append(f"{top_pkg}.games.{module_name}")

    # Try without package but with module name only (if someone placed module in same dir)
    candidates.append(module_name)

    last_exc = None
    for qualname in candidates:
        try:
            module = importlib.import_module(qualname)
            init_fn = getattr(module, f"init_{module_name}", None)
            if callable(init_fn):
                init_fn(bot)
                print(f"[loaded] {qualname}")
            else:
                print(f"[skipped] {qualname} (no init_{module_name} function)")
            return
        except Exception as e:
            last_exc = e
            print(f"[DEBUG] import '{qualname}' failed: {e}")

    # nothing worked
    print(f"[ERROR] Failed to load module '{module_name}'. Tried: {candidates}")
    if last_exc:
        traceback.print_exception(type(last_exc), last_exc, last_exc.__traceback__)

# Modules lists - adjust these if you add/remove modules
required_modules = [
    "start", "flip", "roll", "rob",
    "fight", "top"
]
optional_modules = [
    "profile", "work", "shop",
    "guess", "help", "mine"
]

def main():
    print("Initializing GameBot...\n")

    for module in required_modules:
        safe_init(module)

    for module in optional_modules:
        safe_init(module)

    # Load callbacks LAST (if present)
    safe_init("callbacks")

    print("\n✔ GameBot initialized. Starting client...")
    # Run the bot (this will block)
    bot.run()

if __name__ == "__main__":
    # Helpful note: on VPS you should run either:
    #   python3 main.py
    # or
    #   python3 -m GameBot    (if you want to run as a package and GameBot is a package)
    #
    # Avoid using `python3 -m main.py` — that form is invalid. If you intended to run the module,
    # use `-m main` or `-m GameBot` depending on packaging.
    main()
