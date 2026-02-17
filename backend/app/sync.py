
from app.db import SessionLocal
from app.models import Video
from app.search import index_video

def main():
    db = SessionLocal()
    for video in db.query(Video).all():
        index_video(video)
    db.close()

if __name__ == "__main__":
    main()
