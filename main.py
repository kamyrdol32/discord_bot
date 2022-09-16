import os
import configparser
from discord.ext import commands, tasks

config = configparser.ConfigParser()
config.read('settings.ini')

bot = commands.Bot(command_prefix="!")


for filename in os.listdir('extensions'):
    if filename.endswith('.py'):
        bot.load_extension(f'extensions.{filename[:-3]}')
        print(f'Loaded extension: {filename[:-3]}')


bot.run(config['APP']['TOKEN'])