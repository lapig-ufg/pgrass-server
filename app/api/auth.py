from datetime import timedelta
from typing import Dict

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.model.auth import Token, User
from app.utils.auth import authenticate_user, create_access_token, get_current_active_user
from app.config import settings
from app.db import db_users
from app.utils.auth import get_password_hash

from pydantic import EmailStr

router = APIRouter()

@router.post("/new", status_code=201)
async def create_upload_files(
    username: str,
    first_name: str,
    last_name: str,
    email: EmailStr,
    password: str,
    institution: str,
    properties: Dict
):
    await db_users.insert_one({
        '_id': username,
        'username': username,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'hashed_password': get_password_hash(password),
        'institution': institution,
        'disabled': False,
        'properties': properties
        })
    return {'username': username,
        'first_name': first_name,
        'last_name': last_name}

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]