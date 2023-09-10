import boto3
import pickle
import os

ACCESS_KEY = os.environ['S3_ACCESS_KEY']
SECRET_KEY = os.environ['S3_SECRET_KEY']
BUCKET_NAME = os.environ['S3_BUCKET_NAME']


def load_pickled_model():
    key = 'surprise_svd.pkl'
    s3 = boto3.resource(
        's3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY
    )
    file = s3.Bucket(BUCKET_NAME).Object(key).get()['Body'].read()
    model = pickle.loads(file)

    return model
