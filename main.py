
import discord
from discord.ext import commands
import random
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('TOKEN')


intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), description="Study Buddy Bot to help you stay productive!", intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! 🏓 {round(bot.latency * 1000)}ms")




bot.run(token)