from fastapi import FastAPI

from app.database import engine, Base
from app.routers.auth_router import auth_router
from app.routers.movie_router import movie_router
from app.routers.rating_router import rating_router
from app.routers.comment_router import comment_router

from logger import get_logger

logger = get_logger(__name__)
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router, tags=['auth'], prefix='/auth')
app.include_router(movie_router, tags=['movie'], prefix='/movie')
app.include_router(rating_router, tags=['rating'], prefix='/rating')
app.include_router(comment_router, tags=['comment'], prefix='/comment')


@app.get('/')
def home():
    return {"message": "Welcome to the movie rating API"}



