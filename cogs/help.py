import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", aliases=["h"], help="Get help on how to use the bot")
    async def help(self, ctx):
        help_message = discord.Embed(
            title="Frisk Help Menu",
            description="Command list for Dummies",
            color=discord.Color.red(),
        )
        help_message.add_field(
            name="help",
            commands="`help`, `h`",
            value="You've just used it lol",
            inline=False,
        )
        help_message.add_field(
            name="add flashcards",
            commands="`add_flashcard`, `af`, `flashit`, `addflash`, `memorize`",
            value="Add a flashcards to memorize later",
            inline=False,
        )
        help_message.add_field(
            name="get flashcards",
            commands="`get_flashcards`, `flash`, `gf`, `glance`",
            value="Get all flashcards that you've saved",
            inline=False,
        )
        help_message.add_field(
            name="delete flashcards",
            commands="`delete_flashcard`, `delete`, `df`",
            value="Delete a flashcard from the database",
            inline=False,
        )
        help_message.add_field(
            name="practice flashcards",
            commands="`practice`, `p`",
            value="Practice flashcards",
            inline=False,
        )
        help_message.add_field(
            name="study timer",
            commands="`timer`,`ss`,`startsession`, `st`, `study`, `start`",
            value="Set a timer to study [minutes]",
            inline=False,
        )
        help_message.add_field(
            name="stop timer",
            commands="`es`, `endsession`, `stop`, `end`",
            value="Stops the timer",
            inline=False,
        )
        help_message.add_field(
            name="remainder",
            commands="`remindmein`, `remind`, `reminder`",
            value="reminds you about a task in a given time [minutes]",
            inline=False,
        )
        help_message.add_field(
            name = 'cancel reminder',
            commands = '`cancelreminder`, `cr`',
            value = 'Cancels a previously set reminder',
            inline = False
        )
        help_message.add_field(
            name = 'list reminders',
            commands = '`listreminders`, `lr`',
            value = 'Lists all currently set reminders',
            inline = False
        )

        await ctx.send(help_message)


async def setup(bot):
    await bot.add_cog(Help(bot))
