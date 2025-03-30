from dotenv import load_dotenv
from nextcord.ext import commands
import nextcord
import os
import config

load_dotenv()
token = os.getenv("TOKEN")


intents = nextcord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True


class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix=commands.when_mentioned_or('$'), intents=kwargs.pop('intents', None), help_command=None)
        for cog in config.cogs:
            try:
                self.load_extension(cog)
            except Exception as exc:
                print(f'Could not load extension {cog} due to {exc.__class__.__name__}: {exc}')

    async def on_ready(self):
        print(f'Logged on as {self.user} (ID: {self.user.id})')


bot = Bot(intents=intents)

# write general commands here

bot.run(token)