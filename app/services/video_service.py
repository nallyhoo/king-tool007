
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.video import Video
from app.schemas.video import VideoCreate, VideoUpdate


async def create_video(
    db: AsyncSession, *, obj_in: VideoCreate, owner_id: int
) -> Video:
    db_obj = Video(**obj_in.dict(), owner_id=owner_id)
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def get_multi_by_owner(
    db: AsyncSession, *, owner_id: int, skip: int = 0, limit: int = 100
) -> List[Video]:
    result = await db.execute(
        select(Video).filter(Video.owner_id == owner_id).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def get_video(
    db: AsyncSession, *, video_id: int, owner_id: int
) -> Optional[Video]:
    result = await db.execute(
        select(Video).filter(Video.id == video_id, Video.owner_id == owner_id)
    )
    return result.scalars().first()


async def update_video(
    db: AsyncSession, *, db_obj: Video, obj_in: VideoUpdate
) -> Video:
    update_data = obj_in.dict(exclude_unset=True)
    for field in update_data:
        if hasattr(db_obj, field):
            setattr(db_obj, field, update_data[field])
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def remove_video(db: AsyncSession, *, video_id: int, owner_id: int) -> Optional[Video]:
    result = await db.execute(
        select(Video).filter(Video.id == video_id, Video.owner_id == owner_id)
    )
    video = result.scalars().first()
    if video:
        await db.delete(video)
        await db.commit()
    return video
