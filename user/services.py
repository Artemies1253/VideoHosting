import os
from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from user.schemas import Registration, TokenData, User
from video.models import User as UserModel


SECRET_KEY = "fdk13h6-s;mdh639bxsl238bnla82qchauenba71jjguwabvmzhgh18ngkl24hm,"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_user_dir(user_name):
    os.mkdir(f"media/{user_name}")


async def authenticate_user(username: str, password: str):
    user = await UserModel.objects.get_or_none(username=username)

    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def create_user(registration_data: Registration):
    user_data = registration_data.dict()
    user = await UserModel.objects.get_or_none(username=user_data.get("username"))
    print(user)
    if user:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="username already in use"
        )
    hashed_password = get_password_hash(user_data.pop("password"))
    user_data["hashed_password"] = hashed_password
    user = await UserModel.objects.create(**user_data)
    create_user_dir(user.username)
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await UserModel.objects.get_or_none(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
