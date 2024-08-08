from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from collections import defaultdict

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

def get_user_by_id (db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id)


def create_movie(db: Session, movie: schema.MovieCreate, user_id: int = None):
    db_movie = models.Movie(
        **movie.model_dump(),
        user_id=user_id
    )
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

def get_movie(db: Session, movie_id: int):
    return db.query(models.Movie).filter(models.Movie.id == movie_id).first()

def get_all_movie(db: Session, user_id: int = None, offset: int = 0, limit: int = 10):
    # return db.query(models.Movie).filter(models.Movie.user_id == user_id).offset(offset).limit(limit).all()
    query = db.query(models.Movie)
    if user_id is not None:
        query = query.filter(models.Movie.user_id == user_id)
    movies = query.offset(offset).limit(limit).all()
    
    movie_details = []
    for movie in movies:
        average_rating = db.query(func.avg(models.Rating.rating)).filter(
            models.Rating.movie_id == movie.id).scalar()
        comments = db.query(models.Comment).filter(
            models.Comment.movie_id == movie.id).all()

        movie_details.append({
            'movie': movie,
            'ratings': average_rating,
            'comments': comments
        })
    return movie_details

def update_movie(db: Session, movie_id: int, user_id: int, movie_payload: schema.MovieUpdate):
    movie = get_movie(db, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    if movie.user_id != user_id:
        raise HTTPException(status_code=404, detail="user not found")
    
    payload_dict = movie_payload.dict(exclude_unset=True)

    for k, v in payload_dict.items():
        setattr(movie, k, v)

    db.add(movie)
    db.commit()
    db.refresh(movie)

    return movie

def delete_movie(db: Session, movie_id: int, user_id: int):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    if movie.user_id != user_id:
        raise HTTPException(status_code=403, detail="User not allowed to delete this movie")
    
    db.delete(movie)
    db.commit()

    return {"message": "Movie deleted successfully"}


# def get_all_movie(db: Session, id: int):
#     return db.query(models.Movie).filter(models.Movie.user_id == id).first()


def get_rating(db: Session, movie_id: int):
    # return db.query(models.Rating).filter(models.Rating.movie_id == movie_id).first()
    average_rating = db.query(func.avg(models.Rating.rating)).filter(
        models.Rating.movie_id == movie_id).scalar()

    return average_rating or 0


def rate_movie(db: Session, rating: schema.Rating):
    db_rating = models.Rating(
        **rating.model_dump(),
    )
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating


def create_comments(db: Session, payload: schema.CommentCreate, user_id: int, movie_id: int):
    db_comments = models.Comment(
        contents=payload.contents,
        user_id=user_id,
        movie_id=movie_id,
    )
    db.add(db_comments)
    db.commit()
    db.refresh(db_comments)
    return db_comments

def create_nested_comments(db: Session, payload: schema.CommentNested, user_id: int, movie_id: int):
    if payload.parent_id is not None:
        parent_comment = db.query(models.Comment).filter(models.Comment.id == payload.parent_id).first()
    if parent_comment is None:
        raise HTTPException(status_code=400, detail="Parent comment not found")
    
    db_comments = models.Comment(
        contents=payload.contents,
        user_id=user_id,
        movie_id=movie_id,
        parent_id=payload.parent_id
    )
    db.add(db_comments)
    db.commit()
    db.refresh(db_comments)
    return db_comments


def get_comments(db: Session, movie_id: int):
    comments = db.query(models.Comment).filter(models.Comment.movie_id == movie_id).all()
    
    comments_by_parent_id = defaultdict(list)
    for comment in comments:
        comments_by_parent_id[comment.parent_id].append(comment)
        
    def nested_comment_tree(parent_id):
        nested_comment = []
        for comment in comments_by_parent_id.get(parent_id, []):
            comment_dict = {
                "id": comment.id,
                "contents": comment.contents,
                "user_id": comment.user_id,
                "movie_id": comment.movie_id,
                "children": nested_comment_tree(comment.id)
            }
            nested_comment.append(comment_dict)
        return nested_comment
    comment_tree = nested_comment_tree(None)
    return comment_tree

def get_comments_children(db: Session, comment_id: int):
    return db.query(models.Comment).filter(models.Comment.parent_id == comment_id).all()
