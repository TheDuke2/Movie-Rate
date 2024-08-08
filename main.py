from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from auth import pwd_context, authenticate_user, create_access_token, get_current_user
import  crud
import schema
from database import engine, Base, get_db
from typing import Optional

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get('/')
def home():
    return {"message": "Welcome to the movie rating API"}


@app.post("/signup", response_model=schema.User)
def signup(user: schema.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    hashed_password = pwd_context.hash(user.password)
    if db_user:
        raise HTTPException(
            status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user, hashed_password=hashed_password)


@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/movies/")
def get_movies(db: Session = Depends(get_db), user: schema.User = Depends(get_current_user), offset: int = 0, limit: int = 10):
    movies = crud.get_all_movie(
        db,
        user_id=user.id,
        offset=offset,
        limit=limit
    )
    return {'message': 'success', 'data': movies}


@app.get("/movies/{movie_id}")
def get_movies(movie_id: int, db: Session = Depends(get_db)):
    movies = crud.get_movie(
        db,
        movie_id=movie_id,
    )
    return {'message': 'success', 'data': movies}


@app.get("/ratings/{movie_id}")
def get_rating(movie_id: int, db: Session = Depends(get_db)):
    rating = crud.get_rating(db, movie_id)
    if rating is None:
        raise HTTPException(status_code=404, detail="Rating not found")
    return {'message': 'success', 'rating': rating}


@app.get("/comments/{movie_id}")
def get_comments(movie_id: int, db: Session = Depends(get_db)):
    comments = crud.get_comments(db, movie_id)
    # if comments is None:
    #     raise HTTPException(status_code=404, detail="Comment not found")
    return {'message': 'success', 'data': comments}


@app.post('/movies')
def create_movie(payload: schema.MovieCreate, user: schema.User = Depends(get_current_user), db: Session = Depends(get_db)):
    crud.create_movie(
        db,
        payload,
        user_id=user.id
    )
    return {'message': 'success'}

@app.put('/movie/{movie_id}')
def update_movie(movie_id: int, payload: schema.MovieUpdate, user: schema.User = Depends(get_current_user), db: Session = Depends(get_db)):
    movie = crud.get_movie(db, movie_id)
    current_user = user.id
    if not movie:
        raise HTTPException(status_code=404, detail="movie not found")
    if movie.user_id != current_user:
        raise HTTPException(status_code=404, detail="this user is not allowed to edit this movie")
    
    updated_movie = crud.update_movie(db, movie_id, current_user, payload)
    return {'message': 'success', 'data': updated_movie}

@app.delete('/movie/{movie_id}')
def delete_movie(
    movie_id: int,
    user: schema.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    movie = crud.get_movie(db, movie_id)
    current_user = user.id
    if not movie:
        raise HTTPException(status_code=404, detail="movie not found")
    if movie.user_id != current_user:
        raise HTTPException(status_code=404, detail="this user is not allowed to edit this movie")
    
    deleted_movie = crud.delete_movie(db, movie_id, current_user)
    
    return {'message': "Movie deleted successfully", 'data': deleted_movie}

@app.post('/rating')
def rate_movie(payload: schema.RatingCreate, user: schema.User = Depends(get_current_user), db: Session = Depends(get_db)):
    crud.rate_movie(
        db,
        payload
        # user_id=user.id
    )
    return {'message': 'success'}


@app.post('/comments')
def movie_comment(comment: schema.CommentCreate, user: schema.User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_comment = crud.create_comments(
        db,
        comment,
        user_id=user.id,
        movie_id=comment.movie_id
    )
    return {'message': 'success', 'comment': new_comment}


@app.post('/comments/{parent_id}')
def movie_nested_comment(parent_id: int, comment: schema.CommentNested, user: schema.User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_comment = crud.create_nested_comments(
        db,
        comment,
        user_id=user.id,
        movie_id=comment.movie_id,
        # parent_id=parent_id
    )
    return {'message': 'success', 'comment': new_comment}


