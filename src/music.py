import nextcord
import wavelink
from nextcord.ext import commands

class Music(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
      self.bot.loop.create_task(self.node_connect())

  async def node_connect(self):
      await self.bot.wait_until_ready()
      await wavelink.NodePool.create_node(bot=self.bot, host='narco.buses.rocks', port='2269', password='glasshost1984')

  @commands.Cog.listener()
  async def on_wavelink_node_ready(self, node: wavelink.Node):
      print(f'Node {node.identifier} is ready!')
      
  @commands.command()
  async def play(self, ctx: commands.Context, *, search: wavelink.YouTubeTrack):
      if not ctx.voice_client:
          vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
      else:
          vc: wavelink.Player = ctx.voice_client
          
      await vc.play(search)


  def setup(bot):
    bot.add_cog(Music(bot))