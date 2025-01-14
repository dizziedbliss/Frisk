from discord.ext import commands
from db.firebase import add_flashcard, get_flashcards, delete_flashcard, practice_flashcards

class Flashcards(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='addflashcard', aliases=['af', 'flashit', 'addflash', 'memorize'], help='Add a flashcard to the database')
    async def add_flashcard(self, ctx, question, *, answer):
        add_flashcard(question, answer)
        await ctx.send('Flashcard added!')

    @commands.command(name='get_flashcards', aliases=['flash', 'gf', 'glance'], help='Get all flashcards from the database')
    async def get_flashcards(self, ctx):
        flashcards = get_flashcards()
        if flashcards:
            card = flashcards[0]
            await ctx.send(f"Flashcard: {card['question']} - {card['answer']}")
        else:
            await ctx.send('No flashcards found')
        
    @commands.command(name='delete_flashcard', aliases=['delete', 'df'], help='Delete a flashcard from the database')
    async def delete_flashcard(self, ctx, question):
        if delete_flashcard(question):
            await ctx.send('Flashcard deleted!')
        else:
            await ctx.send('Flashcard not found')
            
    @commands.command(name='practice', aliases=['p'], help='Practice flashcards')
    async def practice(self, ctx):
        practice_flashcards()
        
async def setup(bot):
    await bot.add_cog(Flashcards(bot))