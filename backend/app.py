import logging
from main import _create_manim_video
from src.Youtube.youtube_video_idea import generate_video_idea
from src.Youtube.video_metadata import generate_youtube_metadata
from src.GoogleSheet.google_sheet import GoogleSheet


def _create_video():
    try:
        # Get All ideas title to avoid
        gsheet = GoogleSheet()
        avoid_ideas = gsheet.get_all_title()
        # Using Gemini create video idea / script
        youtube_video_idea = generate_video_idea(avoid_this_ideas=avoid_ideas)
        logging.info("YOUTUBE video idea is created")

        # Using manim code and Gemini we will create manim video
        video_file_url = _create_manim_video(video_idea=youtube_video_idea)

        logging.info("YOUTUBE video file url is created")

        if video_file_url is not None:
            # Using Gemini create metadata for youtube (title, description, tags)
            video_metadata = generate_youtube_metadata(idea=youtube_video_idea)
            logging.info("YOUTUBE video metadata is created")

            # After downloading file we want to push the google sheet
            gsheet.append_data(
                video_url=video_file_url,
                video_title=video_metadata.get("title"),
                video_description=video_metadata.get("description"),
                video_tags=video_metadata.get("tags"),
            )
            logging.info("Google Sheet data is upload.")
            logging.info(f"Video Title: {video_metadata.get('title')}")

    except Exception as e:
        logging.error(f"ERROR when running _create_video: {type(e).__name__}: {e}")


if __name__ == "__main__":
    _create_video()
