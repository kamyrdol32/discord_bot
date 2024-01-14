import asyncio

import discord
from discord import app_commands
from discord.ext import commands


# all cogs inherit from this base class
class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(name="clear")
    async def clear(self, interaction: discord.Interaction, amount: int):
        await interaction.response.defer(ephemeral=True)

        channel = interaction.channel

        # Pętla usunięcia z opóźnieniem
        async for message in channel.history(limit=amount):
            await asyncio.sleep(0.75)
            await message.delete()

        await interaction.followup.send(f'Usunięto {amount} wiadomości!')


    async def cog_load(self):
        print(f"{self.__class__.__name__} loaded!")

    async def cog_unload(self):
        print(f"{self.__class__.__name__} unloaded!")


async def setup(bot):
    await bot.add_cog(Clear(bot=bot))
