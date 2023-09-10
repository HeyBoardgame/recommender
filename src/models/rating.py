from sqlalchemy import Column, Float, Date, BigInteger

from src.database import Base


class Rating(Base):
    __tablename__ = 'rating'

    rating_id = Column(BigInteger, primary_key=True, index=True)
    created_at = Column(Date)
    board_game_id = Column(BigInteger)
    user_id = Column(BigInteger)
    score = Column(Float)
