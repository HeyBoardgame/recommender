from sqlalchemy import func
from sqlalchemy.sql.expression import case
from sqlalchemy.orm import Session

from src.models.rating import Rating


def get_rated_board_games(db: Session, user_id: int):
    return db.query(Rating.board_game_id).filter(Rating.user_id == user_id).all()


def get_group_rated_board_games(db: Session, member_ids: list[int]):
    return (db.query(Rating.board_game_id)
            .group_by(Rating.board_game_id)
            .having(func.count(func.distinct(Rating.user_id)) == len(member_ids))
            .having(func.sum(case((Rating.user_id.in_(member_ids), 1), else_=0)) == len(member_ids))
            .all())
