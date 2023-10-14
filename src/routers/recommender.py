from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database import get_db
from src.schemas.request import RecWithGenreRequest, RecForGroupRequest
from src.services.recommender import RecommenderService
from src.schemas.response import RecommendationResponse

router = APIRouter(prefix='/recommends', tags=['recommenders'])
recommender_service = RecommenderService()


@router.post('', response_model=RecommendationResponse)
async def recommend_by_genre(request: RecWithGenreRequest, db: Session = Depends(get_db)):
    predictions = recommender_service.recommend_by_genre(request.user_id, request.genre_id, db)
    return RecommendationResponse(result=predictions)


@router.post('/group', response_model=RecommendationResponse)
async def recommend_for_group(request: RecForGroupRequest, db: Session = Depends(get_db)):
    predictions = recommender_service.recommend_for_group(request.members, request.seed, db)
    return RecommendationResponse(result=predictions)
