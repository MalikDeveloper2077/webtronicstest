from typing import Optional

from pydantic import BaseModel


class EstimationIn(BaseModel):
    """Like/Dislike"""
    post_id: int
    user_id: int
    value: int  # LIKE_VALUE or DISLIKE_VALUE


class Estimation(EstimationIn):
    id: Optional[int] = None


class PostIn(BaseModel):
    text: str


class Post(PostIn):
    id: Optional[int] = None
    user_id: int

    class Config:
        orm_mode = True
