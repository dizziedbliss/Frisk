
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from db.firebase import initialize_firebase
from cogs.flashcards import Flashcards
import json

load_dotenv()
token = os.getenv('TOKEN')

initialize_firebase()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), description="Study Buddy Bot to help you stay productive!", intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    
    await bot.load_extension('cogs.flashcards')


bot.run(token)