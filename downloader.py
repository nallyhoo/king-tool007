
import uuid
import yt_dlp
from threading import Thread
from flask_socketio import SocketIO

class DownloadTask:
    def __init__(self, url: str, options: dict, socketio: SocketIO):
        self.id = str(uuid.uuid4())
        self.url = url
        self.options = options
        self.socketio = socketio
        self.status = 'queued'
        self.progress = {
            'id': self.id,
            'status': 'queued',
            'percentage': 0,
            'eta': 'N/A',
            'speed': 'N/A',
            'filename': 'N/A',
            'total_bytes': 0,
            'downloaded_bytes': 0
        }

    def _progress_hook(self, d):
        self.status = d['status']
        if d['status'] == 'downloading':
            self.progress['status'] = 'downloading'
            self.progress['percentage'] = d['_percent_str']
            self.progress['eta'] = d['_eta_str']
            self.progress['speed'] = d['_speed_str']
            self.progress['filename'] = d.get('filename')
            self.progress['total_bytes'] = d.get('total_bytes') or d.get('total_bytes_estimate')
            self.progress['downloaded_bytes'] = d.get('downloaded_bytes')
            self.socketio.emit('download_progress', self.progress)
        elif d['status'] == 'finished':
            self.progress['status'] = 'completed'
            self.progress['percentage'] = '100%'
            self.socketio.emit('download_progress', self.progress)
        elif d['status'] == 'error':
            self.progress['status'] = 'failed'
            self.socketio.emit('download_progress', self.progress)

    def run(self):
        def _execute():
            try:
                ydl_opts = {
                    'progress_hooks': [self._progress_hook],
                    'outtmpl': 'downloads/%(title)s.%(ext)s',
                    **self.options
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([self.url])
                self.status = 'completed'
            except Exception as e:
                self.status = 'failed'
                print(f"Error downloading {self.url}: {e}")
                self.progress['status'] = 'failed'
                self.socketio.emit('download_progress', self.progress)

        thread = Thread(target=_execute)
        thread.start()

