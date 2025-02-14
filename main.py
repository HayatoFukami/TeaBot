import os
import logging
import logging.handlers
import discord
from discord.ext import commands as cmds
from dotenv import load_dotenv
from settings import TREE_SYNC, COGS


class TeaBot(cmds.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.all())

    async def setup_hook(self) -> None:
        if COGS:
            for cog in COGS:
                await self.load_extension(cog)
                print(f"Loaded {cog}")
        if TREE_SYNC:
            await self.tree.sync()
            print("Synced application commands")

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
logging.getLogger("discord.http").setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler(
    filename='discord.log',
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024,
    backupCount=5
)
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<7}] {name}: {message}', dt_fmt, style='{')
handler.setFormatter(formatter)
logger.addHandler(handler)

if __name__ == '__main__':
    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    load_dotenv()
    token = os.getenv("TOKEN")
    bot = TeaBot()
    bot.run(token, log_handler=None)