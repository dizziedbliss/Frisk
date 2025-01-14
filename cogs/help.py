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
            value="Commands: `help`, `h`\nDescription: You've just used it lol",
            inline=False,
        )
        help_message.add_field(
            name="add flashcards",
            value="Commands: `add_flashcard`, `af`, `flashit`, `addflash`, `memorize`\nDescription: Add flashcards to memorize later",
            inline=False,
        )
        help_message.add_field(
            name="get flashcards",
            value="Commands: `get_flashcards`, `flash`, `gf`, `glance`\nDescription: Get all flashcards that you've saved",
            inline=False,
        )
        help_message.add_field(
            name="delete flashcards",
            value="Commands: `delete_flashcard`, `delete`, `df`\nDescription: Delete a flashcard from the database",
            inline=False,
        )
        help_message.add_field(
            name="practice flashcards",
            value="Commands: `practice`, `p`\nDescription: Practice flashcards",
            inline=False,
        )
        help_message.add_field(
            name="study timer",
            value="Commands: `timer`, `ss`, `startsession`, `st`, `study`, `start`\nDescription: Set a timer to study [minutes]",
            inline=False,
        )
        help_message.add_field(
            name="stop timer",
            value="Commands: `es`, `endsession`, `stop`, `end`\nDescription: Stops the timer",
            inline=False,
        )
        help_message.add_field(
            name="remainder",
            value="Commands: `remindmein`, `remind`, `reminder`\nDescription: Reminds you about a task in a given time [minutes]",
            inline=False,
        )
        help_message.add_field(
            name="cancel reminder",
            value="Commands: `cancelreminder`, `cr`\nDescription: Cancels a previously set reminder",
            inline=False,
        )
        help_message.add_field(
            name="list reminders",
            value="Commands: `listreminders`, `lr`\nDescription: Lists all currently set reminders",
            inline=False,
        )

        await ctx.send(embed=help_message)


async def setup(bot):
    await bot.add_cog(Help(bot))
