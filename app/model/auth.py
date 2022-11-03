from typing import Dict
from pydantic import BaseModel, EmailStr

from app.db import MongoModel
from app.utils.auth import get_password_hash


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(MongoModel):
    id: str
    username: str
    firstName: str
    lastName: str
    email: EmailStr
    agreements: bool | None = None
    disabled: bool | None = None
    hashed_password: str
    institution: str | None = None
    full_name: str | None = None
    properties: Dict = dict()
    
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.id = self.username
        self.hashed_password = get_password_hash(self.hashed_password)
        self.full_name = f"{self.firstName} {self.lastName}"
