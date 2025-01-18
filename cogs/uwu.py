import nextcord
from nextcord.ext import commands
from utils import links


class Uwu(commands.Cog):
    """just copying some owo commands"""

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def uwu(self, ctx):
        """UwU"""

        embed = nextcord.Embed(
            title="Mokshit is gay", 
            description="", color=nextcord.Colour.red()
            )
        embed.set_image(url=links.mokshit)

        await ctx.send(embed=embed)          

def setup(bot):
    bot.add_cog(Uwu(bot))
