import random
from collections import defaultdict

from sqlalchemy.orm import Session

from src.repositories import boardgame, rating, user
from src.utils import *


def count_recommended_ids_per_member(group_recommendable: list[list]):
    recommendation_count_dict = defaultdict(int)
    for recommendable in group_recommendable:
        for bg_id in recommendable:
            recommendation_count_dict[bg_id] += 1
    return recommendation_count_dict


def get_recommendable_by_count(recommendable_ids: list[list]):
    recommendable_by_count_dict = defaultdict(list)
    recommendation_count_dict = count_recommended_ids_per_member(recommendable_ids)

    for bg_id, count in recommendation_count_dict.items():
        recommendable_by_count_dict[count].append(bg_id)
    recommendable_by_count_dict = dict(sorted(
        recommendable_by_count_dict.items(),
        key=lambda item: item[0],
        reverse=True
    ))

    return recommendable_by_count_dict


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
        user_id = user.get_user_index(db, user_id)
        input_tensor = process_model_input(user_id, boardgame_with_genre)

        predictions = self.model(input_tensor)
        recommendable_ids = get_recommendable_items(boardgame_with_genre, predictions)
        sampled_recommendations = random.sample(recommendable_ids, self.num_recommendation)

        recommended_list = [int(bgg_id) for bgg_id in sampled_recommendations]

        return recommended_list

    def recommend_for_group(self, member_ids: list[int], seed: int, db: Session):
        num_member = len(member_ids)
        group_rated_ids = [ids[0] for ids in rating.get_group_rated_board_games(db, member_ids)]
        board_game_candidates = boardgame.get_unrated_board_games_of_group(db, group_rated_ids, num_member)

        member_ids = user.get_group_user_index(db, member_ids)
        num_member = len(member_ids)
        input_tensor = process_group_input(member_ids, board_game_candidates)

        predictions = self.model(input_tensor)
        group_recommendable = get_group_recommendable_items(board_game_candidates, predictions, num_member)
        recommendable_by_count_dict = get_recommendable_by_count(group_recommendable)

        final_recommendations = self.get_most_recommended_ids(recommendable_by_count_dict, seed)

        return final_recommendations

    def get_most_recommended_ids(self, recommendable_dict: dict, seed: int):
        final_recommendations = []
        random.seed(seed)

        for count in recommendable_dict:
            num_current_recommendations = self.num_recommendation - len(final_recommendations)
            recommendable_board_games = recommendable_dict[count]
            final_recommendations.extend(
                recommendable_board_games
                if len(recommendable_board_games) <= num_current_recommendations
                else random.sample(recommendable_board_games, num_current_recommendations)
            )

        return final_recommendations
