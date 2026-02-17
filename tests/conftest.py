
import pytest
from fastapi.testclient import TestClient
import asyncio
import os

# Fixture for the event loop
@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for our test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

# Fixture to create a dummy video file
@pytest.fixture(scope="module")
def dummy_video_file():
    """Create a dummy video file for testing purposes."""
    temp_dir = "test_temp_videos"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
    file_path = os.path.join(temp_dir, "test_video.mp4")
    
    # In a real scenario, you might generate a small, actual video file here
    # For now, a simple text file will suffice for path manipulation tests
    with open(file_path, "w") as f:
        f.write("dummy video data")
        
    yield file_path
    
    # Teardown: remove the file and directory
    os.remove(file_path)
    os.rmdir(temp_dir)

# Mock yt-dlp response fixture
@pytest.fixture
def mock_yt_dlp_info():
    """Provides a mock dictionary of a yt-dlp response."""
    return {
        "id": "test_video_id",
        "title": "Test Video Title",
        "creator": "Test Creator",
        "upload_date": "20240101",
        "duration": 60,
        "view_count": 1000,
        "tags": ["test", "video"],
        "description": "A test video description.",
        "thumbnail": "http://example.com/thumbnail.jpg",
        "filesize_approx": 10000000
    }
