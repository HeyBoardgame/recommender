from sqlalchemy.orm import Session

from src.models import rating


def get_rated_board_games(db: Session, user_id: int):
    return db.query(rating.Rating.board_game_id).filter(rating.Rating.user_id == user_id).all()
