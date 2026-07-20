from fastapi import APIRouter

from app.config.database import SessionDep
from app.model.schema.chat import AskQuestion
from app.services.chat import ChatService

router = APIRouter()


@router.get('/start/{video_id}')
def start_chat(video_id: int, session: SessionDep):
    service = ChatService(session)
    return service.initiate_chat(video_id)


# This is ask route
@router.post('/ask/{video_id}')
def ask_question(video_id: int, body: AskQuestion, session: SessionDep):
    service = ChatService(session)
    return service.ask_question(video_id, question=body.question)
