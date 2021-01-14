import discord
from discord.ext import commands
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from models import CurrencyPlayer
from datetime import datetime, timedelta


class CurrencyCog(commands.Cog, name='Currency'):
    def __init__(self, bot, db_engine):
        self.bot = bot
        self.db_engine = db_engine


    @commands.command(aliases=['$'], brief='Shows balance')
    async def balance(self, ctx):
        try:
            Session = sessionmaker(bind=self.db_engine)
            session = Session()
            currency_player = session.query(CurrencyPlayer).filter(CurrencyPlayer.discord_user_id==ctx.author.id).one()
            balance_amount = currency_player.balance
        except NoResultFound:
            balance_amount = 0
        balance_amount_str = f'{balance_amount:,}'.replace(',', ' ')
        username = ctx.author.name
        discriminator = ctx.author.discriminator
        embed = discord.Embed(description=f'**{username}#{discriminator}** has {balance_amount_str} :moneybag:', colour=discord.Colour.green())
        await ctx.send(embed=embed)


    @commands.command(brief='Claim some reward every 12h')
    async def timely(self, ctx):
        '''Claim reward if at least the required amount of time has passed since last time the reward has been claimed.
        Add currency player record if no record found

        '''
        # Get currency player
        additional_message = False
        try:
            Session = sessionmaker(bind=self.db_engine)
            session = Session()
            currency_player = session.query(CurrencyPlayer).filter(CurrencyPlayer.discord_user_id==ctx.author.id).one()
        except NoResultFound:
            currency_player = CurrencyPlayer(discord_user_id=ctx.author.id, balance=0, last_timely=datetime.fromtimestamp(0))
            additional_message = '\nAre timelys even real :thonk:'
        username = ctx.author.name
        discriminator = ctx.author.discriminator
        # Check if the required amount of time passed
        current_time = datetime.utcnow()
        if current_time - currency_player.last_timely < timedelta(hours=12):
            time_left = timedelta(hours=12) - (current_time - currency_player.last_timely)
            embed = discord.Embed(description=f'**{username}#{discriminator}** You\'ve already claimed your timely reward. You can get it again in {time_left.days}d {time_left.seconds // 3600}h {time_left.seconds // 60 % 60}m {time_left.seconds % 60}s.', colour=discord.Colour.red())
        else:
            currency_player.balance += 200
            currency_player.last_timely = current_time
            session.add(currency_player)
            session.commit()
            embed = discord.Embed(description=f'**{username}#{discriminator}** You\'ve claimed your 200:moneybag:. You can claim again in 12h', colour=discord.Colour.green())
            if additional_message:
                embed.set_footer(text=additional_message)
        await ctx.send(embed=embed)
