from openrouter import OpenRouter
from dotenv import load_dotenv
import os
import time

load_dotenv()

key = os.getenv("OPENROUTER_API_KEY")

with OpenRouter(api_key=key) as client:

    while True:
        user = input("ask> ")

        if user.lower() in ["exit", "quit"]:
            break

        try:
            # Updated system message with more clarity
            res = client.chat.send(
                model="deepseek/deepseek-chat",
                messages=[
                    {"role": "system", "content": "You are a chatbot who gives short, simple answers. No extra details, no enthusiasm. If someone asks you a question, you do not greet anyone just replay, your text should be like your extremely bored and dont care."},
                    {"role": "user", "content": user}
                ]
            )

            print("reply>", res.choices[0].message.content)

        except Exception as e:
            print("Error:", e)
            print("Waiting 5 seconds...")
            time.sleep(5)

