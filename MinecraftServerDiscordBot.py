import discord
from discord.ext import commands
import asyncio
import logging
from MinecraftServerCog import MinecraftServerCog


class MinecraftServerDiscordBot(commands.Bot):
    def __init__(self, minecraft_server_remote, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.minecraft_server_remote = minecraft_server_remote

        self.add_cog(MinecraftServerCog(self, self.minecraft_server_remote))


    async def on_ready(self):
        '''Print bot user information when ready'''
        print('Logged in as {}'.format(self.user))
