from pydantic import BaseModel


class UploadVideo(BaseModel):
    title: str
    description: str


video = UploadVideo(title="title", description="disctiption")

print(video)
video.description.replace("sc", "pp")
data = video.dict()
description = data.pop("description")
print(data)
print(description)