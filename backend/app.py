import logging
from main import _create_manim_video
from src.Youtube.youtube_video_idea import generate_video_idea
from src.Youtube.video_metadata import generate_youtube_metadata
from src.Youtube.run import push_youtube_video
from src.utils.download_video import download_video

LOCAL_PATH_VIDEO = "temp/temp_video.mp4"

def _create_video():
    try:
        # Using Gemini create video idea / script
        youtube_video_idea = generate_video_idea()
        logging.info("YOUTUBE video idea is created")

        # Using Gemini create metadata for youtube (title, description, tags)
        youtube_metadata = generate_youtube_metadata(idea=youtube_video_idea)
        logging.info("YOUTUBE video metadata is created")

        # Using manim code and Gemini we will create manim video
        video_file_url = _create_manim_video(video_idea=youtube_video_idea)
        logging.info("YOUTUBE video file url is created")

        if video_file_url is not None:
            # Download video_file_url to upload
            download_video(url=video_file_url, local_path=LOCAL_PATH_VIDEO)
            logging.info("Manim file is Download from Cloudinary")

            # After downloading file we want to push the youtube video
            push_youtube_video(
                metadata=youtube_metadata,
                media_file=LOCAL_PATH_VIDEO
            )
            logging.info("YOUTUBE video idea is upload. 😃😃")

    except Exception as e:
        logging.error(f"ERROR when running _create_video: {e}")

if __name__ == '__main__':
    _create_video()
