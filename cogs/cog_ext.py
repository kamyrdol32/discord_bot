from discord import app_commands
from discord.ext import commands


# all cogs inherit from this base class
class ExampleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping")
    async def slash_pingcmd(self, interaction):
        """the second best command in existence"""
        await interaction.response.send_message(interaction.user.mention)

    async def cog_load(self):
        print(f"{self.__class__.__name__} loaded!")

    async def cog_unload(self):
        print(f"{self.__class__.__name__} unloaded!")


async def setup(bot):
    await bot.add_cog(ExampleCog(bot=bot))