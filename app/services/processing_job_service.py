
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy.future import select

from app.models.processing_job import ProcessingJob
from app.schemas.processing_job import ProcessingJobCreate, ProcessingJobUpdate

# Synchronous functions for Celery worker
def get_sync(db: Session, job_id: int) -> Optional[ProcessingJob]:
    return db.query(ProcessingJob).filter(ProcessingJob.id == job_id).first()

def update_sync(db: Session, *, db_obj: ProcessingJob, obj_in: ProcessingJobUpdate) -> ProcessingJob:
    update_data = obj_in.dict(exclude_unset=True)
    for field in update_data:
        if hasattr(db_obj, field):
            setattr(db_obj, field, update_data[field])
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

# Asynchronous functions for FastAPI app
async def create_job(
    db: AsyncSession, *, obj_in: ProcessingJobCreate, owner_id: int
) -> ProcessingJob:
    db_obj = ProcessingJob(**obj_in.dict(), owner_id=owner_id)
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

async def get_job(
    db: AsyncSession, *, job_id: int, owner_id: int
) -> Optional[ProcessingJob]:
    result = await db.execute(
        select(ProcessingJob).filter(ProcessingJob.id == job_id, ProcessingJob.owner_id == owner_id)
    )
    return result.scalars().first()

async def get_multi_by_owner(
    db: AsyncSession, *, owner_id: int, skip: int = 0, limit: int = 100
) -> List[ProcessingJob]:
    result = await db.execute(
        select(ProcessingJob)
        .filter(ProcessingJob.owner_id == owner_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def update_job(
    db: AsyncSession, *, db_obj: ProcessingJob, obj_in: ProcessingJobUpdate
) -> ProcessingJob:
    update_data = obj_in.dict(exclude_unset=True)
    for field in update_data:
        if hasattr(db_obj, field):
            setattr(db_obj, field, update_data[field])
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

async def remove_job(db: AsyncSession, *, job_id: int, owner_id: int) -> Optional[ProcessingJob]:
    result = await db.execute(
        select(ProcessingJob).filter(ProcessingJob.id == job_id, ProcessingJob.owner_id == owner_id)
    )
    job = result.scalars().first()
    if job:
        await db.delete(job)
        await db.commit()
    return job
