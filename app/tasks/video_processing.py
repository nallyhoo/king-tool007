
from app.core.celery_app import celery_app
from app.services.ffmpeg_wrapper import FFmpegWrapper
from app.tasks.video_tasks import DBTask
from app.services import processing_job_service
from app.schemas.processing_job import ProcessingJobUpdate
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@celery_app.task(base=DBTask, name="video.process", bind=True)
def video_process(self, job_id: int):
    job = processing_job_service.get_sync(self.db, job_id=job_id)
    if not job:
        logger.error(f"Processing job with ID {job_id} not found.")
        return

    # Update status to processing
    processing_job_service.update_sync(
        self.db, db_obj=job, obj_in=ProcessingJobUpdate(status="processing")
    )

    try:
        wrapper = FFmpegWrapper(task=self, job=job, db=self.db)
        operation = job.operation
        input_file = job.input_file
        
        # In a real app, you would get kwargs from the job model
        kwargs = {}

        # Operation handlers
        if operation == "convert_format":
            output_file = wrapper.convert_format(input_file, **kwargs)
        elif operation == "change_resolution":
            output_file = wrapper.change_resolution(input_file, **kwargs)
        elif operation == "trim_video":
            output_file = wrapper.trim_video(input_file, **kwargs)
        elif operation == "extract_audio":
            output_file = wrapper.extract_audio(input_file, **kwargs)
        elif operation == "generate_thumbnails":
            output_file = wrapper.generate_thumbnails(input_file, **kwargs)
        elif operation == "merge_videos":
            output_file = wrapper.merge_videos(input_file, **kwargs)
        elif operation == "add_watermark":
            output_file = wrapper.add_watermark(input_file, **kwargs)
        elif operation == "compress_video":
            output_file = wrapper.compress_video(input_file, **kwargs)
        else:
            raise ValueError(f"Unsupported operation: {operation}")

        # Update job with completed status and output file
        update_data = ProcessingJobUpdate(status="completed", output_file=output_file, progress=100)
        processing_job_service.update_sync(self.db, db_obj=job, obj_in=update_data)

        return {"status": "completed", "output_file": output_file}

    except Exception as exc:
        logger.error(f"Task {self.request.id} failed: {exc}")
        # Update job with failed status and error message
        update_data = ProcessingJobUpdate(status="failed", error_message=str(exc))
        processing_job_service.update_sync(self.db, db_obj=job, obj_in=update_data)
        raise self.retry(exc=exc, countdown=60, max_retries=3)
