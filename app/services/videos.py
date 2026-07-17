from youtube_transcript_api import YouTubeTranscriptApi
from sqlmodel import Session

from app.model.schema.videos import SnippetCreate, VideoCreate
from app.repositories.videos import VideoRepository


class VideosService:
    def __init__(self, session: Session):
        self.repository = VideoRepository(session)

    def get_all_videos(self):
        return self.repository.get_all()

    def add_video(self, payload: VideoCreate):
        transcript = YouTubeTranscriptApi().fetch(payload.video_id)
        video = self.repository.add_video(payload)

        snippets = [
            SnippetCreate(
                text=snippet.text,
                start=snippet.start,
                duration=snippet.duration,
                video_id=video.id
            ) for snippet in transcript.snippets
        ]
        self.repository.add_snippets(snippets)
        return
