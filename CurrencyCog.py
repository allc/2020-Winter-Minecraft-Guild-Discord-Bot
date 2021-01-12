from discord.ext import commands
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from models import CurrencyPlayer


class CurrencyCog(commands.Cog, name='Minecraft'):
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
        await ctx.send(f'**{username}#{discriminator}** has has {balance_amount_str} :moneybag:')
