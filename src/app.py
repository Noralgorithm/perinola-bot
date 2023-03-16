from bot import bot
from cogs import music
from cogs import speaking
from config import BOT_TOKEN

speaking.Speaking.setup(bot)
music.Music.setup(bot)

bot.run(BOT_TOKEN)