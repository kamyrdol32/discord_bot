import configparser
import discord

from discord.ext import commands

from db import metadata, engine

config = configparser.ConfigParser()
config.read('settings.ini')

addons = [
    "cog_ext",
    "report_message",
    "report_user",
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
        self.tree.copy_global_to(guild=discord.Object(id=int(config['APP']['MY_GUILD'])))
        await self.tree.sync(guild=discord.Object(id=int(config['APP']['MY_GUILD'])))
        metadata.create_all(engine)


EvGamingBOT().run(config['APP']['TOKEN'])