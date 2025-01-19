import nextcord
# skipcq: PY-W2000
from nextcord.ext import commands#, tasks
from utils import links
import yt_dlp as youtube_dl
import asyncio

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

class Music(commands.Cog):
    """A command for playing music from youtube and youtube music"""

    def __init__(self, bot):
        self.bot = bot
        # self.check_vc_empty.start()
        self.song_queue = {}
        self.current_song = {}

    @commands.command(aliases=['p'])
    async def play(self, ctx, *, query=None):
        """Plays music of the given song name/link of a song/ a playlist link [only yt/ytm]"""
        
        if not query:
            await ctx.send("Please provide a song name/link of a song/ a playlist link [only yt/ytm]")
            return

        if ctx.author.voice:
            if ctx.voice_client is None:
                vc = await ctx.author.voice.channel.connect()
                await ctx.guild.change_voice_state(channel=ctx.author.voice.channel, self_deaf=True)
            elif ctx.voice_client.channel != ctx.author.voice.channel:
                await ctx.voice_client.move_to(ctx.author.voice.channel)
                await ctx.guild.change_voice_state(channel=ctx.author.voice.channel, self_deaf=True)
            else:
                vc = ctx.voice_client
                await ctx.guild.change_voice_state(channel=ctx.author.voice.channel, self_deaf=True)
        else:
            await ctx.send("You must be in a voice channel to use this command!")
            return

        if "youtube.com/playlist" in query or "music.youtube.com/playlist" in query or "list=" in query:
            ytdl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': 'downloads/%(title)s.%(ext)s',
                'restrictfilenames': True,
                'noplaylist': False,
                'quiet': True,
                'no_warnings': True,
                'default_search': 'auto',
            }

            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: self.fetch_info(ytdl_opts, query))

            if data is None or len(data) == 0:
                await ctx.send("No audio found for the given query")
                return

            for song in data:
                self.song_queue.setdefault(ctx.guild.id, []).append(song)

            if not vc.is_playing():
                await self.play_next_song(ctx)
        elif "youtube.com" in query or "music.youtube.com" in query:
            ytdl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': 'downloads/%(title)s.%(ext)s',
                'restrictfilenames': True,
                'noplaylist': True,
                'quiet': True,
                'no_warnings': True,
                'default_search': 'auto',
            }

            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: self.fetch_info(ytdl_opts, query))

            if data is None or len(data) == 0:
                await ctx.send("No audio found for the given query")
                return

            self.song_queue.setdefault(ctx.guild.id, []).append(data[0])

            if not vc.is_playing():
                await self.play_next_song(ctx)
        else:
            ytdl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': 'downloads/%(id)s.%(ext)s',
                'restrictfilenames': True,
                'noplaylist': True,
                'quiet': True,
                'no_warnings': True,
                'default_search': 'ytsearch5',
            }

            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: self.fetch_info(ytdl_opts, query))

            if data is None or len(data) == 0:
                await ctx.send("No audio found for the given query")
                return

            # Display the top 5 search results and prompt the user to select one
            search_results = data
            description = "\n".join([f"{i+1}. {result['title']}" for i, result in enumerate(search_results)])
            embed = nextcord.Embed(
                title="Search Results",
                description=description,
                color=nextcord.Colour.red()
            )
            embed.set_author(name="Frisk", url=None, icon_url=links.authorPFP)
            embed.set_footer(text="Type the number of the song you want to play. With some determination")
            await ctx.send(embed=embed)

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit() and 1 <= int(m.content) <= 5

            try:
                msg = await self.bot.wait_for('message', check=check, timeout=30.0)
            except asyncio.TimeoutError:
                await ctx.send("You took too long to respond.")
                return

            index = int(msg.content) - 1
            selected_result = search_results[index]
            self.song_queue.setdefault(ctx.guild.id, []).append(selected_result)

            if not vc.is_playing():
                await self.play_next_song(ctx)

    async def play_next_song(self, ctx):
        while ctx.guild.id in self.song_queue and len(self.song_queue[ctx.guild.id]) > 0:
            song = self.song_queue[ctx.guild.id].pop(0)
            self.current_song[ctx.guild.id] = song
            audio_url = song['url']
            title = song['title']
            thumbnail_url = song.get('thumbnail')

            vc = ctx.voice_client

            # Debugging: Print the audio URL to ensure it's correct
            print(f"Playing audio from URL: {audio_url}")

            try:
                vc.play(nextcord.FFmpegPCMAudio(audio_url, **ffmpeg_options), after=lambda e: self.bot.loop.create_task(self.play_next_song(ctx)))
                break  # Exit the loop if the song is successfully played
            except Exception as e:
                await ctx.send(f"Error playing audio: {e}")
                print(f"Error playing audio: {e}")
                continue  # Skip to the next song if there's an error

            embed = nextcord.Embed(
                title="Now Playing", 
                description="Not your avg song...", color=nextcord.Colour.red()
            )
            embed.set_author(name="Frisk", url=None, icon_url=links.authorPFP)
            embed.add_field(name=f"{title}", value="type `stop` to stop playing\ntype `pause` to pause playing\n`next` to play next song\n`prev` to play previous song", inline=True)
            if thumbnail_url:
                embed.set_image(url=f"{thumbnail_url}")
            embed.set_footer(text="The beats in these songs sync with your heart, filling you with determination..❤️")
            await ctx.send(embed=embed)

    async def play_previous_song(self, ctx):
        if ctx.guild.id in self.current_song and self.current_song[ctx.guild.id]:
            song = self.current_song[ctx.guild.id]
            self.song_queue.setdefault(ctx.guild.id, []).insert(0, song)
            await self.play_next_song(ctx)

    def fetch_info(self, ytdl_opts, query):
        try:
            with youtube_dl.YoutubeDL(ytdl_opts) as ydl:
                info = ydl.extract_info(query, download=False)
                if 'entries' in info:
                    entries = info['entries']  # Get all entries for playlists
                    valid_entries = []
                    for entry in entries:
                        if not entry.get('url'):
                            print(f"Skipping unavailable video: {entry.get('title', 'Unknown')}")
                            continue
                        valid_entries.append(entry)
                    return valid_entries
                else:
                    return [info]

        except Exception as e:
            print(f"Error occurred: {e}")
            return None

    @commands.command()
    async def stop(self, ctx):
        """Stops the music"""
        if ctx.voice_client:
            self.song_queue.pop(ctx.guild.id, None)  # Clear the song queue
            await ctx.voice_client.disconnect()
        else:
            await ctx.send("I am not in a voice channel.")

    @commands.command()
    async def pause(self, ctx):
        """Pauses the music"""
        if ctx.voice_client:
            ctx.voice_client.pause()
        else:
            await ctx.send("I am not in a voice channel.")
    
    @commands.command()
    async def resume(self, ctx):
        """Resumes the paused music"""
        if ctx.voice_client:
            ctx.voice_client.resume()
        else:
            await ctx.send("I am not in a voice channel.")

    @commands.command()
    async def next(self, ctx):
        """Skips to the next song"""
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await self.play_next_song(ctx)
        else:
            await ctx.send("No song is currently playing.")

    @commands.command()
    async def prev(self, ctx):
        """Plays the previous song"""
        if ctx.voice_client:
            await self.play_previous_song(ctx)
        else:
            await ctx.send("No song is currently playing.")

    @commands.command()
    async def queue(self, ctx):
        """Displays the current song queue"""
        if ctx.guild.id in self.song_queue and len(self.song_queue[ctx.guild.id]) > 0:
            queue = self.song_queue[ctx.guild.id]
            description = "\n".join([f"{i+1}. {song['title']}" for i, song in enumerate(queue)])
            embed = nextcord.Embed(
                title="Current Queue",
                description=description,
                color=nextcord.Colour.red()
            )
            embed.set_author(name="Frisk", url=None, icon_url=links.authorPFP)
            embed.set_footer(text="Looking at this endless void of queue, filling you with endless determination..❤️")
            await ctx.send(embed=embed)
        else:
            await ctx.send("The queue is currently empty.")

def setup(bot):
    bot.add_cog(Music(bot))