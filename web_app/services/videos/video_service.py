from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from web_app.db.postgres_helper import postgres_helper as pg_helper
from web_app.repositories.video_repository import VideoRepository


class VideoService:
    def __init__(self, video_repository: VideoRepository):
        self.video_repository = video_repository


def get_user_service(
    session: AsyncSession = Depends(pg_helper.session_getter)
) -> VideoService:
    return VideoService(video_repository=VideoRepository(session))
