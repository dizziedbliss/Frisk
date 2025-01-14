
import discord
from discord.ext import commands
import random
import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials


load_dotenv()
token = os.getenv('TOKEN')

cred = credentials.Certificate("frisk-dizziedbliss-firebase-adminsdk-lrkge-5e2db57f8e.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://frisk-dizziedbliss-default-rtdb.firebaseio.com/'
})

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), description="Study Buddy Bot to help you stay productive!", intents=intents)

ref = db.reference('flashcards')
ref.push({"question": "What is the capital of France?", "answer": "Paris"})

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! 🏓 {round(bot.latency * 1000)}ms")

flashcards = ref.get()

@bot.command()
async def flash(ctx):
    await ctx.send(flashcards)


bot.run(token)