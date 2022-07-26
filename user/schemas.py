from typing import Union

from pydantic import BaseModel


class UserDetail(BaseModel):
    id: int
    username: str
    full_name: Union[str, None] = None


class User(BaseModel):
    id: int
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class Registration(BaseModel):
    username: str
    email: str
    full_name: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class UserInDB(User):
    hashed_password: str


