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

    # Push Event Handler
    if "ref" in data and data["ref"].startswith("refs/heads"):
        repo_name = data["repository"]["full_name"]
        pusher = data["sender"]["login"]
        commit_message = data["head_commit"]["message"]
        commit_url = data["head_commit"]["url"]
        commit_author = data["head_commit"]["author"]["name"]
        
        # Create Push Embed
        embed = discord.Embed(
            title=f"🚀 New Push to {repo_name}",
            description=f"**Pushed by**: {pusher} 🚀",
            color=discord.Color.green(),
        )
        embed.add_field(name="Commit Message", value=f"**{commit_message}**", inline=False)
        embed.add_field(name="Commit URL", value=f"[Click here to view the commit]({commit_url})", inline=False)
        embed.add_field(name="Commit Author", value=commit_author, inline=True)
        embed.set_footer(text="Let the code flow! 🔥")

        # Send the embed to Discord
        asyncio.run_coroutine_threadsafe(send_to_discord(embed), bot.loop)

    # Handle Pull Request Event
    if "pull_request" in data:
        pr_title = data["pull_request"]["title"]
        pr_url = data["pull_request"]["html_url"]
        pr_state = data["pull_request"]["state"]
        pr_creator = data["pull_request"]["user"]["login"]
        repo_name = data["repository"]["full_name"]
        
        # Create Pull Request Embed
        embed = discord.Embed(
            title=f"🔀 New Pull Request in {repo_name}",
            description=f"**Created by**: {pr_creator}",
            color=discord.Color.blue(),
        )
        embed.add_field(name="PR Title", value=f"**{pr_title}**", inline=False)
        embed.add_field(name="PR URL", value=f"[Click here to view the pull request]({pr_url})", inline=False)
        embed.add_field(name="PR State", value=f"Status: {pr_state.capitalize()}", inline=True)
        embed.set_footer(text="Collaboration in action! 💪")

        # Send the embed to Discord
        asyncio.run_coroutine_threadsafe(send_to_discord(embed), bot.loop)

    # Handle Issue Event
    if "issue" in data:
        issue_title = data["issue"]["title"]
        issue_url = data["issue"]["html_url"]
        issue_state = data["issue"]["state"]
        issue_creator = data["issue"]["user"]["login"]
        repo_name = data["repository"]["full_name"]
        
        # Create Issue Embed
        embed = discord.Embed(
            title=f"📝 New Issue in {repo_name}",
            description=f"**Reported by**: {issue_creator}",
            color=discord.Color.orange(),
        )
        embed.add_field(name="Issue Title", value=f"**{issue_title}**", inline=False)
        embed.add_field(name="Issue URL", value=f"[Click here to view the issue]({issue_url})", inline=False)
        embed.add_field(name="Issue State", value=f"Status: {issue_state.capitalize()}", inline=True)
        embed.set_footer(text="Let's get it fixed! 🛠️")

        # Send the embed to Discord
        asyncio.run_coroutine_threadsafe(send_to_discord(embed), bot.loop)

    # Handle Starred Event
    if "starred" in data:
        starred_by = data["starred"]["user"]["login"]
        repo_name = data["repository"]["full_name"]

        # Create Starred Embed
        embed = discord.Embed(
            title=f"⭐️ New Star on {repo_name}",
            description=f"**Starred by**: {starred_by}",
            color=discord.Color.purple(),
        )
        embed.add_field(name="Repository Starred", value=f"**{repo_name}** is now more famous! 🌟", inline=False)
        embed.set_footer(text="Keep those stars coming! ✨")

        # Send the embed to Discord
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
