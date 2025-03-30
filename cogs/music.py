import nextcord
from utils import links
import asyncio
import wavelink

class Music(commands.Cog):
    """A command for playing music from youtube and youtube music"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['p'])
    async def play(self, ctx, *, query=None):
        """Plays music from a given song name/link/playlist (YouTube only)"""

    @commands.command()
    async def stop(self, ctx):
        """Stops the music"""

    @commands.command()
    async def pause(self, ctx):
        """Pauses the music"""
      
    @commands.command()
    async def resume(self, ctx):
        """Resumes the paused music"""
       
    @commands.command()
    async def next(self, ctx):
        """Skips to the next song"""
    
    @commands.command()
    async def prev(self, ctx):
        """Plays the previous song"""

    @commands.command()
    async def queue(self, ctx):
        """Displays the current song queue"""
      

def setup(bot):
    bot.add_cog(Music(bot))