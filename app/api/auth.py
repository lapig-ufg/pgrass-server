from datetime import timedelta
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.model.auth import CreateUser, Token, User, TokenUI, UserOauth
from app.utils.auth import authenticate_user, get_user, create_access_token, get_oauth_token, get_oauth_user, get_user_by_email_username
from app.config import settings, logger
from app.db import db_users
from pydantic import BaseModel
from app.utils.exceptions import OauthGithubException

router = APIRouter()


class Login(BaseModel):
    username: str
    password: str

class Oauth(BaseModel):
    code: str
    state: str

class SocialUser(BaseModel):
    idToken: str
    id: str
    name: str
    email: str
    photoUrl: str
    firstName: str
    lastName: str
    provider: str

@router.post("/signup", summary="Create new user", status_code=201)
async def create_user(new_user: CreateUser):
    if (user := await db_users.find_one({"$or": [{"username": new_user.username}, {"email": new_user.email}]})) is not None:
        raise HTTPException(400, 'Username or email exists on database.')
    if len(new_user.password) <= 6:
        raise HTTPException(400, 'O password tem que ter mais de 6 caracter')
    await db_users.insert_one(new_user.mongo())
    return new_user


@router.post('/login', summary="Create access and refresh tokens for user", response_model=TokenUI)
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
        user_token = {
            'id': user.username,
            'name': user.firstName + user.lastName,
            'email': user.email,
            'institution': user.institution,
            'avatar': user.avatar,
            'status': 'online',
            'sub': user.username
        }
        access_token = create_access_token(
            data=user_token, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer", "user": user_token}
    except Exception as e:
        raise HTTPException(500, f'{e}')


@router.post('/oauth-github', summary="Create access and refresh tokens for user by oauth github", response_model=TokenUI)
async def login_oauth(oauth_params: Oauth):
    try:
        token = await get_oauth_token(oauth_params.code)
        oauth_user = await get_oauth_user(token)
        user = get_user_by_email_username(oauth_user['login'], oauth_user['email'])
        if not user:
            new_user = UserOauth(**{
                'username': oauth_user['login'],
                'firstName': oauth_user['name'],
                'lastName': '',
                'email': oauth_user['email'],
                'agreements': True,
                'institution': oauth_user['company'],
                'avatar': oauth_user['avatar_url'],
                'password': oauth_user['login'],
                'properties': {},
                'fullName': None,
            })
            await db_users.insert_one(new_user.mongo())
            user = new_user
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        user_token = {
            'id': user.username,
            'name': user.firstName,
            'email': user.email,
            'institution': user.institution,
            'avatar': user.avatar,
            'status': 'online',
            'sub': user.username
        }
        access_token = create_access_token(
            data=user_token, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer", "user": user_token}
    except OauthGithubException as e:
        logger.exception(e)
        raise HTTPException(400, f'{e}')
    except Exception as e:
        logger.exception(e)
        raise HTTPException(500, f'{e}')

@router.post('/oauth-google', summary="Create access and refresh tokens for user by oauth google", response_model=TokenUI)
async def login_oauth(social_user: SocialUser):
    try:
        user = get_user_by_email_username(social_user.id, social_user.email)
        if not user:
            new_user = UserOauth(**{
                'username': social_user.firstName.lower().replace(' ', ''),
                'firstName': social_user.firstName,
                'lastName': social_user.lastName,
                'email': social_user.email,
                'agreements': True,
                'institution': '',
                'avatar': social_user.photoUrl,
                'password': social_user.firstName.lower().replace(' ', ''),
                'properties': {},
                'fullName': None,
            })
            await db_users.insert_one(new_user.mongo())
            user = new_user
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        user_token = {
            'id': user.username,
            'name': user.firstName,
            'email': user.email,
            'institution': user.institution,
            'avatar': user.avatar,
            'status': 'online',
            'sub': user.username
        }
        access_token = create_access_token(
            data=user_token, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer", "user": user_token}
    except OauthGithubException as e:
        logger.exception(e)
        raise HTTPException(400, f'{e}')
    except Exception as e:
        logger.exception(e)
        raise HTTPException(500, f'{e}')


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
            'firstName': user.firstName,
            'lastName': user.lastName,
            'email': user.email,
            'institution': user.institution
        }, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
