import os
import requests
import logging

def download_video(url, local_path):
    # Download the video from the URL and save it to the local file system
    try:
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        response = requests.get(url, timeout=20)
        if response.status_code == 200:
            with open(local_path, 'wb') as f:
                f.write(response.content)
            logging.info(f"Video downloaded successfully to {local_path}")
        else:
            logging.error("Failed to download video")
    except Exception as e:
        logging.error(f"ERROR when run download video: {e}")
