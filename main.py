import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from db.firebase import initialize_firebase
from cogs.flashcards import Flashcards
import json
import asyncio

load_dotenv()
token = os.getenv("TOKEN")

initialize_firebase()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

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

bot.run(token)
