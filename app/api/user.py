from fastapi import Depends, APIRouter, HTTPException, status
from app.utils.auth import get_user

router = APIRouter()

@router.get("/{username}", summary="Get user by username", status_code=201)
async def find_user(username: str):
    try:
        user = get_user(username)
        _user = {
            'id': user.username,
            'name': user.firstName + user.lastName,
            'email': user.email,
            'institution': user.institution,
            'avatar': user.avatar,
            'status': 'online',
            'sub': user.username
        }
        return _user
    except Exception as e:
        raise HTTPException(500, f'{e}')