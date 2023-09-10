from sqlalchemy.orm import Session

from src.models.boardgame import BoardGame


def get_unrated_board_game_ids(db: Session, rated_ids: list[int]):
    return (db.query(BoardGame.board_game_id)
            .filter(BoardGame.board_game_id.notin_(rated_ids))
            .all())
