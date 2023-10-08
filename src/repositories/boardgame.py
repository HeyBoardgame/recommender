from sqlalchemy.orm import Session

from src.models.boardgame import BoardGame
from src.models.genre_of_board_game import GenreOfBoardGame


def get_unrated_board_games_by_genre(db: Session, rated_ids: list[int], genre_id: int):
    return (db.query(BoardGame.board_game_id, BoardGame.bgg_id_index, BoardGame.weight_index)
            .join(GenreOfBoardGame, BoardGame.board_game_id == GenreOfBoardGame.board_game_id)
            .filter(BoardGame.board_game_id.notin_(rated_ids), GenreOfBoardGame.genre_id == genre_id)
            .all())


def get_unrated_board_games_of_group(db: Session, rated_ids: list[int]):
    return (db.query(BoardGame.board_game_id, BoardGame.bgg_id_index, BoardGame.weight_index)
            .filter(BoardGame.board_game_id.notin_(rated_ids))
            .all())

