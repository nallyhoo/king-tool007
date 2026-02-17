
import unittest
import os
import asyncio
from services.ffmpeg_service import FFmpegService

class TestFFmpegService(unittest.TestCase):

    def setUp(self):
        self.service = FFmpegService(temp_dir='test_temp')
        self.loop = asyncio.get_event_loop()

        # Create a dummy video file for testing
        self.test_video_path = os.path.join(self.service.temp_dir, 'test_video.mp4')
        self.create_dummy_video(self.test_video_path)

    def tearDown(self):
        # Clean up temporary files
        for f in os.listdir(self.service.temp_dir):
            os.remove(os.path.join(self.service.temp_dir, f))
        os.rmdir(self.service.temp_dir)

    def create_dummy_video(self, path):
        # This is a placeholder for creating a real dummy video file.
        # For a real test suite, you would use ffmpeg to generate a short test video.
        with open(path, 'w') as f:
            f.write("dummy video data")

    def test_convert_format(self):
        async def run_test():
            output_path = await self.service.convert_format(self.test_video_path, 'mov')
            self.assertTrue(os.path.exists(output_path))
            self.assertTrue(output_path.endswith('.mov'))
        self.loop.run_until_complete(run_test())

    def test_change_resolution(self):
        async def run_test():
            output_path = await self.service.change_resolution(self.test_video_path, 1280, 720)
            self.assertTrue(os.path.exists(output_path))
        self.loop.run_until_complete(run_test())

    def test_trim_video(self):
        async def run_test():
            output_path = await self.service.trim_video(self.test_video_path, '00:00:01', '00:00:03')
            self.assertTrue(os.path.exists(output_path))
        self.loop.run_until_complete(run_test())

    def test_extract_audio(self):
        async def run_test():
            output_path = await self.service.extract_audio(self.test_video_path)
            self.assertTrue(os.path.exists(output_path))
            self.assertTrue(output_path.endswith('.mp3'))
        self.loop.run_until_complete(run_test())
        
    def test_add_text_overlay(self):
        async def run_test():
            output_path = await self.service.add_text_overlay(self.test_video_path, "Test Text")
            self.assertTrue(os.path.exists(output_path))
        self.loop.run_until_complete(run_test())
        
    def test_extract_metadata(self):
        metadata = self.service.extract_metadata(self.test_video_path)
        self.assertIn('format', metadata)

if __name__ == '__main__':
    unittest.main()
