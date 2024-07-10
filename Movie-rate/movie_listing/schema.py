from pydantic import BaseModel

class MovieBase(BaseModel):
    title: str
    username: str
    description: str

class Movie(MovieBase):
    id: int
    user_id: int
    
    class Config:
        orm_mode = True

class BookCreate(MovieBase):
    pass

class BookUpdate(MovieBase):
    pass
    