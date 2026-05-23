# 🤖 Discord Bot Template

A clean, modular Discord bot template built with **discord.py** and **OpenRouter AI**. Drop new command files into the `commands/` folder and they load automatically — no rewiring `main.py` ever.

---

## 📁 Project Structure

```
discord bot template/
├── main.py                   # Bot entry point — loads all cogs automatically
├── chat.py                   # Standalone CLI chatbot (for testing AI outside Discord)
├── .env                      # Your secret keys (never commit this)
└── commands/
    ├── fun/
    │   └── chatbot.py        # AI chatbot cog (responds when mentioned)
    └── mod/
        └── moderation.py     # Moderation cog (kick, ban, timeout)
```

---

## ⚙️ How It Works

### `main.py` — The Core

`main.py` is the heart of the bot. On startup it calls `load_cogs()`, which **automatically walks every subfolder inside `commands/`** and loads any `.py` file it finds as a discord.py **Cog** (extension):

```python
async def load_cogs():
    for root, _, files in os.walk("commands"):
        for filename in files:
            if filename.endswith(".py"):
                cog = os.path.join(root, filename) \
                    .replace("/", ".") \
                    .replace("\\", ".")[:-3]  # converts path → module string
                await bot.load_extension(cog)
```

The file path is converted into a Python module string — for example, `commands/fun/chatbot.py` becomes `commands.fun.chatbot` — and loaded with `bot.load_extension()`.

**This means you never need to touch `main.py` to add new commands.** Just create a new `.py` file anywhere inside `commands/`, make sure it has a `setup(bot)` function at the bottom, and it will be picked up on the next run automatically.

### Adding a New Command File

Every file inside `commands/` must expose a `setup` function so discord.py knows how to register it:

```python
# commands/fun/my_new_command.py

from discord.ext import commands

class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        await ctx.send("Hello!")

async def setup(bot):          # ← required
    await bot.add_cog(MyCog(bot))
```

That's it. Drop it in, restart the bot, and `load_cogs()` handles the rest.

---

## 🔐 Environment Variables (`.env`)

Sensitive credentials are stored in a `.env` file at the project root and loaded with `python-dotenv`. **This file should never be committed to Git.**

```env
DISCORD_TOKEN=your_discord_bot_token_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

| Variable | Used In | Description |
|---|---|---|
| `DISCORD_TOKEN` | `main.py` | Your bot's token from the [Discord Developer Portal](https://discord.com/developers/applications) |
| `OPENROUTER_API_KEY` | `commands/fun/chatbot.py`, `chat.py` | API key from [OpenRouter](https://openrouter.ai) for AI responses |

Both `main.py` and any cog that needs AI simply call:

```python
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
KEY   = os.getenv("OPENROUTER_API_KEY")
```

Add a `.gitignore` entry to make sure `.env` is never accidentally pushed:

```
.env
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/discord-bot-template.git
cd discord-bot-template
```

### 2. Install dependencies

```bash
pip install discord.py python-dotenv openrouter
```

### 3. Create your `.env` file

```bash
cp .env.example .env   # or create it manually
```

Fill in your `DISCORD_TOKEN` and `OPENROUTER_API_KEY`.

### 4. Run the bot

```bash
python main.py
```

The console will show which cogs loaded successfully:

```
✅ Loaded commands.fun.chatbot
✅ Loaded commands.mod.moderation
Bot logged in as YourBot#1234
```

---

## 🧪 Testing AI Without Discord

`chat.py` is a lightweight **CLI chatbot** that talks directly to OpenRouter — useful for testing your AI prompt/model without spinning up the full Discord bot:

```bash
python chat.py
ask> what is the speed of light?
reply> 299,792,458 m/s in a vacuum.
ask> exit
```

It uses the same `OPENROUTER_API_KEY` from `.env`.

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `discord.py` | Discord bot framework |
| `python-dotenv` | Load `.env` variables |
| `openrouter` | OpenRouter AI client |

---

## 📝 License

This project is open source. Feel free to fork and build on top of it.
