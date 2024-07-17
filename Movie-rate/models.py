from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False, index=True)
    full_name = Column(String)
    hashed_password = Column(String, nullable=False)

    movies = relationship("Movie", back_populates="user")

class Movie(Base):
    __tablename__ = "movies"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    username = Column(String, nullable=False)
    description = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="movies")
    
class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    comment = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    movie_id = Column(Integer, ForeignKey("movie.id"))
    
    user = relationship('User', back_populates="comments")
    movie = relationship('Movie', back_populates="comments")
    
class Rating(Base):
    __tablename__ = 'rating'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    rating = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    movie_id = Column(Integer, ForeignKey("movie.id"))
    
    user = relationship('User', back_populates="rating")
    movie = relationship('Movie', back_populates="rating")