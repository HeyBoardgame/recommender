import random

from sqlalchemy.orm import Session

from src.repositories import boardgame, rating
from src.util import load_fm_model, process_model_input, get_recommendable_items


class RecommenderService:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.model = load_fm_model()
        self.num_recommendation = 10

    def recommend_to_single(self, user_id: int, db: Session):
        rated_ids = [ids[0] for ids in rating.get_rated_board_games(db, user_id)]
        unrated_board_games = boardgame.get_unrated_board_games(db, rated_ids)
        input_tensor = process_model_input(2522, unrated_board_games)

        predictions = self.model(input_tensor)
        recommendable_ids = get_recommendable_items(unrated_board_games, predictions)
        sampled_recommendations = random.sample(recommendable_ids, self.num_recommendation)

        recommended_list = [int(bgg_id) for bgg_id in sampled_recommendations]

        return recommended_list
