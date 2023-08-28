from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database import get_db
from src.services.recommender import RecommenderService
from src.schemas.response import Response

router = APIRouter(prefix='/recommends', tags=['recommenders'])
recommender_service = RecommenderService()


@router.get('/{user_id}', response_model=Response)
async def recommend_to_single(user_id: int, db: Session = Depends(get_db)):
    predictions = recommender_service.recommend_to_single(user_id, db)
    return Response(result=predictions)
