from sqlalchemy import Column, String, BigInteger
from sqlalchemy.orm import relationship

from src.database import Base


class Genre(Base):
    __tablename__ = 'genre'

    genre_id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String)

    board_games = relationship('GenreOfBoardGame', back_populates='genre')
