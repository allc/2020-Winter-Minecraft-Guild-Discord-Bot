from discord.ext import commands
from utils.mojang import get_skin_url_from_playername


class MinecraftCog(commands.Cog, name='Minecraft'):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(help='')
    async def player(self, ctx, playername):
        try:
            skin_url, _ = get_skin_url_from_playername(playername)
            await ctx.send(playername + '\n' + skin_url)
        except Exception as e:
            await ctx.send(e)
