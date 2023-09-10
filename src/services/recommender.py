import random

from sqlalchemy.orm import Session

from src.schemas.response import RecommendSchema
from src.repositories import boardgame, rating
from src.util import load_pickled_model


class RecommenderService:
    _instance = None
    _user_id_base = 218044
    _rec_n = 10

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.model = load_pickled_model()

    @staticmethod
    def get_user_threshold(user_id: int, db: Session):
        user_mean = rating.get_user_mean_rating(db, user_id)[0]
        user_stddev = rating.get_user_stddev_rating(db, user_id)[0]
        return user_mean + (user_stddev / 2)

    def recommend_to_single(self, user_id: int, db: Session):
        threshold = self.get_user_threshold(user_id, db)

        rated_ids = rating.get_rated_board_games(db, user_id)
        unrated_board_games = boardgame.get_unrated_board_game_ids(db, rated_ids)

        user_id += self._user_id_base
        predictions = [self.model.predict(str(user_id), str(bg_id[0])) for bg_id in unrated_board_games]
        over_threshold = [x for x in predictions if x.est >= threshold]
        top_predictions = random.sample(over_threshold, 10)

        top_boardgame_ids = [int(float(pred.iid)) for pred in top_predictions]
        top_boardgame_score = [float(pred.est) for pred in top_predictions]
        recommend_list = [RecommendSchema(id=bgg_id, score=score)
                          for bgg_id, score in zip(top_boardgame_ids, top_boardgame_score)]

        return recommend_list
