from typing import Dict
from pydantic import BaseModel, EmailStr

from app.db import MongoModel

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(MongoModel):
    id: str
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    hashed_password: str
    institution: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
    properties: Dict = dict()
    
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.id = self.username
        self.full_name = f"{self.first_name} {self.last_name}"
