from pydantic import BaseModel


class VideoCreate(BaseModel):
    url: str
    title: str | None = None
    video_id: str
    description: str | None = None


class SnippetCreate(BaseModel):
    text: str
    start: float | None = None
    duration: float | None = None
    video_id: int | None
