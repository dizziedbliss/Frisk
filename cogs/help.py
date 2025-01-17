from nextcord.ext import commands


class Help(commands.Cog):
    """An Help command"""

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def help(self, ctx):
        """Displays all available commands."""
        await ctx.send("Here are all my commands:")


def setup(bot):
    bot.add_cog(Help(bot))