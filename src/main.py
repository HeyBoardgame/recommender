from fastapi import FastAPI


def start_app():
    app = FastAPI(title='HeyBoardGame Recommender API')
    return app


app = start_app()
