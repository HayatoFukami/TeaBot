import os
import logging
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


if __name__ == '__main__':
    load_dotenv()
    token = os.getenv("TOKEN")
    bot = TeaBot()
    bot.run(token)