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
    # return db.query(models.Movie).filter(models.Movie.user_id == user_id).offset(offset).limit(limit).all()
    movies = db.query(models.Movie).filter(
        models.Movie.user_id == user_id).offset(offset).limit(limit).all()

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


def get_all_movie(db: Session, id: int):
    return db.query(models.Movie).filter(models.Movie.user_id == id).first()


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
