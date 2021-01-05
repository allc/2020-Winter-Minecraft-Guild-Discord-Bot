from discord.ext import commands
from utils.mojang import get_uuid, get_skin_url
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime, timedelta
import settings
from models import Player


class MinecraftCog(commands.Cog, name='Minecraft'):
    def __init__(self, bot):
        self.bot = bot

        self.db_engine = create_engine('sqlite:///' + settings.DB_PATH)


    @commands.command(brief='Shows player\'s Minecraft profile', usage='[playername]')
    async def player(self, ctx, playername):
        ''''''
        #TODO: Skin render
        Session = sessionmaker(bind=self.db_engine)
        session = Session()
        is_refresh_required = True
        try:
            player = session.query(Player).filter(Player.playername==playername).one()
            if player.last_update + timedelta(minutes=10) > datetime.now():
                is_refresh_required = False
                playername = player.playername
                skin_url = player.skin_url
        except NoResultFound:
            pass
        try:
            if is_refresh_required:
                uuid, playername = get_uuid(playername)
                try:
                    player = session.query(Player).filter(Player.uuid==uuid).one()
                    player.playername = playername
                except NoResultFound:
                    player = Player(uuid=uuid, playername=playername)
                skin_url, is_skin_slim = get_skin_url(uuid)
                player.skin_url = skin_url
                player.is_skin_slim = is_skin_slim
                #player.skin_render
                player.last_update = datetime.now()
                session.add(player)
                session.commit()
            await ctx.send(playername + '\n' + skin_url)
        except Exception as e:
            await ctx.send(e)
