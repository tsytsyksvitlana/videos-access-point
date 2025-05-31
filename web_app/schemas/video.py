from pydantic import BaseModel, Field, HttpUrl


class VideoCreate(BaseModel):
    title: str = Field(..., max_length=100)
    description: str | None = Field(None, max_length=255)
    genre: str = Field(..., max_length=50)
    url: HttpUrl = Field(...)
