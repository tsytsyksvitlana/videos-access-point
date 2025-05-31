from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from web_app.models.video import Video
from web_app.repositories.video_repository import VideoRepository
from web_app.schemas.video import VideoCreate
from web_app.services.videos.video_service import VideoService

pytestmark = pytest.mark.anyio


async def test_video_service_create_video(db_session: AsyncSession, create_test_users):
    user = create_test_users[0]
    video_repo = VideoRepository(session=db_session)
    video_service = VideoService(video_repo)

    video_data = VideoCreate(
        title="New Video",
        description="Cool video",
        genre="Action",
        url="http://test.com/newvideo",
        upload_date=datetime.utcnow()
    )

    created_video = await video_service.create_video(video_data, user.id)

    assert created_video.id is not None
    assert created_video.title == video_data.title
    assert created_video.url == str(video_data.url)
    assert created_video.user_id == user.id


async def test_video_service_get_video_by_url(db_session: AsyncSession, create_test_videos):
    video_repo = VideoRepository(session=db_session)
    video_service = VideoService(video_repo)

    target_video = create_test_videos[0]
    video = await video_service.get_video_by_url(target_video.url)

    assert video is not None
    assert video.url == target_video.url


async def test_video_service_get_videos_by_date_range(db_session: AsyncSession, create_test_videos):
    video_repo = VideoRepository(session=db_session)
    video_service = VideoService(video_repo)

    start_date = datetime.now(timezone.utc) - timedelta(days=4)
    end_date = datetime.now(timezone.utc)

    videos = await video_service.get_videos_by_date_range(start_date, end_date)

    assert all(start_date <= video.upload_date <= end_date for video in videos)


async def test_video_service_get_latest_videos_by_genre(db_session: AsyncSession, create_test_videos):
    video_repo = VideoRepository(session=db_session)
    video_service = VideoService(video_repo)

    videos = await video_service.get_latest_videos_by_genre("TestGenre", limit=10)

    assert all(video.genre == "TestGenre" for video in videos)
    assert len(videos) > 0


async def test_video_service_get_videos_by_date_range(db_session: AsyncSession, create_test_videos):
    video_repo = VideoRepository(session=db_session)
    video_service = VideoService(video_repo)

    start_date = datetime.now(timezone.utc) - timedelta(days=4)
    end_date = datetime.now(timezone.utc)

    videos = await video_service.get_videos_by_date_range(start_date, end_date)

    assert all(start_date <= video.upload_date <= end_date for video in videos)

