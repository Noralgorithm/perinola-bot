from bot import bot
from speaking import Speaking
from music import Music
from config import BOT_TOKEN

Speaking.setup(bot)
Music.setup(bot)

bot.run(BOT_TOKEN)