
from typing import List, Optional, Tuple
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.download import Download
from app.schemas.download import DownloadCreate, DownloadStatus, DownloadUpdate, Platform

# Synchronous functions for Celery worker
def get_sync(db: Session, download_id: int) -> Optional[Download]:
    return db.query(Download).filter(Download.id == download_id).first()

def update_sync(db: Session, *, db_obj: Download, obj_in: DownloadUpdate) -> Download:
    update_data = obj_in.dict(exclude_unset=True)
    for field in update_data:
        if hasattr(db_obj, field):
            setattr(db_obj, field, update_data[field])
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

# Asynchronous functions for FastAPI app
async def create_download(
    db: AsyncSession, *, obj_in: DownloadCreate, owner_id: int
) -> Download:
    db_obj = Download(**obj_in.dict(), owner_id=owner_id)
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

async def create_multi_downloads(
    db: AsyncSession, *, obj_in: List[DownloadCreate], owner_id: int
) -> List[Download]:
    db_objs = [Download(**item.dict(), owner_id=owner_id) for item in obj_in]
    db.add_all(db_objs)
    await db.commit()
    for db_obj in db_objs:
        await db.refresh(db_obj)
    return db_objs


async def get_multi_by_owner(
    db: AsyncSession, *, owner_id: int, skip: int = 0, limit: int = 100
) -> List[Download]:
    result = await db.execute(
        select(Download)
        .filter(Download.owner_id == owner_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def get_multi_by_owner_with_filters(
    db: AsyncSession,
    *,
    owner_id: int,
    skip: int = 0,
    limit: int = 100,
    status: Optional[DownloadStatus] = None,
    platform: Optional[Platform] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
) -> Tuple[int, List[Download]]:
    query = select(Download).filter(Download.owner_id == owner_id)
    count_query = select(func.count()).select_from(Download).filter(Download.owner_id == owner_id)

    if status:
        query = query.filter(Download.status == status)
        count_query = count_query.filter(Download.status == status)
    if platform:
        query = query.filter(Download.url.contains(platform.value))
        count_query = count_query.filter(Download.url.contains(platform.value))
    if start_date:
        query = query.filter(Download.created_at >= start_date)
        count_query = count_query.filter(Download.created_at >= start_date)
    if end_date:
        query = query.filter(Download.created_at <= end_date)
        count_query = count_query.filter(Download.created_at <= end_date)
    
    sort_column = getattr(Download, sort_by)
    if sort_order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    total_count_result = await db.execute(count_query)
    total_count = total_count_result.scalar_one()

    result = await db.execute(query.offset(skip).limit(limit))
    downloads = result.scalars().all()

    return total_count, downloads


async def get_download(
    db: AsyncSession, *, download_id: int, owner_id: int
) -> Optional[Download]:
    result = await db.execute(
        select(Download).filter(Download.id == download_id, Download.owner_id == owner_id)
    )
    return result.scalars().first()


async def update_download(
    db: AsyncSession, *, db_obj: Download, obj_in: DownloadUpdate
) -> Download:
    update_data = obj_in.dict(exclude_unset=True)
    for field in update_data:
        if hasattr(db_obj, field):
            setattr(db_obj, field, update_data[field])
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def remove_download(db: AsyncSession, *, download_id: int, owner_id: int) -> Optional[Download]:
    result = await db.execute(
        select(Download).filter(Download.id == download_id, Download.owner_id == owner_id)
    )
    download = result.scalars().first()
    if download:
        await db.delete(download)
        await db.commit()
    return download
