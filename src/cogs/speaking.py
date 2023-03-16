import nextcord
from nextcord.ext import commands


class Speaking(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["alias1", "alias2"])
    async def command_name(self, ctx):
        await ctx.send("aaa")

    @commands.command(aliases=["repeat"])
    async def command_example(self, ctx, *args):
        await ctx.send("Dijiste " + " ".join(args) + "? 😎")

    def setup(client):
        client.add_cog(Speaking(client))
