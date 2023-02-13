import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
TESTING_GUILD_ID = os.getenv('TESTING_GUILD_ID')