import logging
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status

from web_app.models import User
from web_app.schemas.video import VideoCreate, VideoOut
from web_app.services.videos.video_service import (
    VideoService,
    get_video_service
)
from web_app.utils.auth import get_current_user

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("", response_model=VideoOut, status_code=status.HTTP_201_CREATED)
async def create_video(
    video_data: VideoCreate,
    current_user: User = Depends(get_current_user),
    video_service: VideoService = Depends(get_video_service),
):
    created_video = await video_service.create_video(video_data, current_user.id)
    return created_video


@router.get("/videos/latest", response_model=list[VideoOut])
async def get_latest_videos(
    video_service: VideoService = Depends(get_video_service)
):
    return await video_service.get_latest_videos()


@router.get("/videos/latest/{genre}", response_model=list[VideoOut])
async def get_latest_videos_by_genre(
    genre: str,
    video_service: VideoService = Depends(get_video_service)
):
    return await video_service.get_latest_videos_by_genre(genre)


@router.get("/videos/date-range", response_model=list[VideoOut])
async def get_videos_by_date_range(
    start_date: datetime,
    end_date: datetime,
    video_service: VideoService = Depends(get_video_service)
):
    return await video_service.get_videos_by_date_range(start_date, end_date)


@router.get("/videos/{video_id}", response_model=VideoOut)
async def get_video_by_id(
    video_id: int,
    video_service: VideoService = Depends(get_video_service)
):
    video = await video_service.video_repository.get_video_by_id(video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video


@router.get("/videos/by-title/{title}", response_model=VideoOut)
async def get_video_by_title(
    title: str,
    video_service: VideoService = Depends(get_video_service)
):
    video = await video_service.video_repository.get_video_by_title(title)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video
