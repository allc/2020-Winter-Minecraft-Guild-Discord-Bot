from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from datetime import datetime
import settings


Base = declarative_base()


def u():
    print('update')
    return datetime.now()


class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    uuid = Column(String, unique=True)
    playername = Column(String)
    skin_url = Column(String)
    is_skin_slim = Column(Boolean)
    skin_render = Column(String)
    last_update = Column(DateTime, default=datetime.now, onupdate=u)


    def __repr__(self):
        return f'<Player(name={self.player_name})>'


if __name__ == '__main__':
    db_engine = create_engine('sqlite:///' + settings.DB_PATH)
    Base.metadata.create_all(db_engine)
