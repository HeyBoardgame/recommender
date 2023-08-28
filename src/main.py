from fastapi import FastAPI

from src.routers import recommender


def include_routers(app):
    app.include_router(recommender.router)


def start_app():
    app = FastAPI(title='HeyBoardGame Recommender API')
    include_routers(app)
    return app


app = start_app()
