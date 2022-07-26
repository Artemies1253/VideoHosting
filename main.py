from fastapi import FastAPI

from followers.api import followers_router
from video.api import video_router
from user.api import auth_routes
from db import database, metadata, engine

app = FastAPI()

# metadata.drop_all(engine)
metadata.create_all(engine)
app.state.database = database

@app.on_event("startup")
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()


app.include_router(auth_routes)
app.include_router(video_router)
app.include_router(followers_router)
