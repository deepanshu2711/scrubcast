from sqlmodel import Session, select
from app.config.database import Snippets


class ChatRepository():
    def __init__(self, session: Session):
        self.session = session

    def get_snippets(self, video_id: int):
        statement = select(Snippets).where(Snippets.video_id == video_id)
        return self.session.exec(statement).all()
