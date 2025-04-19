import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from db.firebase import initialize_firebase
from cogs.flashcards import Flashcards
import json
import asyncio
from flask import Flask, request


load_dotenv()
token = os.getenv("TOKEN")
CHANNEL_ID = 1363086639622262984

initialize_firebase()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

app = Flask(__name__)

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("!"),
    description="Study Buddy Bot to help you stay productive!",
    intents=intents,
)
bot.remove_command('help')


async def load_cogs():
    await bot.load_extension("cogs.flashcards")
    await bot.load_extension("cogs.help")
    await bot.load_extension("cogs.timer")

async def setup_hook():
    await load_cogs()

bot.setup_hook = setup_hook

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

@app.route("/github", methods=["POST"])
def github_webhook():
    data = request.json
    repo = data["repository"]["name"]
    pusher = data["pusher"]["name"]
    msg = f"New commit to {repo} by {pusher}:\n"
    asyncio.run_coroutine_threadsafe(send_to_discord(msg), bot.loop)
    return "", 204

async def send_to_discord(msg):
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(msg)
    else:
        print("Channel not found")
        
import threading
threading.Thread(target=app.run, kwargs={"port": 5000}).start()    
        
bot.run(token)
