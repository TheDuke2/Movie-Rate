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
