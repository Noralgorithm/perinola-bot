import nextcord
from nextcord.ext import commands

intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='r!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')