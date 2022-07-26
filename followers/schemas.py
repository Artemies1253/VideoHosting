from typing import List

from pydantic import BaseModel

from user.schemas import UserDetail


class FollowerCreate(BaseModel):
    user: int


class PublisherDetail(BaseModel):
    id: int
    publisher: UserDetail


class SubscriberDetail(BaseModel):
    id: int
    subscriber: UserDetail
