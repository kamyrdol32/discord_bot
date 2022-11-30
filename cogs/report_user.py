import datetime

import discord
from discord import app_commands
from discord.ext import commands

class ReportUser(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        print(f"{self.__class__.__name__} loaded!")

    async def cog_unload(self):
        print(f"{self.__class__.__name__} unloaded!")


@app_commands.context_menu(name='Zgłoś użytkownika')
async def report_user(interaction: discord.Interaction, user: discord.User):
    await interaction.response.send_message(
        f'Zgłoszono użytkownika {user.mention}! Dziękujemy za pomoc!',
    )




async def setup(bot):
    await bot.add_cog(ReportUser(bot=bot))
    bot.tree.add_command(report_user)