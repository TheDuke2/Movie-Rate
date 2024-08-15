from fastapi import Depends, FastAPI, HTTPException, APIRouter
from sqlalchemy.orm import Session

from app import  crud, schema
from app.database import get_db
from app.auth import get_current_user

from logger import get_logger

logger = get_logger(__name__)

comment_router = APIRouter()

@comment_router.get("/{movie_id}")
def get_comments(movie_id: int, db: Session = Depends(get_db)):
    comments = crud.get_comments(db, movie_id)
    return {'message': 'success', 'data': comments}


@comment_router.post('')
def movie_comment(comment: schema.CommentCreate, user: schema.User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_comment = crud.create_comments(
        db,
        comment,
        user_id=user.id,
        movie_id=comment.movie_id
    )
    return {'message': 'success', 'comment': new_comment}


@comment_router.post('/{parent_id}')
def movie_nested_comment(parent_id: int, comment: schema.CommentNested, user: schema.User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_comment = crud.create_nested_comments(
        db,
        comment,
        user_id=user.id,
        movie_id=comment.movie_id,
    )
    return {'message': 'success', 'comment': new_comment}

