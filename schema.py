from pydantic import BaseModel
from typing import List, Optional


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    full_name: str
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class MovieBase(BaseModel):
    title: str
    genre: str
    duration: int
    description: str


class Movie(MovieBase):
    id: int
    user_id: int
    ratings: list['Rating'] = []
    comments: list['Comment'] = []

    class Config:
        orm_mode = True


class MovieCreate(MovieBase):
    pass


class MovieUpdate(MovieBase):
    pass


class CommentBase(BaseModel):
    contents: str
    movie_id: int


class Comment(CommentBase):
    id: int
    user_id: int
    children: List['Comment'] = []

    class Config:
        orm_mode = True


class CommentCreate(CommentBase):
    pass


class CommentNested(CommentBase):
    parent_id: Optional[int] = None


class RatingBase(BaseModel):
    rating: int
    movie_id: int


class Rating(RatingBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class RatingCreate(RatingBase):
    pass
