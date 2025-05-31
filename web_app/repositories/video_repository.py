from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from web_app.models import Video
from web_app.repositories.base_repository import BaseRepository


class VideoRepository(BaseRepository[Video]):
    def __init__(self, session: AsyncSession):
        super().__init__(Video, session)

    async def get_video_by_url(self, url: str) -> Video | None:
        query = select(Video).where(Video.url == url)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_latest_videos(self, limit: int = 100) -> list[Video]:
        query = select(Video).order_by(Video.upload_date.desc()).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_latest_videos_by_genre(self, genre: str, limit: int = 100) -> list[Video]:
        query = (
            select(Video)
            .where(Video.genre == genre)
            .order_by(Video.upload_date.desc())
            .limit(limit)
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_videos_by_date_range(self, start_date: datetime, end_date: datetime) -> list[Video]:
        query = (
            select(Video)
            .where(Video.upload_date >= start_date, Video.upload_date <= end_date)
            .order_by(Video.upload_date.desc())
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_video_by_id(self, video_id: int) -> Video | None:
        query = select(Video).where(Video.id == video_id)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_video_by_title(self, title: str) -> Video | None:
        query = select(Video).where(Video.title == title)
        result = await self.session.execute(query)
        return result.scalars().first()
