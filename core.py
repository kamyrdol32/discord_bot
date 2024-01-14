import configparser
import discord
import os

from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

addons = [
    "cog_ext",
    "report_message",
    "report_user",
    "clear"
]

class EvGamingBOT(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=discord.Intents.all()
        )

    async def setup_hook(self):

        # Load all cogs
        for file in addons:
            await self.load_extension("cogs." + file)

        # Load all slash commands
        self.tree.copy_global_to(guild=discord.Object(id=int(os.environ.get("DISCORD_GUILD_ID"))))
        await self.tree.sync(guild=discord.Object(id=int(os.environ.get("DISCORD_GUILD_ID"))))


EvGamingBOT().run(os.environ.get("DISCORD_TOKEN"))
