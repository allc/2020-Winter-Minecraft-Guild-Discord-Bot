from discord.ext import commands


class CurrencyCog(commands.Cog, name='Minecraft'):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases=['$'], brief='Shows balance')
    async def balance(self, ctx):
        username = ctx.author.name
        discriminator = ctx.author.discriminator
        await ctx.send(f'**{username}#{discriminator}** has has 0 :moneybag:')
