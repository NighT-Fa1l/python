import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Setup bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Auto-load cogs from all subfolders in "commands/"
async def load_cogs():
    for root, _, files in os.walk("commands"):
        for filename in files:
            if filename.endswith(".py"):
                cog = os.path.join(root, filename) \
                    .replace("/", ".") \
                    .replace("\\", ".")[:-3]  # convert path -> module
                try:
                    await bot.load_extension(cog)
                    print(f"✅ Loaded {cog}")
                except Exception as e:
                    print(f"❌ Failed to load {cog}: {e}")

@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")


async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    print(f"{message.author}: {message.content}")

    await bot.process_commands(message)
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
