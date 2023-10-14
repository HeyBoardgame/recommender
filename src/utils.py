import boto3
import torch
import os

from src.ai.factorization_machine import FactorizationMachineModel

ACCESS_KEY = os.environ['S3_ACCESS_KEY']
SECRET_KEY = os.environ['S3_SECRET_KEY']
BUCKET_NAME = os.environ['S3_BUCKET_NAME']
MODEL_PATH = os.environ['MODEL_PATH']


def load_fm_model():
    num_feats = 230159
    model = FactorizationMachineModel(num_feats, embed_dim=64, sigmoid=True)
    loaded_model_path = '/tmp/fm_model.pth'

    s3 = boto3.client(
        's3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY
    )
    s3.download_file(BUCKET_NAME, MODEL_PATH, loaded_model_path)

    param_dict = torch.load(loaded_model_path, map_location=torch.device('cpu'))
    model.load_state_dict(param_dict)
    os.remove(loaded_model_path)

    return model


def process_model_input(user_id, board_games):
    user_idx_offset = 12115
    weight_idx_offset = 12110
    user_idx = user_id + user_idx_offset
    input_data = [(bgg_id_idx, weight_idx + weight_idx_offset, user_idx)
                  for bgg_id, bgg_id_idx, weight_idx in board_games]
    input_tensor = torch.tensor(input_data)

    return input_tensor


def process_group_input(member_ids, board_games):
    input_tensor = process_model_input(member_ids[0], board_games)
    for member_id in member_ids[1:]:
        input_tensor = torch.cat([input_tensor, process_model_input(member_id, board_games)], dim=0)

    return input_tensor


def get_recommendable_items(board_games, predictions):
    binary_predictions = torch.round(predictions)
    one_indices = (binary_predictions == 1).nonzero().squeeze().tolist()

    recommendable = []
    for idx in one_indices:
        recommendable.append(board_games[idx][0])

    return recommendable


def get_group_recommendable_items(board_games, predictions, num_member):
    num_item = len(board_games)
    member_predictions = []
    for i in range(num_member):
        member_predictions.append(predictions[i * num_item:i * num_item + num_item])

    group_recommendable = []
    for prediction in member_predictions:
        group_recommendable.append(get_recommendable_items(board_games, prediction))

    return group_recommendable
