import nextcord
from nextcord.ext import commands
from utils import links


class Help(commands.Cog):
    """A custom Help command"""

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=['h'])
    async def help(self, ctx):
        """Displays all available commands."""
        embed = nextcord.Embed(
            title="Help Menu", 
            description="A list of commands for Dummies", color=nextcord.Colour.red()
            )
        embed.set_author(name="Frisk", url=None, icon_url=links.authorPFP)
        embed.add_field(name="Help", value="Stuck?? Get help.\n *useage*- `help` or `h`", inline=True)
        embed.set_image(url=links.helpBanner)
        embed.set_footer(text="Reading a long list of commands fills you with determination.❤️")

        
        await ctx.send(embed=embed)          

def setup(bot):
    bot.add_cog(Help(bot))
    