
from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.schemas.download import DownloadStatus

class Download(Base):
    __tablename__ = "downloads"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True)
    status = Column(Enum(DownloadStatus), default=DownloadStatus.PENDING)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="downloads")
