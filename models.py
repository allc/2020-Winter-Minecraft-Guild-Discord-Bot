from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from datetime import datetime
import settings


Base = declarative_base()


class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    uuid = Column(String, unique=True)
    playername = Column(String)
    skin_url = Column(String)
    is_skin_slim = Column(Boolean)
    skin_render = Column(String)
    last_update = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    def __repr__(self):
        return f'<Player(name={self.player_name})>'


class CurrencyPlayer(Base):
    __tablename__ = 'currency_player'

    id = Column(Integer, primary_key=True)
    discord_user_id = Column(Integer, unique=True)
    balance = Column(Integer, default=0)
    last_timely = Column(DateTime, default=datetime.fromtimestamp(0))


if __name__ == '__main__':
    db_engine = create_engine('sqlite:///' + settings.DB_PATH)
    Base.metadata.create_all(db_engine)
