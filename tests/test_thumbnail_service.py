
import unittest
import os
import asyncio
from services.thumbnail_service import ThumbnailService

class TestThumbnailService(unittest.TestCase):

    def setUp(self):
        self.service = ThumbnailService(storage_dir='test_thumbnails', temp_dir='test_temp')
        self.loop = asyncio.get_event_loop()

        # Create a dummy video file for testing
        self.test_video_path = os.path.join(self.service.temp_dir, 'test_video.mp4')
        self.create_dummy_video(self.test_video_path)

    def tearDown(self):
        # Clean up temporary and storage files
        for d in [self.service.temp_dir, self.service.storage_dir]:
            if os.path.exists(d):
                for f in os.listdir(d):
                    os.remove(os.path.join(d, f))
                os.rmdir(d)

    def create_dummy_video(self, path):
        # Placeholder for creating a real dummy video file.
        # In a real test suite, you would use ffmpeg to generate a short test video.
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write("dummy video data")

    def test_extract_single_thumbnail(self):
        async def run_test():
            output_path = await self.service.extract_single_thumbnail(self.test_video_path, timestamp=1)
            self.assertTrue(os.path.exists(output_path))
            self.assertTrue(output_path.endswith('.jpg'))
        self.loop.run_until_complete(run_test())

    def test_generate_thumbnail_strip(self):
        async def run_test():
            output_path = await self.service.generate_thumbnail_strip(self.test_video_path, interval=5)
            self.assertTrue(os.path.exists(output_path))
        self.loop.run_until_complete(run_test())

    def test_create_animated_preview(self):
        async def run_test():
            output_path = await self.service.create_animated_preview(self.test_video_path, duration=2)
            self.assertTrue(os.path.exists(output_path))
            self.assertTrue(output_path.endswith('.gif'))
        self.loop.run_until_complete(run_test())
        
    def test_batch_generation(self):
        async def run_test():
            video_paths = [self.test_video_path] * 3
            results = await self.service.batch_generate_thumbnails(video_paths, task_type='single', timestamp=2)
            self.assertEqual(len(results), 3)
            for r in results:
                self.assertTrue(os.path.exists(r))
        self.loop.run_until_complete(run_test())

if __name__ == '__main__':
    unittest.main()
