from fastapi import APIRouter

from app.config.database import SessionDep
from app.services.chat import ChatService

router = APIRouter()


@router.get('/start/{video_id}')
def start_chat(video_id: int, session: SessionDep):
    service = ChatService(session)
    return service.initiate_chat(video_id)
