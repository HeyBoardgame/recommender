import random
from collections import defaultdict

from sqlalchemy.orm import Session

from src.repositories import boardgame, rating
from src.utils import *


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

    def recommend_for_group(self, member_ids: list[int], seed: int, db: Session):
        group_rated_ids = [ids[0] for ids in rating.get_group_rated_board_games(db, member_ids)]
        board_game_candidates = boardgame.get_unrated_board_games_of_group(db, group_rated_ids)

        input_tensor = process_group_input(member_ids, board_game_candidates)

        predictions = self.model(input_tensor)
        group_recommendable = get_group_recommendable_items(board_game_candidates, predictions, len(member_ids))

        recommendation_count_dict = defaultdict(int)
        for recommendable in group_recommendable:
            for bg_id in recommendable:
                recommendation_count_dict[bg_id] += 1

        recommendable_by_count_dict = defaultdict(list)
        for bg_id, count in recommendation_count_dict.items():
            recommendable_by_count_dict[count].append(bg_id)
        recommendable_by_count_dict = dict(sorted(
            recommendable_by_count_dict.items(),
            key=lambda item: item[0],
            reverse=True
        ))

        final_recommendations = []
        random.seed(seed)
        for count in recommendable_by_count_dict:
            num_current_recommendations = self.num_recommendation - len(final_recommendations)
            recommendable_board_games = recommendable_by_count_dict[count]
            final_recommendations.extend(
                recommendable_board_games
                if len(recommendable_board_games) <= num_current_recommendations
                else random.sample(recommendable_board_games, num_current_recommendations)
            )

        return final_recommendations
