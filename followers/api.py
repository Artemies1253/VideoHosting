from pprint import pprint
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response
from starlette import status

from followers.schemas import FollowerCreate, SubscriberDetail, PublisherDetail
from followers.models import Follower
from schemas import Id
from user.models import User
from user.services import get_current_active_user

followers_router = APIRouter(prefix="/followers", tags=["followers"])


@followers_router.post("/add", response_model=Id)
async def add_follower(
        data: FollowerCreate,
        user: User = Depends(get_current_active_user)
):
    publisher = await User.objects.get_or_none(id=data.user)
    if publisher is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found"
        )
    follower = await Follower.objects.get_or_create(subscriber=user, publisher=publisher)
    return follower[0]


@followers_router.post("/subscribers_list", response_model=List[SubscriberDetail])
async def subscribers_list(
        user: User = Depends(get_current_active_user)
):
    return await Follower.objects.select_related(["subscriber"]).filter(publisher=user).all()


@followers_router.post("/follower_list", response_model=List[PublisherDetail])
async def publisher_list(
        user: User = Depends(get_current_active_user)
):
    return await Follower.objects.select_related(["publisher"]).filter(subscriber=user).all()


@followers_router.delete("/delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def add_follower(
        user_id: int,
        user: User = Depends(get_current_active_user)
):
    follower = await Follower.objects.select_related(["publisher"]).get_or_none(
        subscriber=user, publisher__id=user_id
    )
    if follower:
        await follower.delete()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


