import discord
from discord.ext import commands
from sqlalchemy import create_engine
import asyncio
import logging
import settings
from MinecraftServerCog import MinecraftServerCog
from MinecraftCog import MinecraftCog
from CurrencyCog import CurrencyCog


class MinecraftServerDiscordBot(commands.Bot):
    def __init__(self, minecraft_server_remote, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.minecraft_server_remote = minecraft_server_remote
        self.db_engine = create_engine('sqlite:///' + settings.DB_PATH)

        self.add_cog(MinecraftServerCog(self, self.minecraft_server_remote))
        self.add_cog(MinecraftCog(self, self.db_engine))
        self.add_cog(CurrencyCog(self, self.db_engine))


    async def on_ready(self):
        '''Print bot user information when ready'''
        print('Logged in as {}'.format(self.user))
