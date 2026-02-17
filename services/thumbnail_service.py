
import asyncio
import ffmpeg
import os

class ThumbnailService:
    def __init__(self, storage_dir='thumbnails', temp_dir='temp'):
        self.storage_dir = storage_dir
        self.temp_dir = temp_dir
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)

    def get_video_duration(self, file_path):
        try:
            probe = ffmpeg.probe(file_path)
            return float(probe['format']['duration'])
        except (ffmpeg.Error, KeyError) as e:
            raise RuntimeError(f"Could not get video duration: {e}")

    async def run_ffmpeg(self, stream, output_path):
        process = await asyncio.create_subprocess_exec(
            *ffmpeg.get_args(stream),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        if process.returncode != 0:
            raise RuntimeError(f"FFmpeg error: {stderr.decode()}")
        return output_path
    
    def get_output_path(self, input_path, suffix, extension):
        basename = os.path.basename(input_path)
        name, _ = os.path.splitext(basename)
        return os.path.join(self.storage_dir, f"{name}_{suffix}.{extension}")

    # 1. Extract single thumbnail
    async def extract_single_thumbnail(self, file_path, timestamp=None, percentage=None, resolution='320x240', quality=5, output_format='jpg'):
        if percentage:
            duration = self.get_video_duration(file_path)
            timestamp = (percentage / 100) * duration
        
        if timestamp is None:
            # Smart selection placeholder: just take from the middle
            duration = self.get_video_duration(file_path)
            timestamp = duration / 2

        width, height = map(int, resolution.split('x'))

        output_path = self.get_output_path(file_path, f"thumb_{timestamp:.2f}s", output_format)
        
        stream = ffmpeg.input(file_path, ss=timestamp)
        stream = ffmpeg.filter(stream, 'scale', width, -1)
        stream = ffmpeg.output(stream, output_path, vframes=1, q=quality)
        
        return await self.run_ffmpeg(stream, output_path)

    # 2. Generate thumbnail strip
    async def generate_thumbnail_strip(self, file_path, interval=10, resolution='160x120', grid_layout='4x4', output_format='jpg'):
        width, height = map(int, resolution.split('x'))
        grid_cols, grid_rows = map(int, grid_layout.split('x'))
        
        output_path = self.get_output_path(file_path, f"strip_{grid_layout}", output_format)

        stream = ffmpeg.input(file_path)
        stream = ffmpeg.filter(stream, 'fps', fps=1/interval)
        stream = ffmpeg.filter(stream, 'scale', width, -1)
        stream = ffmpeg.filter(stream, 'tile', layout=f"{grid_cols}x{grid_rows}")
        stream = ffmpeg.output(stream, output_path, vframes=1)

        return await self.run_ffmpeg(stream, output_path)

    # 3. Create animated preview (GIF)
    async def create_animated_preview(self, file_path, start_time=0, duration=5, resolution='320x240', fps=10, quality=5):
        width, height = map(int, resolution.split('x'))
        output_path = self.get_output_path(file_path, f"preview_{start_time}s_{duration}s", 'gif')
        
        stream = ffmpeg.input(file_path, ss=start_time, t=duration)
        stream = ffmpeg.filter(stream, 'scale', width, -1)
        
        # Use palettegen and paletteuse filters for optimized GIF quality
        split = ffmpeg.filter(stream, 'split')
        palette = ffmpeg.filter(split[1], 'palettegen')
        final_stream = ffmpeg.filter([split[0], palette], 'paletteuse')
        
        final_stream = ffmpeg.output(final_stream, output_path, r=fps)

        return await self.run_ffmpeg(final_stream, output_path)
        
    # 4. Batch generation
    async def batch_generate_thumbnails(self, file_paths, task_type='single', **kwargs):
        tasks = []
        if task_type == 'single':
            for path in file_paths:
                tasks.append(self.extract_single_thumbnail(path, **kwargs))
        elif task_type == 'strip':
            for path in file_paths:
                tasks.append(self.generate_thumbnail_strip(path, **kwargs))
        elif task_type == 'animated':
             for path in file_paths:
                tasks.append(self.create_animated_preview(path, **kwargs))
        else:
            raise ValueError("Invalid task type. Choose 'single', 'strip', or 'animated'.")

        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results
