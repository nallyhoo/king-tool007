
import ffmpeg
import os
import subprocess
import re
from celery.utils.log import get_task_logger
from app.schemas.processing_job import ProcessingJobUpdate
from app.services import processing_job_service

logger = get_task_logger(__name__)

class FFmpegWrapper:
    def __init__(self, task, job, db):
        self.task = task
        self.job = job
        self.db = db

    def _get_output_path(self, input_file, suffix, extension):
        base, _ = os.path.splitext(input_file)
        return f"{base}_{suffix}.{extension}"

    def _run_ffmpeg(self, stream_spec, input_file):
        probe = ffmpeg.probe(input_file)
        total_duration = float(probe['format']['duration'])

        args = ffmpeg.get_args(stream_spec)
        cmd = ['ffmpeg'] + args
        
        process = subprocess.Popen(cmd, stderr=subprocess.PIPE, universal_newlines=True, encoding='utf-8')

        for line in process.stderr:
            if 'frame=' in line:
                progress_data = self._parse_progress(line, total_duration)
                if progress_data:
                    # Update Celery task state for real-time frontend updates
                    self.task.update_state(state='PROGRESS', meta=progress_data)
                    
                    # Update job progress in the database
                    update_data = ProcessingJobUpdate(progress=progress_data['progress'])
                    processing_job_service.update_sync(self.db, db_obj=self.job, obj_in=update_data)


        process.wait()
        if process.returncode != 0:
            # The error will be caught by the main task exception handler
            raise RuntimeError(f"FFmpeg command failed with exit code {process.returncode}")

    def _parse_progress(self, line, total_duration):
        time_match = re.search(r"time=(\d{2}):(\d{2}):(\d{2})\.(\d{2})", line)
        if time_match:
            hours = int(time_match.group(1))
            minutes = int(time_match.group(2))
            seconds = int(time_match.group(3))
            milliseconds = int(time_match.group(4))
            current_time_sec = hours * 3600 + minutes * 60 + seconds + milliseconds / 100
            
            if total_duration > 0:
                progress = (current_time_sec / total_duration) * 100
            else:
                progress = 0

            return {
                'progress': round(min(progress, 100), 2),
                'current_time': current_time_sec,
                'total_duration': total_duration
            }
        return None

    def convert_format(self, input_file, output_format='mp4', quality='23'):
        output_file = self._get_output_path(input_file, f"converted_{output_format}", output_format)
        stream = ffmpeg.input(input_file)
        stream = ffmpeg.output(stream, output_file, crf=quality)
        self._run_ffmpeg(stream, input_file)
        return output_file

    def change_resolution(self, input_file, width, height, quality='23'):
        output_file = self._get_output_path(input_file, f"{width}x{height}", 'mp4')
        stream = ffmpeg.input(input_file)
        stream = ffmpeg.filter(stream, 'scale', width, height)
        stream = ffmpeg.output(stream, output_file, crf=quality)
        self._run_ffmpeg(stream, input_file)
        return output_file

    def trim_video(self, input_file, start_time, end_time):
        output_file = self._get_output_path(input_file, "trimmed", 'mp4')
        in_stream = ffmpeg.input(input_file)
        trimmed_stream = in_stream.trim(start=start_time, end=end_time).setpts('PTS-STARTPTS')
        audio_stream = in_stream.audio.filter('atrim', start=start_time, end=end_time).filter('asetpts', 'PTS-STARTPTS')
        stream = ffmpeg.concat(trimmed_stream, audio_stream, v=1, a=1).output(output_file)
        self._run_ffmpeg(stream, input_file)
        return output_file

    def extract_audio(self, input_file, audio_format='mp3'):
        output_file = self._get_output_path(input_file, "audio", audio_format)
        stream = ffmpeg.input(input_file).audio
        stream = ffmpeg.output(stream, output_file)
        self._run_ffmpeg(stream, input_file)
        return output_file

    def generate_thumbnails(self, input_file, interval, width=128):
        output_path = self._get_output_path(input_file, "thumbnails", "") + "/thumb_%04d.jpg"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        stream = ffmpeg.input(input_file)
        stream = ffmpeg.filter(stream, 'fps', fps=1/interval)
        stream = ffmpeg.filter(stream, 'scale', width, -1)
        stream = ffmpeg.output(stream, output_path, start_number=0)
        self._run_ffmpeg(stream, input_file)
        return os.path.dirname(output_path)
    
    def merge_videos(self, input_files, output_file):
        with open("concat_list.txt", "w") as f:
            for file in input_files:
                f.write(f"file '{file}'\n")
        
        stream = ffmpeg.input("concat_list.txt", format='concat', safe=0)
        stream = ffmpeg.output(stream, output_file, c='copy')
        self._run_ffmpeg(stream, input_files[0])
        os.remove("concat_list.txt")
        return output_file

    def add_watermark(self, input_file, watermark_file, position="10:10"):
        output_file = self._get_output_path(input_file, "watermarked", 'mp4')
        main_stream = ffmpeg.input(input_file)
        watermark_stream = ffmpeg.input(watermark_file)
        stream = ffmpeg.overlay(main_stream, watermark_stream, x=position.split(':')[0], y=position.split(':')[1])
        stream = ffmpeg.output(stream, output_file)
        self._run_ffmpeg(stream, input_file)
        return output_file

    def compress_video(self, input_file, quality='28'):
        return self.convert_format(input_file, quality=quality)
