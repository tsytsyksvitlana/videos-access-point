from datetime import datetime

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from web_app.db.postgres_helper import postgres_helper as pg_helper
from web_app.models.video import Video
from web_app.repositories.video_repository import VideoRepository
from web_app.schemas.video import VideoCreate


class VideoService:
    def __init__(self, video_repository: VideoRepository):
        self.video_repository = video_repository

    async def get_video_by_url(self, url: str) -> Video | None:
        return await self.video_repository.get_video_by_url(url)

    async def get_latest_videos(self, limit: int = 100) -> list[Video]:
        return await self.video_repository.get_latest_videos(limit)

    async def get_latest_videos_by_genre(self, genre: str, limit: int = 100) -> list[Video]:
        return await self.video_repository.get_latest_videos_by_genre(genre, limit)

    async def get_videos_by_date_range(self, start_date: datetime, end_date: datetime) -> list[Video]:
        return await self.video_repository.get_videos_by_date_range(start_date, end_date)

    async def create_video(self, video_data: VideoCreate, user_id: int) -> Video:
        video = Video(
            **video_data.model_dump(exclude={"url"}),
            url=str(video_data.url),
            user_id=user_id
        )
        new_video = await self.video_repository.create_obj(video)

        await self.video_repository.session.commit()
        await self.video_repository.session.refresh(new_video)
        return new_video


def get_video_service(
    session: AsyncSession = Depends(pg_helper.session_getter)
) -> VideoService:
    return VideoService(video_repository=VideoRepository(session))
