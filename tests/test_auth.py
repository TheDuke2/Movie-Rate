import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi import HTTPException, Depends
from app.auth import verify_password, authenticate_user, create_access_token, get_current_user
from app.auth import crud, oauth2_scheme, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

DUMMY_PASSWORD = "testpassword"
DUMMY_HASHED_PASSWORD = "$2y$10$eIbXTWEn.R1sUmUPuzLLTeFVmYvWhEXpsKGZ64elHpRpOe.L1QCIe"  
DUMMY_USER = MagicMock()
DUMMY_USER.hashed_password = DUMMY_HASHED_PASSWORD

def test_verify_password():
    assert verify_password(DUMMY_PASSWORD, DUMMY_HASHED_PASSWORD) is True
    assert verify_password("wrongpassword", DUMMY_HASHED_PASSWORD) is False

@patch('app.crud.get_user_by_username')
@patch('app.auth.verify_password')
def test_authenticate_user(mock_verify_password, mock_get_user_by_username):
    mock_get_user_by_username.return_value = DUMMY_USER
    mock_verify_password.return_value = True

    assert authenticate_user(MagicMock(), "testuser", DUMMY_PASSWORD) == DUMMY_USER
    mock_verify_password.return_value = False
    assert authenticate_user(MagicMock(), "testuser", DUMMY_PASSWORD) is False
    mock_get_user_by_username.return_value = None
    assert authenticate_user(MagicMock(), "nonexistentuser", DUMMY_PASSWORD) is False

@patch('app.auth.jwt.encode')
def test_create_access_token(mock_encode):
    data = {"sub": "testuser"}
    mock_encode.return_value = "encoded_jwt_token"

    token = create_access_token(data, expires_delta=timedelta(minutes=10))
    assert token == "encoded_jwt_token"

    token = create_access_token(data)
    assert token == "encoded_jwt_token"

@patch('app.crud.get_user_by_username')
@patch('app.auth.jwt.decode')
def test_get_current_user(mock_decode, mock_get_user_by_username):
    mock_decode.return_value = {"sub": "testuser"}
    mock_get_user_by_username.return_value = DUMMY_USER

    db = MagicMock()
    token = "valid_jwt_token"
    user = get_current_user(db, token)
    assert user == DUMMY_USER

    mock_decode.side_effect = JWTError
    with pytest.raises(HTTPException):
        get_current_user(db, token)

    mock_get_user_by_username.return_value = None
    with pytest.raises(HTTPException):
        get_current_user(db, token)
