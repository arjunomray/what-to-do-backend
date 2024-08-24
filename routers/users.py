from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ..models.user import User
from ..utils.database import get_session

from ..internals.auth import (
    ACCESS_TOKEN_EXPIRE_MIN,
    authenticate_user,
    create_access_token,
    get_password_hash,
)
from ..schema.token import Token


router = APIRouter(prefix="/users")


@router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect Username or Password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MIN)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")


@router.post("/register")
async def register(user: User):
    with next(get_session()) as session:
        user_in_db = session.get(User, user.username)
        if user_in_db:
            raise HTTPException(status_code=400, detail="User already exists")
        user.hashed_password = get_password_hash(user.hashed_password)
        session.add(user)
        session.commit()
        session.refresh(user)

        return user
