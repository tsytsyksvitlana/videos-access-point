from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from web_app.repositories.video_repository import VideoRepository

pytestmark = pytest.mark.anyio


async def test_video_repository_get_video_by_url(db_session: AsyncSession, create_test_videos):
    repo = VideoRepository(session=db_session)
    url = "http://test.com/video2"
    video = await repo.get_video_by_url(url)

    assert video is not None
    assert video.url == url


async def test_video_repository_get_latest_videos(db_session: AsyncSession, create_test_videos):
    repo = VideoRepository(session=db_session)
    videos = await repo.get_latest_videos(limit=2)

    assert len(videos) == 2
    assert videos[0].upload_date >= videos[1].upload_date


async def test_video_repository_get_latest_videos_by_genre(db_session: AsyncSession, create_test_videos):
    repo = VideoRepository(session=db_session)
    videos = await repo.get_latest_videos_by_genre(genre="TestGenre", limit=5)

    assert len(videos) == 2
    assert all(video.genre == "TestGenre" for video in videos)


async def test_video_repository_get_videos_by_date_range(db_session: AsyncSession, create_test_videos):
    repo = VideoRepository(session=db_session)
    start = datetime.now(timezone.utc) - timedelta(days=4)
    end = datetime.now(timezone.utc)

    videos = await repo.get_videos_by_date_range(start, end)

    assert all(start <= video.upload_date <= end for video in videos)


async def test_video_repository_get_video_by_id(db_session: AsyncSession, create_test_videos):
    repo = VideoRepository(session=db_session)
    video = create_test_videos[0]
    fetched = await repo.get_video_by_id(video.id)

    assert fetched is not None
    assert fetched.id == video.id


async def test_video_repository_get_video_by_title(db_session: AsyncSession, create_test_videos):
    repo = VideoRepository(session=db_session)
    video = create_test_videos[1]
    fetched = await repo.get_video_by_title(video.title)

    assert fetched is not None
    assert fetched.title == video.title
