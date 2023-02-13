import wavelink
from wavelink import *
from nextcord.ext import commands

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
  @commands.command()
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
          await ctx.send(f'🚌 Queued ***{search}***.')
          return self.queue.put(search)
      
      self.queue.put(search)
      track = await vc.play(self.queue[0])
      await ctx.send(f'▶ Playing ***{track}***.')

  @commands.Cog.listener()
  async def on_wavelink_track_end(self, player: player, track: Track, reason):
      print('Terminó la canción.')
      self.queue.get()
      if self.queue.is_empty:
          return await self.context.send(f'⛔ No more songs to play...')
      if not self.queue.is_empty:
        track = await self.player.play(self.queue[0])
        await self.context.send(f'▶ Playing ***{track}***.')
        
  @commands.command()
  async def skip(self, ctx):
      print('Canción skippeada.')
      print(self.queue)
      await self.player.stop()
      if not self.queue.is_empty:
          await self.context.send(f'⏩ Skipped current song.')
          
      
  def setup(bot):
    bot.add_cog(Music(bot))