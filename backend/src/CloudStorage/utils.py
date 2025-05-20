import os
import cloudinary
import cloudinary.api
from cloudinary.uploader import upload as cloud_uploader
from . import cloudinary_config


class CloudinaryStorage:
    def __init__(self) -> None:
        cloudinary_config()
        self.folder = "MANIM_AI_GENERATED_VIDEOS"

    def get_files_from_cloudinary(self):
        try:
            result = cloudinary.api.resources_by_asset_folder(asset_folder=self.folder)
            return result["secure_url"], result["display_name"]
        except Exception as e:
            print(f"Error getting file: {e}")
            return None, None

    def upload_to_cloudinary(self, file_path, project_name: str):
        try:
            print(f"Uploading file: {file_path}")
            upload_result = cloud_uploader(
                file=file_path,
                public_id=project_name,
                folder=self.folder,
                overwrite=False,
                resource_type="raw",
            )

            return upload_result["secure_url"]
        except Exception as e:
            print(f"Error uploading file: {e}")
            return None
