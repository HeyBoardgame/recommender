from sqlalchemy.orm import Session

from src.models.boardgame import BoardGame


def get_unrated_board_games(db: Session, rated_ids: list[int]):
    return (db.query(BoardGame.board_game_id, BoardGame.bgg_id_index, BoardGame.weight_index)
            .filter(BoardGame.board_game_id.notin_(rated_ids))
            .all())
