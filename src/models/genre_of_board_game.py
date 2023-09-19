from sqlalchemy import Column, BigInteger, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base
from src.models.boardgame import BoardGame
from src.models.genre import Genre


class GenreOfBoardGame(Base):
    __tablename__ = 'genre_of_board_game'

    genre_of_board_game_id = Column(BigInteger, primary_key=True, index=True)
    board_game_id = Column(BigInteger, ForeignKey('board_game.board_game_id'))
    genre_id = Column(BigInteger, ForeignKey('genre.genre_id'))

    board_game = relationship('BoardGame', back_populates='genres')
    genre = relationship('Genre', back_populates='board_games')
