from sqlalchemy.orm import Session

from src.models.rating import Rating


def get_rated_board_games(db: Session, user_id: int):
    return db.query(Rating.board_game_id).filter(Rating.user_id == user_id).all()
