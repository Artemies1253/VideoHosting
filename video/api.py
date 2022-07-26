import shutil
from typing import List

from fastapi import UploadFile, File, APIRouter, Form, BackgroundTasks, Request, Depends
from fastapi.responses import StreamingResponse
from fastapi.security import OAuth2PasswordBearer
from starlette.templating import Jinja2Templates

from user.models import User
from user.services import get_current_user
from video.schemas import GetListVideo
from video.models import Video
from video.services import save_video, open_file, add_like, delete_like

video_router = APIRouter(prefix="/video", tags=["video"])

templates = Jinja2Templates(directory="templates")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@video_router.post("/")
async def create_video(
        back_tasks: BackgroundTasks,
        title: str = Form(...),
        description: str = Form(...),
        file: UploadFile = File(...),
        user: User = Depends(get_current_user)
):
    return await save_video(user=user, file=file, back_tasks=back_tasks, title=title, description=description)


@video_router.get("/user/{user_pk}", response_model=List[GetListVideo])
async def get_list_video(user_pk: int):
    video_list = await Video.objects.filter(user=user_pk).all()
    return video_list


@video_router.get("/{video_pk}")
async def get_streaming_video(request: Request, video_pk: int) -> StreamingResponse:
    file, status_code, content_length, headers = await open_file(request, video_pk)
    response = StreamingResponse(
        file,
        media_type="video/mp4",
        status_code=status_code
    )
    response.headers.update({
        "Accept-Ranges": "bytes",
        "Content-Length": str(content_length),
        **headers
    })
    return response


@video_router.post("/like/{video_pk}")
async def like(video_pk: int, user: User = Depends(get_current_user)):
    video = await Video.objects.select_related("like_user").get_or_none(id=video_pk, like_user__id=user)

    if video is None:
        video = await add_like(video_pk, user)
    else:
        video = await delete_like(video_pk, user)

    return video
