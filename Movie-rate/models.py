from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship

from database import Base


# movie_rating_relationship = Table(
#     "movie_rating", Base.metadata, 
#     Column('movie_id', Integer, ForeignKey("movies.id"),primary_key=True),
#     Column('rating_id', Integer, ForeignKey("ratings.id"),primary_key=True)
# )

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False, index=True)
    full_name = Column(String)
    hashed_password = Column(String, nullable=False)

    movies = relationship("Movie", back_populates="users")
    ratings = relationship("Rating", back_populates="users")
    comments = relationship("Comment", back_populates="users")

class Movie(Base):
    __tablename__ = "movies"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    users = relationship("User", back_populates="movies")
    comments = relationship("Comment", back_populates="movies")
    ratings = relationship("Rating", back_populates="movies")
    
    
class Rating(Base):
    __tablename__ = 'ratings'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    rating = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    movie_id = Column(Integer, ForeignKey("movies.id"))
    
    movies = relationship('Movie', back_populates="ratings")
    users = relationship('User', back_populates="ratings")

class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    contents = Column(String, nullable=False)
    
    user_id = Column(Integer, ForeignKey("users.id"))
    movie_id = Column(Integer, ForeignKey("movies.id"))
    
    parent_id = Column(Integer, ForeignKey("comments.id"), nullable=True)
    
    children = relationship('Comment', backref='parent', remote_side=[id])
    users = relationship('User', back_populates="comments")
    movies = relationship('Movie', back_populates="comments")

    