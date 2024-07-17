from sqlalchemy.orm import Session
import models
import schema

def create_user(db: Session, user: schema.UserCreate, hashed_password: str): 
    db_user = models.User(
        username=user.username, 
        full_name=user.full_name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_movie(db: Session, movie: schema.MovieCreate, user_id: int = None):
    db_movie = models.Movie(
        **movie.model_dump(),
        user_id=user_id
    )
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

def get_movie(db: Session, user_id: int = None, offset: int = 0, limit: int = 10):
    return db.query(models.Movie).filter(models.Movie.id == user_id).offset(offset).limit(limit).all()

def get_movie(db: Session, id: int):
    return db.query(models.Movie).filter(models.Movie.id == id).first()