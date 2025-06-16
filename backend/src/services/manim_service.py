import re
import subprocess
import os
import glob
import logging
import tempfile
import shutil
import uuid
import threading
from pathlib import Path
import time


class ManimVideoProcessor:
    def __init__(self, base_output_dir="output"):
        self.base_output_dir = Path(base_output_dir)
        self.session_id = str(uuid.uuid4())[:8]
        self.temp_dir = None
        self.lock = threading.Lock()
        self.cleanup_files = []

    def __enter__(self):
        # Create temporary directory for this session
        # self.temp_dir = Path(tempfile.mkdtemp(prefix=f"manim_video_{self.session_id}_"))
        self.temp_dir = Path("output_final") / f"manim_video_{self.session_id}"
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()

    def cleanup(self):
        """Clean up all temporary files and directories"""
        try:
            with self.lock:
                # Remove specific files first
                for file_path in self.cleanup_files:
                    try:
                        if os.path.exists(file_path):
                            os.remove(file_path)
                            logging.info(f"Removed temporary file: {file_path}")
                    except Exception as e:
                        logging.warning(f"Failed to remove file {file_path}: {e}")

                # Remove temporary directory
                if self.temp_dir and self.temp_dir.exists():
                    shutil.rmtree(self.temp_dir, ignore_errors=True)
                    logging.info(f"Removed temporary directory: {self.temp_dir}")

        except Exception as e:
            logging.error(f"Error during cleanup: {e}")

    def get_scene_name(self, manim_code):
        """Extract scene class name from Manim code"""
        match = re.search(r"class\s+(\w+)\s*\(\s*Scene\s*\)", manim_code)
        if match:
            return match.group(1)
        raise ValueError("No Scene class found in generated code")

    def ensure_directories(self):
        """Create all necessary output directories"""
        directories = [
            self.base_output_dir / "video",
            self.base_output_dir / "final_video",
            self.base_output_dir / "subtitles",
            self.temp_dir,
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            logging.info(f"Ensured directory exists: {directory}")

    def run_subprocess_safely(self, command, timeout=300):
        """Run subprocess with proper error handling and timeout"""
        try:
            logging.info(f"Running command: {' '.join(command)}")
            result = subprocess.run(
                command, check=True, capture_output=True, text=True, timeout=timeout
            )
            logging.info("Command completed successfully")
            return result
        except subprocess.TimeoutExpired:
            logging.error(f"Command timed out after {timeout} seconds")
            raise Exception(f"Command timed out: {' '.join(command)}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Command failed with exit code {e.returncode}")
            logging.error(f"STDOUT: {e.stdout}")
            logging.error(f"STDERR: {e.stderr}")
            raise Exception(f"Command failed: {' '.join(command)}\nError: {e.stderr}")

    def get_media_duration(self, file_path):
        """Get duration of media file using ffprobe"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Media file not found: {file_path}")

        command = [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(file_path),
        ]

        result = self.run_subprocess_safely(command)
        try:
            return float(result.stdout.strip())
        except ValueError:
            raise Exception(f"Could not parse duration from: {result.stdout}")

    def create_manim_scene(self, manim_code):
        """Create and render Manim scene"""
        logging.info("Creating Manim scene")

        # Clean the code
        manim_code_clean = re.sub(r"```python", "", manim_code)
        manim_code_clean = manim_code_clean.replace("```", "").strip()

        # Create unique script file
        script_file = self.temp_dir / f"generated_video_{self.session_id}.py"
        self.cleanup_files.append(str(script_file))

        with open(script_file, "w") as f:
            f.write(manim_code_clean)

        scene_name = self.get_scene_name(manim_code_clean)
        logging.info(f"Identified scene name: {scene_name}")

        # Render with Manim
        command = ["manim", "-qh", str(script_file), scene_name]
        self.run_subprocess_safely(command)

        # Find the rendered video
        output_pattern = self.base_output_dir / "video" / f"{scene_name}.mp4"
        if not output_pattern.exists():
            # Try alternative locations
            media_dir = Path("media/videos")
            if media_dir.exists():
                for video_file in media_dir.rglob(f"{scene_name}.mp4"):
                    shutil.copy2(video_file, output_pattern)
                    break
            else:
                raise Exception(f"No rendered video found for scene {scene_name}")

        logging.info(f"Manim video created: {output_pattern}")
        return str(output_pattern)

    def extend_video_to_audio_length(self, video_file, audio_duration):
        """Extend video duration to match audio length"""
        video_duration = self.get_media_duration(video_file)

        if audio_duration <= video_duration:
            return video_file

        logging.info(f"Extending video from {video_duration}s to {audio_duration}s")

        extended_video = self.temp_dir / f"extended_video_{self.session_id}.mp4"
        self.cleanup_files.append(str(extended_video))

        # Calculate how many times to loop the video
        loop_count = int(audio_duration / video_duration) + 1

        # Create extended video by looping
        command = [
            "ffmpeg",
            "-y",
            "-stream_loop",
            str(loop_count - 1),
            "-i",
            video_file,
            "-t",
            str(audio_duration),
            "-c",
            "copy",
            str(extended_video),
        ]

        self.run_subprocess_safely(command)
        return str(extended_video)

    def merge_video_audio(self, video_file, audio_file):
        """Merge video with audio track"""
        if not audio_file or not os.path.exists(audio_file):
            logging.warning("No audio file provided or audio file doesn't exist")
            return video_file

        logging.info(f"Merging video with audio: {audio_file}")

        video_duration = self.get_media_duration(video_file)
        audio_duration = self.get_media_duration(audio_file)

        logging.info(
            f"Video duration: {video_duration}s, Audio duration: {audio_duration}s"
        )

        # Extend video if needed
        if audio_duration > video_duration:
            video_file = self.extend_video_to_audio_length(video_file, audio_duration)

        # Merge video and audio
        merged_video = self.temp_dir / f"merged_video_{self.session_id}.mp4"
        self.cleanup_files.append(str(merged_video))

        command = [
            "ffmpeg",
            "-y",
            "-i",
            video_file,
            "-i",
            audio_file,
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
            "-shortest",  # End when shortest stream ends
            str(merged_video),
        ]

        self.run_subprocess_safely(command)
        return str(merged_video)

    def crop_to_portrait(self, video_file, subtitle_file=None):
        """Crop video to 9:16 portrait aspect ratio"""
        logging.info("Cropping video to 9:16 portrait format")
        subtitle_file = "output/subtitles/subtitles.ass"

        portrait_video = (
            self.base_output_dir
            / "final_video"
            / f"portrait_output_{self.session_id}.mp4"
        )

        # Build filter complex
        video_filter = "scale=w=min(iw\\,ih*9/16):h=min(ih\\,iw*16/9):force_original_aspect_ratio=decrease,pad=ceil(iw/2)*2:ceil(ih*16/9/2)*2:(ow-iw)/2:(oh-ih)/2:black"

        # Add subtitles if file exists
        if subtitle_file and os.path.exists(subtitle_file):
            video_filter += f",subtitles={subtitle_file}"
            logging.info(f"Adding subtitles from: {subtitle_file}")
        else:
            logging.info(f"No subtitle file provided or subtitle file doesn't exist: {subtitle_file}")

        command = [
            "ffmpeg",
            "-y",
            "-i",
            video_file,
            "-vf",
            video_filter,
            "-c:a",
            "copy",
            str(portrait_video),
        ]

        self.run_subprocess_safely(command)
        logging.info(f"Portrait video created: {portrait_video}")
        return str(portrait_video)

    def create_manim_video(
        self, video_data, manim_code, audio_file=None, subtitle_file=None
    ):
        """Main function to create Manim video with all processing steps"""
        try:
            logging.info("Starting Manim video creation process")

            # Ensure all directories exist
            self.ensure_directories()

            # Step 1: Create Manim scene
            video_file = self.create_manim_scene(manim_code)

            # Step 2: Merge with audio if provided
            if audio_file:
                video_file = self.merge_video_audio(video_file, audio_file)

            # Step 3: Crop to portrait and add subtitles
            subtitle_path = None
            if subtitle_file:
                # Check if subtitle file exists, if not, check in default location
                if os.path.exists(subtitle_file):
                    subtitle_path = subtitle_file
                else:
                    default_subtitle_path = (
                        self.base_output_dir / "subtitles" / "subtitles.ass"
                    )
                    if default_subtitle_path.exists():
                        subtitle_path = str(default_subtitle_path)

            final_video = self.crop_to_portrait(video_file, subtitle_path)

            logging.info(f"Final video created successfully: {final_video}")
            return final_video

        except Exception as e:
            logging.error(f"Error creating Manim video: {e}")
            raise e


# Usage function for backward compatibility
def create_manim_video(video_data, manim_code, audio_file=None, subtitle_file=None):
    """
    Create Manim video with proper error handling and cleanup

    Args:
        video_data: Video data (kept for compatibility)
        manim_code: Manim Python code as string
        audio_file: Path to audio file (optional)
        subtitle_file: Path to subtitle file (optional)

    Returns:
        Path to final video file
    """
    with ManimVideoProcessor() as processor:
        return processor.create_manim_video(
            video_data, manim_code, audio_file, subtitle_file
        )
