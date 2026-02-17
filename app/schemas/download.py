
from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime

class Quality(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Format(str, Enum):
    MP4 = "mp4"
    MP3 = "mp3"

class Platform(str, Enum):
    YOUTUBE = "youtube"
    VIMEO = "vimeo"

class DownloadStatus(str, Enum):
    PENDING = "pending"
    DOWNLOADING = "downloading"
    COMPLETED = "completed"
    FAILED = "failed"

class DownloadBase(BaseModel):
    url: HttpUrl
    quality: Quality = Quality.MEDIUM
    format: Format = Format.MP4

class DownloadCreate(DownloadBase):
    pass

class DownloadUpdate(BaseModel):
    status: Optional[DownloadStatus] = None

class DownloadRead(DownloadBase):
    id: int
    status: DownloadStatus
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class DownloadStatusInfo(BaseModel):
    id: int
    status: DownloadStatus
    progress: float = Field(..., ge=0, le=100)
    speed: Optional[float] = None
    eta: Optional[int] = None
    error_message: Optional[str] = None

class DownloadList(BaseModel):
    items: List[DownloadRead]
    total: int
