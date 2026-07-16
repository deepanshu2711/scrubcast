from sqlmodel import Session
from app.model.schema.videos import VideoCreate
from app.repositories.videos import VideoRepository


class VideosService:
    def __init__(self, session: Session):
        self.repository = VideoRepository(session)

    def get_all_videos(self):
        self.repository.get_all()

    def add_video(self, payload: VideoCreate):
        return self.repository.add_video(payload)
