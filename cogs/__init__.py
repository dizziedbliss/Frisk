"""
import nextcord
from nextcord.ext import commands
from utils import links


class Classname(commands.Cog):
    '''docstring'''

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def CommandName(self, ctx):
        '''Command Description'''

        #your command logic here         

def setup(bot):
    bot.add_cog(Classname(bot))

"""