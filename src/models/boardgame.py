from sqlalchemy import Column, Integer, String, Float, BigInteger

from src.database import Base


class BoardGame(Base):
    __tablename__ = 'board_game'

    board_game_id = Column(BigInteger, primary_key=True, index=True)
    description = Column(String)
    image_path = Column(String)
    is_localized = Column(String)
    name = Column(String)
    play_time = Column(Integer)
    player_max = Column(Integer)
    player_min = Column(Integer)
    weight = Column(Float)
    bgg_id_index = Column(Integer)
    weight_index = Column(Integer)
