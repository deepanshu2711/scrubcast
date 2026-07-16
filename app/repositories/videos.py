from sqlmodel import Session, select

from app.config.database import Videos
from app.model.schema.videos import VideoCreate


class VideoRepository():
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        return self.session.exec(select(Videos)).all()

    def add_video(self, payload: VideoCreate):
        self.session.add(payload)
        self.session.commit()
        self.session.refresh(payload)
        return
