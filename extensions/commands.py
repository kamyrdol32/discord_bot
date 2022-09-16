import asyncio
import time
import discord

from main import commands, tasks

from discord import Member
from discord.ext.commands import Context


class Commands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    ########################################
    ### COMMANDS
    ########################################
    
    @commands.command(name="commands")
    @commands.cooldown(rate=1, per=30)
    async def help(self, ctx: commands.Context):

        embed = discord.Embed(title="Commands", colour=0xECB72D)
        embed.set_author(name="🏆 EvBOT 🏆", icon_url=str(self.bot.user.avatar_url))
        embed.add_field(name="🌟 ┃ kick <nick>", value="Wyrzucenie użytkownika", inline=False)
        embed.add_field(name="🌟 ┃ ban <nick>", value="Banowanie użytkownika", inline=False)
        embed.add_field(name="🌟 ┃ clean <ilość>", value="Czyszczenie kanału", inline=False)
        embed.add_field(name="🌟 ┃ setstatus", value="Zmiana statusu bot'a", inline=False)
        embed.add_field(name="🌟 ┃ ping", value="Sprawdzanie opóźnienia", inline=False)
        embed.set_footer(text="Pomogłem? ✅ ❌")

        message = await ctx.send(embed=embed, delete_after=300)
        await message.add_reaction("✅")
        await message.add_reaction("❌")

        check = lambda r, u: u == ctx.author and str(r.emoji) in "✅❌"  # r=reaction, u=user

        try:
            reaction, user = await self.bot.wait_for("reaction_add", check=check, timeout=30)
        except asyncio.TimeoutError:
            return

        if str(reaction.emoji) == "✅":
            await ctx.message.delete()
            await message.delete()
            return


    ########################################
    #### CLEAN
    ########################################

    @commands.command(name="clean")
    async def clear(self, ctx: commands.Context, *, text: str):

        deleted = await ctx.channel.purge(limit=int(text) + 1)
        embed = discord.Embed(title="Czyszczenie kanału", description='Usunięto {} wiadomości'.format(len(deleted) - 1), colour=0xECB72D)
        embed.set_author(name="🏆 EvBOT 🏆", icon_url=str(self.bot.user.avatar_url))
        await ctx.send(embed=embed, delete_after=5)
        await ctx.message.delete(delay=10)


    ########################################
    #### PING
    ########################################

    @commands.command(name="ping")
    @commands.cooldown(rate=1, per=30)
    async def ping(self, ctx: commands.Context):
        start_time = time.time()
        message = await ctx.send("Testowanie...")
        end_time = time.time()

        embed = discord.Embed(title="Opóźnienia", colour=0xECB72D)
        embed.set_author(name="🏆 EvBOT 🏆", icon_url=str(self.bot.user.avatar_url))
        embed.add_field(name="Ping", value=str(round(self.bot.latency * 1000)), inline=True)
        embed.add_field(name="API", value=str(round((end_time - start_time) * 1000)), inline=True)

        await message.edit(content="", embed=embed, delete_after=10)
        await ctx.message.delete(delay=10)


    ########################################
    #### SETSTATUS
    ########################################

    @commands.command(name="setstatus")
    @commands.cooldown(rate=1, per=30)
    async def setstatus(self, ctx: commands.Context, *, text: str = "EvGaming"):
        await self.bot.change_presence(activity=discord.Game(name=text))
        await ctx.message.delete(delay=10)


    ########################################
    #### KICK
    ########################################

    @commands.command(name="kick")
    async def kick(self, ctx: Context, member: Member):

        message = await ctx.send(f"Jesteś pewny ze chcesz wyrzucić tego użytkownika? 👀```| {member}```")
        await message.add_reaction("✅")
        await message.add_reaction("❌")

        check = lambda r, u: u == ctx.author and str(r.emoji) in "✅❌"  # r=reaction, u=user

        try:
            reaction, user = await self.bot.wait_for("reaction_add", check=check, timeout=30)
        except asyncio.TimeoutError:
            await message.edit(content="Anulowano wyrzucenie, upłynał czas.")
            await message.delete()
            await ctx.message.delete()
            return

        if str(reaction.emoji) == "✅":
            await member.kick()
            await message.edit(content=f"{member} został wyrzucony.", delete_after=10)
            await ctx.message.delete(deley=10)
            return

        await message.edit(content="Anulowano wyrzucenie.", delete_after=10)
        await ctx.message.delete()


    ########################################
    #### BAN
    ########################################

    @commands.command(name="ban")
    async def ban(self, ctx: Context, member: Member):

        message = await ctx.send(f"Jesteś pewny ze chcesz zbanować tego użytkownika? 👀```| {member}```")
        await message.add_reaction("✅")
        await message.add_reaction("❌")

        check = lambda r, u: u == ctx.author and str(r.emoji) in "✅❌"  # r=reaction, u=user

        try:
            reaction, user = await self.bot.wait_for("reaction_add", check=check, timeout=30)
        except asyncio.TimeoutError:
            await message.edit(content="Anulowano banowanie, upłynał czas.")
            await message.delete()
            await ctx.message.delete()
            return

        if str(reaction.emoji) == "✅":
            await member.ban()
            await message.edit(content=f"{member} został zbanowany.", delete_after=10)
            await ctx.message.delete(deley=10)
            return

        await message.edit(content="Anulowano banowanie.", delete_after=10)
        await ctx.message.delete()


    ########################################
    #### WARN
    ########################################

    @commands.command(name="warn")
    async def warn(self, ctx: Context, member: Member, text: str):

        message = await ctx.send(f"Jesteś pewny ze chcesz ostrzec tego użytykownika? 👀```| {member}```")
        await message.add_reaction("✅")
        await message.add_reaction("❌")

        check = lambda r, u: u == ctx.author and str(r.emoji) in "✅❌"  # r=reaction, u=user

        try:
            reaction, user = await self.bot.wait_for("reaction_add", check=check, timeout=30)
        except asyncio.TimeoutError:
            await message.edit(content="Anulowano ostrzeżenie, upłynał czas.")
            await message.delete()
            await ctx.message.delete()
            return

        if str(reaction.emoji) == "✅":
            embed = discord.Embed(title="Ostrzeżenie", description=str(text), colour=0xECB72D)
            embed.set_author(name="🏆 EvBOT 🏆", icon_url=str(self.bot.user.avatar_url))

            await member.send(embed=embed)
            await message.edit(content=f"{member} został ostrzeżony.", delete_after=10)
            await ctx.message.delete(deley=10)
            return

        await message.edit(content="Anulowano ostrzeżenie.", delete_after=10)
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(Commands(bot))
