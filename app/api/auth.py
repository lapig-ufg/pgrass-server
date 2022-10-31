from datetime import timedelta
from typing import Dict

from fastapi import Depends, APIRouter, HTTPException, status, Query

from typing import Optional
from fastapi.security import OAuth2PasswordRequestForm

from app.model.auth import Token
from app.utils.auth import authenticate_user, create_access_token
from app.config import settings
from app.db import db_users
from app.utils.auth import get_password_hash

from pydantic import EmailStr

router = APIRouter()

@router.post("/signup", summary="Create new user", status_code=201)
async def create_user(
    username: str,
    first_name: str,
    last_name: str,
    email: EmailStr,
    institution: str,
    properties: Dict,
    password: Optional[str] =   Query(None, min_length=6)
):
    if password == None:
        raise HTTPException(400,'Passowd nao informado') 
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

@router.post('/login', summary="Create access and refresh tokens for user", response_model=Token)
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
        data={
            "sub": user.username, 
            'first_name':user.first_name,
            'last_name':user.last_name ,
            'email':user.email,
            'institution':user.institution 
            }, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/token", response_model=Token)
async def get_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": user.username, 
            'first_name':user.first_name,
            'last_name':user.last_name ,
            'email':user.email,
            'institution':user.institution 
            }, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

