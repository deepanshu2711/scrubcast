from pydantic import BaseModel


class VideoCreate(BaseModel):
    url: str
    title: str | None = None
    video_id: str
    description: str | None = None
