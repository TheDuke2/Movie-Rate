from fastapi import Depends, FastAPI, HTTPException, APIRouter
from sqlalchemy.orm import Session


from app import  crud, schema
from app.database import engine, Base, get_db
from app.auth import get_current_user


from logger import get_logger

logger = get_logger(__name__)

movie_router = APIRouter()

@movie_router.get("")
def get_movies(user: schema.User, db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
    movies = crud.get_all_movie(
        db,
        user_id=user.id,
        offset=offset,
        limit=limit
    )
    return {'message': 'success', 'data': movies}


@movie_router.get("/{movie_id}")
def get_movies(movie_id: int, db: Session = Depends(get_db)):
    movies = crud.get_movie(
        db,
        movie_id=movie_id,
    )
    return {'message': 'success', 'data': movies}

@movie_router.post('')
def create_movie(payload: schema.MovieCreate, user: schema.User = Depends(get_current_user), db: Session = Depends(get_db)):
    crud.create_movie(
        db,
        payload,
        user_id=user.id
    )
    logger.info('Movie Created Successfully'),
    return {'message': 'success'}

@movie_router.put('/{movie_id}')
def update_movie(movie_id: int, payload: schema.MovieUpdate, user: schema.User = Depends(get_current_user), db: Session = Depends(get_db)):
    movie = crud.get_movie(db, movie_id)
    current_user = user.id
    if not movie:
        logger.info(f'Movie with {movie_id} does not exist.')
        raise HTTPException(status_code=404, detail="movie not found")
    if movie.user_id != current_user:
        logger.info(f'User with {current_user} is not allowed to edit movie.') 
        raise HTTPException(status_code=404, detail="this user is not allowed to edit this movie")
    
    updated_movie = crud.update_movie(db, movie_id, current_user, payload)
    return {'message': 'success', 'data': updated_movie}

@movie_router.delete('/{movie_id}')
def delete_movie(
    movie_id: int,
    user: schema.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    movie = crud.get_movie(db, movie_id)
    current_user = user.id
    if not movie:
        logger.info(f'Movie with {movie_id} does not exist.')
        raise HTTPException(status_code=404, detail="movie not found")
    if movie.user_id != current_user:
        logger.info(f'User with {current_user} is not allowed to delete movie.') 
        raise HTTPException(status_code=404, detail="this user is not allowed to edit this movie")
    
    deleted_movie = crud.delete_movie(db, movie_id, current_user)
    
    return {'message': "Movie deleted successfully"}