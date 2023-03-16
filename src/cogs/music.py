import wavelink
from wavelink import *
from nextcord.ext import commands
from utils import duration_formatter


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue: wavelink.Queue = wavelink.Queue()
        self.player: wavelink.Player
        self.context: wavelink.Context

    ### Connection ###
    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.loop.create_task(self.node_connect())

    async def node_connect(self):
        await self.bot.wait_until_ready()
        await wavelink.NodePool.create_node(bot=self.bot, host='narco.buses.rocks', port='2269', password='glasshost1984')

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f'Node {node.identifier} is ready!')

    ### Music ###
    @commands.command(aliases=['p'])
    async def play(self, ctx: commands.Context, *, search: wavelink.YouTubeTrack):
        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
            self.player = vc
            self.context = ctx
        else:
            vc: wavelink.Player = ctx.voice_client
            self.player = vc
            self.context = ctx

        if not self.queue.is_empty:
            await ctx.send(f'🚌 Queued ***{search}***. *({duration_formatter.duration_formatter(search.duration)})*')
            return self.queue.put(search)

        self.queue.put(search)
        track = await vc.play(self.queue[0])
        await ctx.send(f'▶ Playing ***{track}***. *({duration_formatter.duration_formatter(search.duration)})*')

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, player: player, track: Track, reason):
        print('Terminó la canción.')
        self.queue.get()
        if self.queue.is_empty:
            return await self.context.send(f'⛔ No more songs to play...')
        if not self.queue.is_empty:
            track = await self.player.play(self.queue[0])
            await self.context.send(f'▶ Playing ***{track}***. *({duration_formatter.duration_formatter(track.duration)})*')

    @commands.command(aliases=['s'])
    async def skip(self, ctx):
        print('Canción skippeada.')
        print(self.queue)
        await self.player.stop()
        if not self.queue.is_empty:
            await self.context.send(f'⏩ Skipped current song.')

    @commands.command(aliases=['q', 'list', 'songs'])
    async def queue(self, ctx):
        if self.queue.count <= 1:
            return await self.context.send('*Empty queue...*')
        formatted_track_list = ''
        print(str(self.queue[0].title))
        for i in range(self.queue.count - 1):
            formatted_track_list = ''.join(
                [formatted_track_list, f'***{i + 1}—*** ', f'***{self.queue[i + 1].title}.*** ', f'({duration_formatter.duration_formatter(self.queue[i + 1].duration)})', '\n'])
        await self.context.send(formatted_track_list)

    @commands.command(aliases=['rm'])
    async def remove(self, ctx, *args):
        try:
            index = int(args[0])
            if index < 0 or index >= self.queue.count:
                raise ValueError('Índice inválido...')
            del self.queue._queue[index]
        except (ValueError):
            await self.context.send('Índice inválido...')

    @commands.command(aliases=['cls'])
    async def clear(self, ctx):
        self.queue.clear()
        await self.context.send('*Cleared queue...*')

    @commands.command(aliases=['pn'])
    async def next(self, ctx, *args):
        try:
            index = int(args[0])
            if index < 0 or index >= self.queue.count:
                raise ValueError('Índice inválido...')
            song = self.queue[index]
            self.queue.put_at_index(1, song)
            await self.context.send('Deleted selected song...')
            await self.context.invoke(self.queue)
            del self.queue._queue[index + 1]
        except (ValueError):
            await self.context.send('Índice inválido...')

    def setup(bot):
        bot.add_cog(Music(bot))
