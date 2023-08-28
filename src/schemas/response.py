from pydantic import BaseModel


class RecommendSchema(BaseModel):
    id: int
    score: float


class Response(BaseModel):
    result: list[RecommendSchema]
