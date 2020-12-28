import discord
from discord.ext import commands
import asyncio
import logging
from MinecraftServerCog import MinecraftServerCog


class MinecraftServerDiscordBot(commands.Bot):
    def __init__(self, minecraft_server_remote, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.minecraft_server_remote = minecraft_server_remote

        self.last_activity = None

        self.add_cog(MinecraftServerCog(self, self.minecraft_server_remote))

        self.update_activity_task = self.loop.create_task(self.update_activity())

    
    async def update_activity(self):
        await self.wait_until_ready()
        while not self.is_closed():
            num_online_players = self.minecraft_server_remote.get_online_players_count()
            if num_online_players == 0:
                activity_content = 'with no one'
            else:
                activity_content = f'with {num_online_players} online player' + ('s' if num_online_players > 1 else '')
            if activity_content != self.last_activity:
                await self.change_presence(activity=discord.Game(name=activity_content))
                self.last_activity = activity_content
                logging.info(f'Updated activity to "{activity_content}".')
            await asyncio.sleep(60)
