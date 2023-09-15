from pydantic import BaseModel


class RecommendationResponse(BaseModel):
    result: list[int]
