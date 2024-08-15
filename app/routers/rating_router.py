from fastapi import Depends, FastAPI, HTTPException, APIRouter
from sqlalchemy.orm import Session

from app import  crud, schema
from app.database import get_db
from app.auth import get_current_user

from logger import get_logger

logger = get_logger(__name__)

rating_router = APIRouter()


@rating_router.post('')
def rate_movie(payload: schema.RatingCreate, user: schema.User = Depends(get_current_user), db: Session = Depends(get_db)):
    crud.rate_movie(
        db,
        payload
    )
    return {'message': 'success'}

@rating_router.get("/{movie_id}")
def get_rating(movie_id: int, db: Session = Depends(get_db)):
    rating = crud.get_rating(db, movie_id)
    if rating is None:
        raise HTTPException(status_code=404, detail="Rating not found")
    return {'message': 'success', 'rating': rating}