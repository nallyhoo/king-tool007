
from app.core.celery_app import celery_app
from app.services.yt_dlp_wrapper import YTDLWrapper
from app.services import download_service
from app.core.database import SessionLocal
from app.schemas.download import DownloadUpdate, DownloadStatus
from sqlalchemy.orm import Session

class DBTask(celery_app.Task):
    _db: Session = None

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        if self._db is not None:
            self._db.close()

    @property
    def db(self) -> Session:
        if self._db is None:
            self._db = SessionLocal()
        return self._db


@celery_app.task(base=DBTask, name="video.download", bind=True)
def video_download(self, download_id: int, url: str):
    try:
        # 1. Update status to DOWNLOADING
        download_obj = download_service.get_sync(self.db, download_id)
        if not download_obj:
            raise ValueError(f"Download with ID {download_id} not found.")

        download_service.update_sync(self.db, db_obj=download_obj, obj_in=DownloadUpdate(status=DownloadStatus.DOWNLOADING))

        # 2. Download video using the wrapper
        wrapper = YTDLWrapper(task=self, download_id=download_id)
        file_path = wrapper.download(url)

        # 3. Validate downloaded file (basic check)
        import os
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            raise ValueError("Downloaded file is invalid or empty.")

        # 4. Extract metadata and save to storage (placeholder)

        # 5. Generate thumbnails (yt-dlp already did this)

        # 6. Update database on completion
        download_service.update_sync(self.db, db_obj=download_obj, obj_in=DownloadUpdate(status=DownloadStatus.COMPLETED, file_path=file_path))

        return {"status": "completed", "file_path": file_path}

    except Exception as exc:
        # On failure, update the status to FAILED
        download_obj = download_service.get_sync(self.db, download_id)
        if download_obj:
            download_service.update_sync(self.db, db_obj=download_obj, obj_in=DownloadUpdate(status=DownloadStatus.FAILED, error_message=str(exc)))
        # Retry the task
        raise self.retry(exc=exc, countdown=60, max_retries=3)
