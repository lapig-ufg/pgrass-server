
from datetime import timedelta

from fastapi import Depends, APIRouter, HTTPException, status


from fastapi.security import OAuth2PasswordRequestForm

from app.model.auth import CreateUser, Token, User
from app.utils.auth import authenticate_user, create_access_token
from app.config import settings
from app.db import db_users
from pydantic import BaseModel


router = APIRouter()

class Login(BaseModel):
    username: str
    password: str
    rememberMe: bool



@router.post("/signup", summary="Create new user", status_code=201)
async def create_user(new_user: CreateUser):
    if len(new_user.password) <= 6 :
        raise HTTPException(400,'O password tem que ter mais de 6 caracter')
    await db_users.insert_one(new_user.mongo())
    return new_user

@router.post('/login', summary="Create access and refresh tokens for user", response_model=Token)
async def login_for_access_token(form_data: Login):
    try:
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
                'firstName':user.firstName,
                'lastName':user.lastName ,
                'email':user.email,
                'institution':user.institution, 
                'rememberMe':form_data.rememberMe
                }, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer","rememberMe":form_data.rememberMe }
    except Exception as e:
        raise HTTPException(500,f'{e}')

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
            'firstName':user.firstName,
            'lastName':user.lastName ,
            'email':user.email,
            'institution':user.institution 
            }, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

