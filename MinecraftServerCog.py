import discord
from discord.ext import commands, tasks
import logging
import settings
from utils.discord_bot import send_to_channels
class MinecraftServerCog(commands.Cog, name='Minecraft Server'):
    def __init__(self, bot, minecraft_server_remote):
        self.bot = bot
        self.minecraft_server_remote = minecraft_server_remote

        self.last_activity = None
        self.minecraft_server_offline = False

        self.update_activity.start()


    def cog_unload(self):
        '''Cancel tasks when unload Cog'''
        self.update_activity.cancel()


    @tasks.loop(minutes=1)
    async def update_activity(self):
        '''Update bot activity with number of current online players every minute
        If the Minecraft server became offline or back online again, sends an alert to configured channels

        '''
        try:
            num_online_players = self.minecraft_server_remote.get_online_players_count()
        except ConnectionError:
            if not self.minecraft_server_offline:
                self.minecraft_server_offline = True
                message = 'Minecraft server appears to be offline.'
                print(message)
                logging.warning(message)
                await send_to_channels(self.bot, settings.MINECRAFT_SERVER_OFFLINE_ALERT_CHANNEL_IDS, message)
            return
        if self.minecraft_server_offline:
            self.minecraft_server_offline = False
            log_message = 'Minecraft server is online.'
            print(log_message)
            logging.info(log_message)
            await send_to_channels(self.bot, settings.MINECRAFT_SERVER_OFFLINE_ALERT_CHANNEL_IDS, 'Minecraft server is back online :ok_hand:')
        if num_online_players == 0:
            activity_content = 'with no one'
        else:
            activity_content = f'with {num_online_players} online player' + ('s' if num_online_players > 1 else '')
        if activity_content != self.last_activity:
            await self.bot.change_presence(activity=discord.Game(name=activity_content))
            self.last_activity = activity_content
            logging.info(f'Updated activity to "{activity_content}".')


    @update_activity.before_loop
    async def before_update_activity(self):
        '''Wait until bot is ready to start updating activity'''
        await self.bot.wait_until_ready()


    @commands.command(aliases=['m'], help='Shows the list of current online players on the Minecraft server')
    async def online(self, ctx):
        online_players = self.minecraft_server_remote.get_online_players()
        if len(online_players) == 0:
            response = 'No online players.'
        else:
            response = 'Online player' + ('s' if len(online_players) > 1 else '') + ':\n- ' + '\n- '.join(online_players)
        await ctx.send(response)
