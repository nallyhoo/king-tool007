
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class ProcessingJob(Base):
    __tablename__ = "processing_jobs"

    id = Column(Integer, primary_key=True, index=True)
    operation = Column(String, nullable=False)
    input_file = Column(String, nullable=False)
    output_file = Column(String)
    status = Column(String, default="pending")
    progress = Column(Float, default=0.0)
    error_message = Column(String)

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="processing_jobs")
