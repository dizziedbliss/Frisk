from dotenv import load_dotenv
import hikari
import os
import config
import wavelink

load_dotenv()
token = os.getenv("TOKEN")


intents = 
intents.messages = True
intents.guilds = True
intents.message_content = True


import hikari

bot = hikari.GatewayBot(token=token)

@bot.listen()
async def ping(event: hikari.MessageCreateEvent) -> None:
    """If a non-bot user mentions your bot, respond with 'Pong!'."""

    # Do not respond to bots nor webhooks pinging us, only user accounts
    if not event.is_human:
        return

    me = bot.get_me()

    if me.id in event.message.user_mentions_ids:
        await event.message.respond("Pong!")

bot.run()
bot = Bot(intents=intents)

bot.run(token)
