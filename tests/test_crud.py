import pytest
from unittest.mock import MagicMock, patch
from app.crud import create_user, get_user_by_username, get_user_by_id, create_movie, get_movie
from app.models import User, Movie
from app import models

# Example data
mock_user_data = {"username": "testuser", "full_name": "Test User"}
mock_movie_data = {"title": "Test Movie", "genre": "Test genre", "duration": 90, "description": "A test movie" }

# Test create_user
def test_create_user():
    db = MagicMock()
    user_schema = MagicMock(**mock_user_data)
    hashed_password = "hashed_password"
    
    new_user = create_user(db, user_schema, hashed_password)
    
    print(f"db.add called with: {db.add.call_args}")
    print(f"db.refresh called with: {db.refresh.call_args}")
    
    db.commit.assert_called_once()
    db.add.assert_called_once()
    db.refresh.assert_called_once_with(new_user)
    
    assert new_user.username == user_schema.username
    assert new_user.full_name == user_schema.full_name
    assert new_user.hashed_password == hashed_password

# Test get_user_by_username
def test_get_user_by_username():
    db = MagicMock()
    
    mock_user = models.User(**mock_user_data)
    
    db.query.return_value.filter.return_value.first.return_value = mock_user
    
    user = get_user_by_username(db, "testuser")
    

    assert user.username == "testuser"
    db.query.return_value.filter.assert_called_once()

# Test create_movie
def test_create_movie():
    db = MagicMock()
    
    movie_schema = MagicMock()
    movie_schema.model_dump.return_value = mock_movie_data
    
    mock_movie = models.Movie(**mock_movie_data, user_id=1)

    db.add.return_value = None
    db.commit.return_value = None
    db.refresh.return_value = None

    
    new_movie = create_movie(db, movie_schema, user_id=1)
    print(db.mock_calls)

    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once()
    
    
    assert new_movie.title == mock_movie.title
    assert new_movie.genre == mock_movie.genre
    assert new_movie.duration == mock_movie.duration
    assert new_movie.description == mock_movie.description
    assert new_movie.user_id == mock_movie.user_id   
    

# Test get_movie
def test_get_movie():
    db = MagicMock()
    mock_movie = models.Movie(**mock_movie_data)
    db.query.return_value.filter.return_value.first.return_value = mock_movie
    
    movie = get_movie(db, 1)
    
    assert movie.title == "Test Movie"
    db.query().filter.assert_called_once()
