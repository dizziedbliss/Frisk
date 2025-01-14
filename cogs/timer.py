import asyncio
from discord.ext import commands

bot = commands.Bot(command_prefix="!")

# To track timers per user
active_timers = {}

class Timer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='timer', aliases=['ss', 'startsession', 'st', 'study', 'start'], help='Set a study session timer.')
    async def timer(self, ctx, minutes: int):
        user_id = ctx.author.id

        if user_id in active_timers and not active_timers[user_id].done():
            await ctx.send(f"{ctx.author.mention}, you already have a running timer. Stop it first with `stop`.")
            return

        await ctx.send(f"Timer set for {minutes} minutes!")
        active_timers[user_id] = asyncio.create_task(self.start_timer(ctx, minutes))

    async def start_timer(self, ctx, minutes):
        try:
            await asyncio.sleep(minutes * 60)
            await ctx.send(f"Time's up! Study session ended, {ctx.author.mention}")
        except asyncio.CancelledError:
            await ctx.send(f"Your timer was canceled, {ctx.author.mention}!")
            return
        finally:
            active_timers.pop(ctx.author.id, None)

    @commands.command(name='stop', aliases=['es', 'endsession', 'end'], help='Stops your current timer.')
    async def stop_timer(self, ctx):
        user_id = ctx.author.id

        if user_id in active_timers and not active_timers[user_id].done():
            active_timers[user_id].cancel()
            active_timers.pop(user_id, None)
            await ctx.send(f"Your timer has been stopped, {ctx.author.mention}.")
        else:
            await ctx.send(f"{ctx.author.mention}, you don't have an active timer.")
    
    @commands.command(name='remindmein', aliases=['remind', 'reminder'], help='Reminds you about a task in a given time [minutes]')
    async def remindmein(self, ctx, minutes: int, *, task):
        if minutes <= 0:
            await ctx.send("Please specify a time greater than 0 minutes!")
            return
        
        reminder_id = len(self.active_reminders) + 1
        self.active_reminders[reminder_id] = {
            'user_id': ctx.author.id,
            'task': task,
            'minutes': minutes,
            'ctx': ctx
        }

        await ctx.send(f"Reminder set! I'll remind you to '{task}' in {minutes} minutes.")

        await asyncio.sleep(minutes * 60)

        reminder = self.active_reminders.pop(reminder_id, None)
        if reminder:
            await reminder['ctx'].send(f"{ctx.author.mention}, time's up! Don't forget to {reminder['task']}.")

    @commands.command(name='cancelreminder', aliases=['cancel', 'stopreminder'], help='Cancels your active reminder')
    async def cancelreminder(self, ctx, reminder_id: int):
        if reminder_id not in self.active_reminders:
            await ctx.send(f"No active reminder found with ID {reminder_id}.")
        else:
            reminder = self.active_reminders.pop(reminder_id)
            await ctx.send(f"Your reminder for '{reminder['task']}' has been cancelled.")

    @commands.command(name='listreminders',aliases=['lr'], help='Lists all your active reminders')
    async def list_reminders(self, ctx):
        user_id = ctx.author.id
        user_reminders = [reminder for reminder in self.active_reminders.values() if reminder['user_id'] == user_id]

        if not user_reminders:
            await ctx.send(f"{ctx.author.mention}, you have no active reminders.")
        else:
            reminder_list = "\n".join([f"ID: {reminder_id} - Task: {reminder['task']} - In: {reminder['minutes']} minutes" for reminder_id, reminder in self.active_reminders.items() if reminder['user_id'] == user_id])
            await ctx.send(f"Your active reminders:\n{reminder_list}")

async def setup(bot):
    await bot.add_cog(Timer(bot))
