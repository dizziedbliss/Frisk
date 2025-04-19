import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
from flask import Flask, request
import threading

# Load environment variables from .env file
load_dotenv()

# Get the bot token and channel ID from environment variables
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = 1363086639622262984

# Set up discord intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# Initialize Flask app
app = Flask(__name__)

# Initialize Discord bot with the given command prefix and description
bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("!"),
    description="Looking for a life on Valoria",
    intents=intents,
)

# Remove the default help command
bot.remove_command('help')

# Flask route for receiving GitHub webhook payload
@app.route("/github", methods=["POST"])
def github_webhook():
    data = request.json
    
    
    print("Received GitHub Webhook Data:", data)
    
    
    repo = data.get("hook", {}).get("name", "Unknown Repo")
    pusher = data.get("sender", {}).get("login", "Unknown Pusher")
    commit_url = data.get("head_commit", {}).get("url", "No commit URL available")  # URL to the commit
    
    # Create embedded message for Discord
    embed = discord.Embed(
        title=f"New commit to {repo}",
        description=f"**Commit by**: {pusher}",
        color=discord.Color.blue(),
    )
    embed.add_field(name="Commit URL", value=f"[Click here]({commit_url})", inline=False)
    embed.add_field(name="Repository", value=repo, inline=True)
    embed.add_field(name="Pusher", value=pusher, inline=True)

    # Send the embed message to Discord asynchronously
    asyncio.run_coroutine_threadsafe(send_to_discord(embed), bot.loop)
    
    return "", 204

# Function to send the embed to Discord
async def send_to_discord(embed):
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(embed=embed)
    else:
        print("Channel not found")

# Run the Flask app in a separate thread to avoid blocking the bot
def run_flask():
    app.run(host='0.0.0.0', port=8080)

# Start Flask app in a separate thread
threading.Thread(target=run_flask, daemon=True).start()

# Run the bot
bot.run(TOKEN)
