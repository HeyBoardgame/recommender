from sqlalchemy.orm import Session
from sqlalchemy import func

from src.models import rating


def get_rated_board_games(db: Session, user_id: int):
    return db.query(rating.Rating.board_game_id).filter(rating.Rating.user_id == user_id).all()


def get_user_mean_rating(db: Session, user_id: int):
    return db.query(func.avg(rating.Rating.score)).filter(rating.Rating.user_id == user_id).first()


def get_user_stddev_rating(db: Session, user_id: int):
    return db.query(func.STD(rating.Rating.score)).filter(rating.Rating.user_id == user_id).first()
