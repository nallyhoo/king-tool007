
import yt_dlp
import redis
import json

class YTDLWrapper:
    def __init__(self, task, download_id, redis_url='redis://localhost:6379/0'):
        self.task = task
        self.download_id = download_id
        self.redis = redis.from_url(redis_url)

    def _progress_hook(self, d):
        if d['status'] == 'downloading':
            progress_data = {
                'progress': d.get('_percent_str', '0%').replace('%', ''),
                'speed': d.get('speed', 0),
                'eta': d.get('eta', 0),
                'total_bytes': d.get('total_bytes', 0),
                'downloaded_bytes': d.get('downloaded_bytes', 0),
            }
            self.task.update_state(state='PROGRESS', meta=progress_data)
            # Also publish to Redis for real-time updates
            self.redis.publish(f"download:{self.download_id}:progress", json.dumps(progress_data))

        if d['status'] == 'finished':
            self.task.update_state(state='POST_PROCESSING', meta={'progress': 100})

    def download(self, url: str, download_path: str = '/app/downloads'):
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': f'{download_path}/%(id)s.%(ext)s',
            'progress_hooks': [self._progress_hook],
            'writethumbnail': True,
            'writeinfojson': True,
            'subtitleslangs': ['en'],
            'writesubtitles': True,
            'noplaylist': True,
            # For resuming partial downloads
            'continuedl': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                return ydl.prepare_filename(info)
        except Exception as e:
            # Log the full error
            print(f"[YTDL-ERROR] Failed to download {url}: {e}")
            raise
