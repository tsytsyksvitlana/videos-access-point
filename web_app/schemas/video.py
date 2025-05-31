from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl


class VideoCreate(BaseModel):
    title: str = Field(..., max_length=100)
    description: str | None = Field(None, max_length=255)
    genre: str = Field(..., max_length=50)
    url: HttpUrl = Field(...)


class VideoOut(BaseModel):
    id: int
    title: str
    description: str | None
    genre: str
    url: HttpUrl
    upload_date: datetime
    user_id: int

    class Config:
        orm_mode = True
