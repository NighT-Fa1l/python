# 🤖 Discord.py Bot Template

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Discord.py](https://img.shields.io/badge/discord.py-v2.x-green.svg)](https://discordpy.readthedocs.io/en/stable/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A structured, scalable, and modular Discord bot template built using **discord.py (v2.x)** and Python. This template features an automated extension loader (Cogs system) and a native integration with the **OpenRouter API** for LLM-powered chat features.

---

## 🚀 How the Template Works

This template avoids the mess of writing a bot inside a single massive file by utilizing a modular architecture called **Cogs**. Here is how the different files connect seamlessly:

### 1. The Central Hub (`main.py`)
`main.py` is the entry point of your bot. It handles:
* Loading environment variables securely.
* Setting up client Intents.
* Initializing the bot and triggering the core asynchronous event loop.

### 2. Automatic Command Coupling
The magic of this template lies in its dynamic cog-loading mechanism located inside `main.py`:

```python
async def load_cogs():
    for root, _, files in os.walk("commands"):
        for filename in files:
            if filename.endswith(".py"):
                # Converts file path into a Python module import string
