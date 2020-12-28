import discord
from discord.ext import commands

class MinecraftServerCog(commands.Cog, name='Minecraft Server'):
    def __init__(self, bot, minecraft_server_remote):
        self.bot = bot
        self.minecraft_server_remote = minecraft_server_remote


    @commands.Cog.listener()
    async def on_ready(self):
        print('Logged in as {}'.format(self.bot.user))


    @commands.command(aliases=['m'], help='Shows the list of players who are currently online on the Minecraft server.')
    async def online(self, ctx):
        online_players = self.minecraft_server_remote.get_online_players()
        if len(online_players) == 0:
            response = 'No online players.'
        else:
            response = 'Online player' + ('s' if len(online_players) > 1 else '') + ':\n- ' + '\n- '.join(online_players)
        await ctx.send(response)
