import discord
from discord import app_commands
from discord.ext import commands


# all cogs inherit from this base class
class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="clear")
    async def clear(self, interaction: discord.Interaction, amount: int):
        channel = interaction.channel

        await channel.purge(limit=amount)
        await channel.send(f'Usunięto {amount} wiadomości!', delete_after=5)


    async def cog_load(self):
        print(f"{self.__class__.__name__} loaded!")

    async def cog_unload(self):
        print(f"{self.__class__.__name__} unloaded!")


async def setup(bot):
    await bot.add_cog(Clear(bot=bot))