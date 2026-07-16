from fastapi import APIRouter

from app.config.database import SessionDep
from app.model.schema.videos import VideoCreate
from app.services.videos import VideosService

router = APIRouter()


@router.get('/')
def get_all_videos(session: SessionDep):
    service = VideosService(session)
    return service.get_all_videos()


@router.post('/')
def submit_video(payload: VideoCreate, session: SessionDep):
    service = VideosService(session)
    return service.add_video(payload)
