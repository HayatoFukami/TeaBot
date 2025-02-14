import os
import discord
from discord.ext import commands as cmds
from dotenv import load_dotenv


class TeaBot(cmds.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.default())

    async def setup_hook(self) -> None:
        return

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")


if __name__ == '__main__':
    load_dotenv()
    token = os.getenv("TOKEN")
    bot = TeaBot()
    bot.run(token)