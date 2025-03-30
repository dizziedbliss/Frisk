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
            description="A list of commands for Dummies", color=red
            )
        embed.set_author(name="Frisk", url=None, icon_url=links.authorPFP)


        embed.add_field(name="Help", value="Stuck?? Get help.\n *useage*- `help` or `h`", inline=False)
        embed.add_field(name="Music", value="The place where the world lies, there's a whole another help menu for this\n *useage*- `musichelp`", inline=False)


        embed.set_image(url=links.helpBanner)
        embed.set_footer(text="Reading a long list of commands fills you with determination.❤️")

        
        await ctx.send(embed=embed)          
    

    @commands.command()
    async def musichelp(self, ctx):
        """Displays all available music commands."""
        embed = nextcord.Embed(
            title="Music Help Menu", 
            description="A list of music commands for Dummies", color=red
            )
        embed.set_author(name="Frisk", url=None, icon_url=links.authorPFP)
        embed.add_field(name="Play", value="Plays a song from the given URL or Song Name or even a Playlist\n *useage*- `play [URL/Name]` or `p [URL/Name]` ", inline=False)
        embed.add_field(name="Pause", value="Pauses the current song\n *useage*- `pause`", inline=False)
        embed.add_field(name="Resume", value="Resumes the current paused song\n *useage*- `resume`", inline=False)
        embed.add_field(name="Stop", value="Stops the current song\n *useage*- `stop`", inline=False)
        embed.add_field(name="Next", value="Skips to the next song in the queue\n *useage*- `next`", inline=False)
        embed.add_field(name="Previous", value="Skips to the previous song in the queue\n *useage*- `prev`", inline=False)
        embed.add_field(name="Queue", value="Displays the current song queue\n *useage*- `queue` or `q`", inline=False)
        embed.add_field(name="Volume", value="Adjusts the volume of the current song\n *useage*- `volume [number 1-100]` or `vol [number 1-100]", inline=False)
        embed.add_field(name="Loop", value="Toggles looping of the current song\n *useage*- `loop [number]` or `lp [number]`", inline=False)
        embed.set_image(url=links.helpsongs)
        embed.set_footer(text="Reading a long list of commands fills you with determination❤️.")

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))
    