
from typing import Optional

from pydantic import BaseModel


class VideoBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    file_path: str


class VideoCreate(VideoBase):
    title: str


class VideoUpdate(VideoBase):
    pass


class VideoInDBBase(VideoBase):
    id: int
    title: str
    owner_id: int

    class Config:
        orm_mode = True


class Video(VideoInDBBase):
    pass
