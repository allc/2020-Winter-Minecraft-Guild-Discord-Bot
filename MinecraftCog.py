import discord
from discord.ext import commands
from utils.mojang import get_uuid, get_skin_url
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
import requests
from PIL import Image, ImageDraw
from io import BytesIO
from datetime import datetime, timedelta
from models import Player


class MinecraftCog(commands.Cog, name='Minecraft'):
    def __init__(self, bot, db_engine):
        self.bot = bot
        self.db_engine = db_engine


    @commands.command(brief='Shows player\'s Minecraft profile', usage='[playername]')
    async def player(self, ctx, playername):
        '''Shows player's Minecraft profile including playername, skin file URL and skin render.
        Gets data from database cache if available and not expired, otherwise gets data from Mojang API and update cache

        '''
        Session = sessionmaker(bind=self.db_engine)
        session = Session()
        is_refresh_required = True
        try:
            player = session.query(Player).filter(Player.playername==playername).one()
            if player.last_update + timedelta(minutes=10) > datetime.utcnow():
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
                r = requests.get(skin_url)
                skin_file = Image.open(BytesIO(r.content))
                skin_render = Image.new('RGBA', (16, 32))
                skin_render.paste(skin_file.crop((8, 8, 16, 16)), (4, 0)) # head
                skin_render.paste(skin_file.crop((20, 20, 28, 32)), (4, 8)) # body
                skin_render.paste(skin_file.crop((36, 52, 40, 64)), (12, 8)) # left arm
                skin_render.paste(skin_file.crop((44, 20, 48, 32)), (0, 8)) # right arm
                skin_render.paste(skin_file.crop((20, 52, 24, 64)), (8, 20)) # left leg
                skin_render.paste(skin_file.crop((4, 20, 8, 32)), (4, 20)) # right leg
                skin_render = skin_render.resize((64, 128), Image.NEAREST)
                skin_render_filename = uuid + '.png'
                skin_render.save(f'./skin_renders/{skin_render_filename}')
                player.skin_render = skin_render_filename
                player.skin_url = skin_url
                player.is_skin_slim = is_skin_slim
                player.last_update = datetime.utcnow()
                session.add(player)
                session.commit()
            skin_render = discord.File(f'./skin_renders/{player.skin_render}')
            embed = discord.Embed(title=playername)
            embed.add_field(name='Skin file URL', value=skin_url)
            embed.set_image(url=f'attachment://{player.skin_render}')
            await ctx.send(embed=embed, file=skin_render)
        except Exception as e:
            await ctx.send(e)
