from pydantic import BaseModel


class RecWithGenreRequest(BaseModel):
    user_id: int
    genre_id: int
