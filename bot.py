from discord.ext import commands
from datetime import datetime
import logging
import settings
from MinecraftServerRemote import MinecraftServerRemote
from MinecraftServerDiscordBot import MinecraftServerDiscordBot
import utils.minecraft as minecraft_utils


'''Setup logging.'''
logging_filename = './logs/{}.log'.format(datetime.now().strftime('%Y-%m-%d'))
logging_format = '%(asctime)s:%(levelname)s:%(name)s: %(message)s'
logging_handler = logging.FileHandler(filename=logging_filename, encoding='utf-8', mode='a')
logging.basicConfig(format=logging_format, level=logging.INFO, handlers=[logging_handler])


logging.info('Logging started.')


minecraft_server_remote = MinecraftServerRemote(*minecraft_utils.get_minecraft_server_address_port(settings.MINECRAFT_SERVER_ADDRESS, settings.MINECRAFT_SERVER_PORT))


bot = MinecraftServerDiscordBot(minecraft_server_remote, command_prefix=settings.COMMAND_PREFIX)


bot.run(settings.DISCORD_BOT_TOKEN)
