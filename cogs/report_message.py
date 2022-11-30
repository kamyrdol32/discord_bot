import datetime

import discord
from discord import app_commands
from discord.ext import commands

admin_channel_id = 951174054931480656

class ReportMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        print(f"{self.__class__.__name__} loaded!")

    async def cog_unload(self):
        print(f"{self.__class__.__name__} unloaded!")


@app_commands.context_menu(name='Zgłoś wiadomość')
async def report_message(interaction: discord.Interaction, message: discord.Message):

    # Check the message
    if message.author == interaction.user:
        await interaction.response.send_message('Nie możesz zgłosić swojej wiadomości!', ephemeral=True)
        return

    # Send message
    await interaction.response.send_message(
        f'Zgłoszono wiadomość od {message.author.mention}! Dziękujemy za pomoc!',
    )

    # Admin channel
    log_channel = interaction.guild.get_channel(admin_channel_id)

    # Embed
    embed = discord.Embed(title='Zgłoszono wiadomość', color=discord.Color.red())
    if message.content:
        embed.description = message.content

    embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar.url)
    embed.timestamp = message.created_at

    url_view = discord.ui.View()
    url_view.add_item(discord.ui.Button(label='Pokaż wiadomość', style=discord.ButtonStyle.url, url=message.jump_url))

    await log_channel.send(embed=embed, view=url_view)

async def setup(bot):
    await bot.add_cog(ReportMessage(bot=bot))
    bot.tree.add_command(report_message)