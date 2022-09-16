

from main import commands

class Scrapper(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(Scrapper(bot))