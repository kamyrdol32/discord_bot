import os
import configparser
from discord.ext import commands

config = configparser.ConfigParser()
config.read('settings.ini')

bot = commands.Bot(command_prefix="!")

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(config['APP']['TOKEN'])