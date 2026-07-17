from sqlmodel import Session, select

from app.config.database import Snippets, Videos
from app.model.schema.videos import VideoCreate, SnippetCreate


class VideoRepository():
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        return self.session.exec(select(Videos)).all()

    def add_video(self, payload: VideoCreate):
        video = Videos(**payload.model_dump())
        self.session.add(video)
        self.session.commit()
        self.session.refresh(video)
        return video

    def add_snippets(self, snippets: list[SnippetCreate]):
        db_snippets = [Snippets(**s.model_dump()) for s in snippets]
        self.session.add_all(db_snippets)
        self.session.commit()
        return db_snippets

    def get_snippets(self, video_id: int):
        statement = select(Snippets).where(Snippets.video_id == video_id)
        return self.session.exec(statement).all()
