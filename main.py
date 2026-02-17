from flask import Flask, jsonify, send_from_directory
from flask_socketio import SocketIO

app = Flask(__name__, static_folder='frontend/dist')
socketio = SocketIO(app, async_mode='eventlet')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

@app.route('/api/videos')
def get_videos():
    mock_videos = [
      {
        'id': '1',
        'title': 'Big Buck Bunny',
        'thumbnailUrl': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Big_Buck_Bunny_thumbnail_vlc.png/1200px-Big_Buck_Bunny_thumbnail_vlc.png',
        'creator': 'Blender Foundation',
        'uploadDate': '2024-05-20',
        'downloadDate': '2024-05-21',
        'duration': 596,
        'fileSize': 150 * 1024 * 1024,
        'quality': '1080p',
        'views': 1234567,
        'tags': ['animation', 'short film', 'blender'],
        'description': 'A short computer-animated film by the Blender Institute, part of the Blender Foundation.'
      },
      {
        'id': '2',
        'title': 'Sintel',
        'thumbnailUrl': 'https://i.ytimg.com/vi/eRsGyueVLvQ/maxresdefault.jpg',
        'creator': 'Blender Foundation',
        'uploadDate': '2010-09-27',
        'downloadDate': '2024-05-20',
        'duration': 888,
        'fileSize': 250 * 1024 * 1024,
        'quality': '1080p',
        'views': 543210,
        'tags': ['animation', 'fantasy', 'short film'],
        'description': 'A short computer animated film by the Blender Institute, part of the Blender Foundation.'
      },
        {
        'id': '3',
        'title': 'Elephants Dream',
        'thumbnailUrl': 'https://i.ytimg.com/vi/dv_k1mS9I_w/maxresdefault.jpg',
        'creator': 'Blender Foundation',
        'uploadDate': '2006-03-24',
        'downloadDate': '2024-05-19',
        'duration': 653,
        'fileSize': 180 * 1024 * 1024,
        'quality': '720p',
        'views': 987654,
        'tags': ['animation', 'sci-fi', 'short film'],
        'description': 'The first open movie, created by the Blender Foundation.'
      }
    ]
    return jsonify(mock_videos)

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, debug=True)
