
from pydantic import BaseModel
from typing import Optional

class ProcessingJobBase(BaseModel):
    operation: str
    input_file: str

class ProcessingJobCreate(ProcessingJobBase):
    pass

class ProcessingJobUpdate(BaseModel):
    status: Optional[str] = None
    progress: Optional[float] = None
    output_file: Optional[str] = None
    error_message: Optional[str] = None

class ProcessingJobRead(ProcessingJobBase):
    id: int
    status: str
    progress: float
    output_file: Optional[str]
    error_message: Optional[str]
    owner_id: int

    class Config:
        orm_mode = True
