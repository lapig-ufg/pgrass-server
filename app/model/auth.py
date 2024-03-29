from typing import Dict, Optional
from pydantic import BaseModel, EmailStr

from bson import ObjectId
from pydantic import BaseConfig, BaseModel
from datetime import datetime


from app.db import MongoModel
from app.utils.password import get_password_hash, verify_password


class TokenData(BaseModel):
    username: str | None = None

class CreateUser(BaseModel):
    username: str
    firstName: str
    lastName: Optional[str] | None = None
    email: EmailStr
    agreements: bool | None = None
    disabled: bool | None = None
    password: str
    institution: str | None = None
    fullName: str | None = None
    avatar: Optional[str]
    properties: Dict = dict()
    
    class Config(BaseConfig):
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
            ObjectId: lambda oid: str(oid),
        }

    @classmethod
    def from_mongo(cls, data: dict):
        return cls(**dict(data))

    def mongo(self, **kwargs):
        exclude_unset = kwargs.pop('exclude_unset', True)
        by_alias = kwargs.pop('by_alias', True)

        parsed = self.dict(
            exclude_unset=exclude_unset,
            by_alias=by_alias,
            **kwargs,
        )
        if '_id' not in parsed :
            parsed['_id'] = parsed['username']
        if 'hashed_password' not in parsed and 'password' in parsed:
            parsed['hashed_password'] = get_password_hash(parsed.pop('password'))
        
        return parsed


class UserOauth(BaseModel):
    username: str
    firstName: str
    lastName: Optional[str] | None = None
    email: EmailStr
    agreements: bool | None = None
    disabled: bool | None = None
    password: str | None = None
    institution: str | None = None
    fullName: str | None = None
    avatar: Optional[str]
    properties: Dict = dict()

    class Config(BaseConfig):
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
            ObjectId: lambda oid: str(oid),
        }

    @classmethod
    def from_mongo(cls, data: dict):
        return cls(**dict(data))

    def mongo(self, **kwargs):
        exclude_unset = kwargs.pop('exclude_unset', True)
        by_alias = kwargs.pop('by_alias', True)

        parsed = self.dict(
            exclude_unset=exclude_unset,
            by_alias=by_alias,
            **kwargs,
        )
        if '_id' not in parsed:
            parsed['_id'] = parsed['username']
        if 'hashed_password' not in parsed and 'password' in parsed:
            parsed['hashed_password'] = get_password_hash(parsed.pop('password'))

        return parsed

class User(MongoModel):
    id: str
    username: str
    firstName: str
    lastName: Optional[str]
    email: EmailStr
    hashed_password: Optional[str]
    agreements: bool | None = None
    disabled: bool | None = None
    institution: str | None = None
    full_name: str | None = None
    avatar: Optional[str]
    status: Optional[str]
    properties: Dict = dict()
    
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.id = self.username
        self.full_name = f"{self.firstName} {self.lastName}"

    def get_user(self, **kwargs):
        exclude_unset = kwargs.pop('exclude_unset', True)
        by_alias = kwargs.pop('by_alias', True)

        parsed = self.dict(
            exclude_unset=exclude_unset,
            by_alias=by_alias,
            **kwargs,
        )
        parsed.pop('hashed_password')
        return parsed

    def get_user_auth(self, **kwargs):
        by_alias = kwargs.pop('by_alias', True)

        parsed = self.dict(
            by_alias=by_alias,
            **kwargs,
        )
        parsed.pop('hashed_password')
        return parsed
        


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenUI(BaseModel):
    access_token: str
    token_type: str
    user: Dict

