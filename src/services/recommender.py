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

    def recommend_by_genre(self, user_id: int, genre_id: int, db: Session):
        rated_ids = [ids[0] for ids in rating.get_rated_board_games(db, user_id)]
        boardgame_with_genre = boardgame.get_unrated_board_games_by_genre(db, rated_ids, genre_id)
        input_tensor = process_model_input(2522, boardgame_with_genre)

        predictions = self.model(input_tensor)
        recommendable_ids = get_recommendable_items(boardgame_with_genre, predictions)
        sampled_recommendations = random.sample(recommendable_ids, self.num_recommendation)

        recommended_list = [int(bgg_id) for bgg_id in sampled_recommendations]

        return recommended_list
