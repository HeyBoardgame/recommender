import pickle
import os

from sqlalchemy.orm import Session

from src.schemas.response import RecommendSchema
from src.repositories import boardgame, rating


class RecommenderService:
    _instance = None
    _pickle_path = os.environ['PICKLE_PATH']
    _user_id_base = 218044
    _rec_n = 10

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        model_path = self._pickle_path
        with open(model_path, 'rb') as f:
            self.model = pickle.load(f)

    def recommend_to_single(self, user_id: int, db: Session):
        rated_ids = rating.get_rated_board_games(db, user_id)
        unrated_board_games = boardgame.get_unrated_board_game_ids(db, rated_ids)

        # user_id += self._user_id_base
        predictions = [self.model.predict(str(user_id), str(bg_id[0])) for bg_id in unrated_board_games]

        def sort_key_est(pred):
            return pred.est

        predictions.sort(key=sort_key_est, reverse=True)
        top_predictions = predictions[:self._rec_n]

        top_boardgame_ids = [int(float(pred.iid)) for pred in top_predictions]
        top_boardgame_score = [float(pred.est) for pred in top_predictions]
        recommend_list = [RecommendSchema(id=bgg_id, score=score)
                          for bgg_id, score in zip(top_boardgame_ids, top_boardgame_score)]

        return recommend_list
