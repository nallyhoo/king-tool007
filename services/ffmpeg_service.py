
import asyncio
import ffmpeg
import os
import math
import json

class FFmpegService:
    def __init__(self, temp_dir='temp'):
        self.temp_dir = temp_dir
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)

    async def run_ffmpeg(self, stream, output_path, progress_callback=None):
        process = await asyncio.create_subprocess_exec(
            *ffmpeg.get_args(stream),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        # Implement progress tracking here

        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            raise RuntimeError(f"FFmpeg error: {stderr.decode()}")

        return output_path

    def get_output_path(self, input_path, suffix, extension):
        basename = os.path.basename(input_path)
        name, _ = os.path.splitext(basename)
        return os.path.join(self.temp_dir, f"{name}_{suffix}.{extension}")

    # 1. Format Conversion
    async def convert_format(self, file_path, output_format, preset='web_optimized', codec_options=None, progress_callback=None):
        output_path = self.get_output_path(file_path, f"converted_{preset}", output_format)
        stream = ffmpeg.input(file_path)

        if preset == 'web_optimized':
            stream = ffmpeg.output(stream, output_path, vcodec='libx264', acodec='aac', preset='fast', movflags='faststart')
        elif preset == 'high_quality':
            stream = ffmpeg.output(stream, output_path, vcodec='libx264', acodec='aac', preset='medium', crf=18)
        elif preset == 'small_size':
            stream = ffmpeg.output(stream, output_path, vcodec='libx264', acodec='aac', preset='slow', crf=28)
        else:
            stream = ffmpeg.output(stream, output_path)
            
        if codec_options:
            stream = ffmpeg.output(stream, output_path, **codec_options)

        return await self.run_ffmpeg(stream, output_path, progress_callback)

    # 2. Resolution/Quality Change
    async def change_resolution(self, file_path, width, height, progress_callback=None):
        output_path = self.get_output_path(file_path, f"{width}x{height}", os.path.splitext(file_path)[1][1:])
        stream = ffmpeg.input(file_path)
        stream = ffmpeg.filter(stream, 'scale', width, height)
        stream = ffmpeg.output(stream, output_path)
        return await self.run_ffmpeg(stream, output_path, progress_callback)

    async def change_quality(self, file_path, crf=23, progress_callback=None):
        output_path = self.get_output_path(file_path, f"crf{crf}", os.path.splitext(file_path)[1][1:])
        stream = ffmpeg.input(file_path)
        stream = ffmpeg.output(stream, output_path, crf=crf)
        return await self.run_ffmpeg(stream, output_path, progress_callback)
        
    # 3. Video Editing
    async def trim_video(self, file_path, start_time, end_time, progress_callback=None):
        output_path = self.get_output_path(file_path, f"trimmed_{start_time}_{end_time}", os.path.splitext(file_path)[1][1:])
        stream = ffmpeg.input(file_path, ss=start_time)
        stream = ffmpeg.output(stream, output_path, to=end_time)
        return await self.run_ffmpeg(stream, output_path, progress_callback)

    async def split_video(self, file_path, segment_duration, progress_callback=None):
        output_pattern = self.get_output_path(file_path, "segment_%03d", os.path.splitext(file_path)[1][1:])
        stream = ffmpeg.input(file_path)
        stream = ffmpeg.output(stream, output_pattern, f='segment', segment_time=segment_duration, reset_timestamps=1)
        
        process = await asyncio.create_subprocess_exec(
            *ffmpeg.get_args(stream),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        if process.returncode != 0:
            raise RuntimeError(f"FFmpeg error: {stderr.decode()}")

        output_dir = os.path.dirname(output_pattern)
        base_pattern = os.path.basename(output_pattern).replace('%03d', '')
        created_files = [os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.startswith(base_pattern.split('.')[0]) and f.endswith('.' + base_pattern.split('.')[1])]
        return sorted(created_files)

    async def merge_videos(self, file_paths, progress_callback=None):
        if not file_paths:
            raise ValueError("No file paths provided for merging.")
        
        output_path = self.get_output_path(file_paths[0], "merged", os.path.splitext(file_paths[0])[1][1:])
        
        input_streams = [ffmpeg.input(f) for f in file_paths]
        
        video_streams = [s.video for s in input_streams]
        audio_streams = [s.audio for s in input_streams]
        
        merged_video = ffmpeg.concat(*video_streams, v=1)
        merged_audio = ffmpeg.concat(*audio_streams, a=1)
        
        stream = ffmpeg.output(merged_video, merged_audio, output_path)
        
        return await self.run_ffmpeg(stream, output_path, progress_callback)

    async def crop_video(self, file_path, x, y, width, height, progress_callback=None):
        output_path = self.get_output_path(file_path, f"cropped_{width}x{height}", os.path.splitext(file_path)[1][1:])
        stream = ffmpeg.input(file_path)
        stream = ffmpeg.filter(stream, 'crop', w=width, h=height, x=x, y=y)
        stream = ffmpeg.output(stream, output_path)
        return await self.run_ffmpeg(stream, output_path, progress_callback)

    # 4. Audio Operations
    async def extract_audio(self, file_path, output_format='mp3', progress_callback=None):
        output_path = self.get_output_path(file_path, "audio", output_format)
        stream = ffmpeg.input(file_path)
        acodec = 'libmp3lame' if output_format == 'mp3' else None
        stream = ffmpeg.output(stream.audio, output_path, acodec=acodec)
        return await self.run_ffmpeg(stream, output_path, progress_callback)

    async def remove_audio(self, file_path, progress_callback=None):
        output_path = self.get_output_path(file_path, "no_audio", os.path.splitext(file_path)[1][1:])
        stream = ffmpeg.input(file_path)
        stream = ffmpeg.output(stream.video, output_path, vcodec='copy', an=None)
        return await self.run_ffmpeg(stream, output_path, progress_callback)

    async def replace_audio(self, video_path, audio_path, progress_callback=None):
        output_path = self.get_output_path(video_path, "new_audio", os.path.splitext(video_path)[1][1:])
        video_stream = ffmpeg.input(video_path).video
        audio_stream = ffmpeg.input(audio_path).audio
        stream = ffmpeg.output(video_stream, audio_stream, output_path, vcodec='copy', acodec='aac', shortest=None)
        return await self.run_ffmpeg(stream, output_path, progress_callback)

    async def adjust_volume(self, file_path, volume_factor, progress_callback=None):
        output_path = self.get_output_path(file_path, f"volume_{volume_factor}x", os.path.splitext(file_path)[1][1:])
        stream = ffmpeg.input(file_path)
        stream = ffmpeg.filter(stream, 'volume', str(volume_factor))
        stream = ffmpeg.output(stream, output_path)
        return await self.run_ffmpeg(stream, output_path, progress_callback)

    # 5. Effects & Filters
    async def add_watermark(self, file_path, watermark_path, position="main_w-overlay_w-10:10", progress_callback=None):
        output_path = self.get_output_path(file_path, "watermarked", os.path.splitext(file_path)[1][1:])
        main_video = ffmpeg.input(file_path)
        watermark = ffmpeg.input(watermark_path)
        stream = ffmpeg.overlay(main_video, watermark, x=position.split(':')[0], y=position.split(':')[1])
        stream = ffmpeg.output(stream, output_path)
        return await self.run_ffmpeg(stream, output_path, progress_callback)

    async def add_text_overlay(self, file_path, text, x="(w-text_w)/2", y="(h-text_h)/2", fontfile=None, fontsize=24, fontcolor="white", progress_callback=None):
        output_path = self.get_output_path(file_path, "text_overlay", os.path.splitext(file_path)[1][1:])
        stream = ffmpeg.input(file_path)
        drawtext_options = {
            'text': text,
            'x': x,
            'y': y,
            'fontsize': fontsize,
            'fontcolor': fontcolor
        }
        if fontfile:
            drawtext_options['fontfile'] = fontfile
        stream = ffmpeg.drawtext(stream, **drawtext_options)
        stream = ffmpeg.output(stream, output_path)
        return await self.run_ffmpeg(stream, output_path, progress_callback)

    async def adjust_speed(self, file_path, speed_factor, progress_callback=None):
        output_path = self.get_output_path(file_path, f"speed_{speed_factor}x", os.path.splitext(file_path)[1][1:])
        stream = ffmpeg.input(file_path)
        stream = ffmpeg.filter(stream, 'setpts', f'{1/speed_factor}*PTS')
        if 'audio' in ffmpeg.probe(file_path, select_streams='a'):
            audio_stream = stream.audio
            audio_stream = ffmpeg.filter(audio_stream, 'atempo', speed_factor)
            stream = ffmpeg.output(stream.video, audio_stream, output_path)
        else:
            stream = ffmpeg.output(stream.video, output_path)
        return await self.run_ffmpeg(stream, output_path, progress_callback)

    async def rotate_video(self, file_path, angle, progress_callback=None):
        output_path = self.get_output_path(file_path, f"rotated_{angle}", os.path.splitext(file_path)[1][1:])
        stream = ffmpeg.input(file_path)
        if angle == 90:
            stream = ffmpeg.filter(stream, 'transpose', 1)
        elif angle == -90:
            stream = ffmpeg.filter(stream, 'transpose', 2)
        elif angle == 180:
            stream = ffmpeg.filter(stream, 'transpose', 2).filter('transpose', 2)
        else:
            radians = math.radians(angle)
            stream = ffmpeg.filter(stream, 'rotate', str(radians))
        
        stream = ffmpeg.output(stream, output_path)
        return await self.run_ffmpeg(stream, output_path, progress_callback)

    async def flip_video(self, file_path, direction='h', progress_callback=None):
        output_path = self.get_output_path(file_path, f"{direction}flip", os.path.splitext(file_path)[1][1:])
        stream = ffmpeg.input(file_path)
        if direction == 'h':
            stream = ffmpeg.hflip(stream)
        elif direction == 'v':
            stream = ffmpeg.vflip(stream)
        else:
            raise ValueError("Invalid flip direction. Use 'h' for horizontal or 'v' for vertical.")
        
        stream = ffmpeg.output(stream, output_path)
        return await self.run_ffmpeg(stream, output_path, progress_callback)

    async def correct_color(self, file_path, brightness=0, contrast=1, saturation=1, progress_callback=None):
        output_path = self.get_output_path(file_path, "color_corrected", os.path.splitext(file_path)[1][1:])
        stream = ffmpeg.input(file_path)
        stream = ffmpeg.filter(stream, 'eq', brightness=brightness, contrast=contrast, saturation=saturation)
        stream = ffmpeg.output(stream, output_path)
        return await self.run_ffmpeg(stream, output_path, progress_callback)

    # 6. Metadata Operations
    def extract_metadata(self, file_path):
        try:
            probe = ffmpeg.probe(file_path)
            return probe
        except ffmpeg.Error as e:
            raise RuntimeError(f"FFprobe error: {e.stderr.decode()}")

    async def modify_metadata(self, file_path, metadata, progress_callback=None):
        output_path = self.get_output_path(file_path, "metadata_modified", os.path.splitext(file_path)[1][1:])
        stream = ffmpeg.input(file_path)
        stream = ffmpeg.output(stream, output_path, metadata=metadata, codec='copy')
        return await self.run_ffmpeg(stream, output_path, progress_callback)

    async def strip_metadata(self, file_path, progress_callback=None):
        output_path = self.get_output_path(file_path, "metadata_stripped", os.path.splitext(file_path)[1][1:])
        stream = ffmpeg.input(file_path)
        stream = ffmpeg.output(stream, output_path, map_metadata='-1', codec='copy')
        return await self.run_ffmpeg(stream, output_path, progress_callback)
