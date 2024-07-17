from pydantic import BaseModel

class UserBase(BaseModel):
    Usename: str
    
class UserCreate(UserBase):
    full_name: str
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class MovieBase(BaseModel):
    title: str
    username: str
    description: str

class Movie(MovieBase):
    id: int
    user_id: int
    
    class Config:
        orm_mode = True

class MovieCreate(MovieBase):
    pass

class MovieUpdate(MovieBase):
    pass

class CommentBase(BaseModel):
    comment: str

class Comment(CommentBase):
    id: int
    user_id: int
    movie_id: int
    
    class Config:
        orm_mode = True
        
class CommentCreate(CommentBase):
    pass

class RatingBase(BaseModel):
    rating: int

class Rating(RatingBase):
    id: int
    user_id: int
    movie_id: int
    
    class Config:
        orm_mode = True
        
class RatingCreate(RatingBase):
    pass