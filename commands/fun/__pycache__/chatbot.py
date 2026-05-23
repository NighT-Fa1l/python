import os
import discord
from openrouter import OpenRouter
from discord.ext import commands
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv


load_dotenv()
# name of model from openrouter
model = "deepseek/deepseek-chat"
key = os.getenv("OPENROUTER_API_KEY")  


class ChatBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_mentioned = {}
        self.focused_user = None
        self.focus_time = timedelta(minutes=1)
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        now = datetime.now()

        # user focus
        if self.focused_user:
            last_time = self.last_mentioned.get(self.focused_user.id, datetime.min)
            if now - last_time > self.focus_time:
                print(f"Focus expired for {self.focused_user}")
                self.focused_user = None

        # set focus
        if self.bot.user.mentioned_in(message) or 'bot' in message.content.lower():
            self.focused_user = message.author
            self.last_mentioned[message.author.id] = now

            print(f"Focus set to {message.author}")
            await self.respond(message)

        # continues chatting
        elif self.focused_user and message.author.id == self.focused_user.id:
            self.last_mentioned[message.author.id] = now

            print(f"Continuing focus with {message.author}")
            await self.respond(message)

        await self.bot.process_commands(message)

    async def respond(self, message):
        with OpenRouter(api_key=key) as client:
            try:
                # set the personality of bot
                res = client.chat.send(
                    model="deepseek/deepseek-chat",
                    messages=[
                        {"role": "system", "content": "you ans questions, keep them simple and not too big."},
                        #{"role": "system", "content": "you hear donald trump replay with orange pig as you call him a orange pig,you hate israel,you dont like the word israel,everytime u see the word israel reply with ""fk israel"",You are a chatbot who gives short, simple answers. No extra details, no enthusiasm. If someone asks you a question, you do not greet anyone just replay, your text should be like your extremely bored and dont care."},
                        {"role": "user", "content": message.content}
                    ]
                )

                #print("reply>", res.choices[0].message.content)

            except Exception as e:
                print("Error:", e)

            await message.reply(res.choices[0].message.content) 


async def setup(bot):
    await bot.add_cog(ChatBot(bot))
   # {"role": "system", "content": "you ans questions, keep them simple and not too big."},
   #{"role": "system", "content": "you hear donald trump replay with orange pig as you call him a orange pig,you hate israel,you dont like the word israel,everytime u see the word israel reply with ""fk israel"",You are a chatbot who gives short, simple answers. No extra details, no enthusiasm. If someone asks you a question, you do not greet anyone just replay, your text should be like your extremely bored and dont care."},
   
