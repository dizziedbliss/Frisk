from dotenv import load_dotenv
import os
from nextcord.ext import commands

load_dotenv()
token = os.getenv("TOKEN")

# the prefix is not used in this example
bot = commands.Bot(command_prefix='$')

@bot.event
async def on_message(message):
    print(f'Message from {message.author}: {message.content}')

bot.run(token)
