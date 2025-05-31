import logging

from fastapi import APIRouter, Depends, status

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
