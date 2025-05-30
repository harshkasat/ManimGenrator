import os
import cloudinary
from dotenv import load_dotenv

load_dotenv()


def cloudinary_config():
    config = cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_NAME"),
        api_key=os.getenv("CLOUDINARY_API_KEY"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET"),
        secure=True,
    )

    return config
