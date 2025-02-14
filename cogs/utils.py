import discord as d
from discord.ext import commands as cmds


class Utils(cmds.Cog):
    def __init__(self, bot):
        self.bot = bot

    @d.app_commands.command(name="ping", description="Pong!")
    async def ping(self, interaction: d.Interaction):
        await interaction.response.send_message(f"Pong! {round(self.bot.latency * 1000)}ms")


async def setup(bot: cmds.Bot):
    await bot.add_cog(Utils(bot))
