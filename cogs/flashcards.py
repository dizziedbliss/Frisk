from discord.ext import commands
from db.firebase import add_flashcard, get_flashcards

class Flashcards(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='add_flashcard', help='Add a flashcard to the database')
    async def add_flashcard(self, ctx, question, *, answer):
        add_flashcard(question, answer)
        await ctx.send('Flashcard added!')

    @commands.command(name='get_flashcards', help='Get all flashcards from the database')
    async def get_flashcards(self, ctx):
        flashcards = get_flashcards()
        if flashcards:
            card = flashcards[0]
            await ctx.send(f"Flashcard: {card['question']} - {card['answer']}")
        else:
            await ctx.send('No flashcards found')
            
async def setup(bot):
    await bot.add_cog(Flashcards(bot))