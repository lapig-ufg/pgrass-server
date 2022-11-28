import requests
from urllib.parse import parse_qs
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.db import db_dataset, ObjectId
from app.model.auth import TokenData, User
from app.config import settings, logger
from app.utils.password import verify_password
from pymongo import MongoClient
from app.utils.exceptions import OauthGithubException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")


def get_user(username: str):
    with MongoClient(settings.MONGODB_URL) as client:
        db = client.pgrass
        if (user := db.users.find_one({"$or": [{"username": username}, {"email": username}]})) is not None:
            return User.from_mongo(user)

def get_user_by_email_username(username: str, email: str):
    with MongoClient(settings.MONGODB_URL) as client:
        db = client.pgrass
        if (user := db.users.find_one({"$or": [{"username": username}, {"email": email}]})) is not None:
            return User.from_mongo(user)

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


def secure_query_dataset(username):
    return {'$or': [{'username': username}, {'public': True}]}


async def have_permission_access_dataset(_id, username):
    if dataset := await db_dataset.find_one({"_id": ObjectId(_id), **secure_query_dataset(username)}):
        return True
    raise HTTPException(status_code=401, detail="You do not have permission to access this data")


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=401, detail="Inactive user")
    return current_user

async def get_oauth_token(code: str):
    token = None
    url = 'https://github.com/login/oauth/access_token'
    headers = {'Content-Type': 'application/json'}
    params = {
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': settings.OAUTH_REDIRECT_URL,
        'client_id': settings.OAUTH_CLIENT_ID,
        'client_secret': settings.OAUTH_CLIENT_SECRET,
    }
    response = requests.post(url, headers=headers, json=params)

    if response.status_code == 200:
        res = dict(parse_qs(response.text))
        if 'error' in res:
            raise OauthGithubException(res['error_description'][0])
        else:
            token = res['access_token'][0]
    else:
        raise OauthGithubException(f"Error fetching token from github: {str(response.content)}")

    return token

async def get_oauth_user(token: str):
    user = None
    url = 'https://api.github.com/user'
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        res = dict(parse_qs(response.text))
        if 'error' in res:
            raise OauthGithubException(res['error_description'][0])
        else:
            user = response.json()
    else:
        logger.exception(response)
        raise OauthGithubException(f"Error fetching user from github: {str(response.text)}")
    return user
