import os
import logging
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

load_dotenv()


class GoogleSheet:
    def __init__(self):
        # === Setup Credentials ===
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            "src/GoogleSheet/google_cred.json", scope
        )
        self.client = gspread.authorize(creds)
        # === Open Google Sheet ===
        sheet_id = os.getenv("SHEET_ID")  # Replace with actual ID
        self.sheet = self.client.open_by_key(sheet_id).sheet1

    def append_data(
        self,
        video_url: str,
        video_title: str,
        video_description: str,
        video_tags: str,
    ):
        try:
            # === Open Google Sheet ===
            # sheet_id = os.getenv("SHEET_ID")  # Replace with actual ID
            # sheet = self.client.open_by_key(sheet_id).sheet1

            # === Headers (Add if not exist) ===
            headers = [
                "Video url",
                "Title",
                "Description",
                "Tags",
                "Date created",
                "Status",
            ]
            if not self.sheet.row_values(1):
                self.sheet.append_row(headers)

            # === Example Video Data ===
            video_data = {
                "Video url": video_url,
                "Title": video_title,
                "Description": video_description,
                "Tags": video_tags,
                "Date created": datetime.now().strftime("%Y-%m-%d"),
                "Status": "Pending",
            }

            # === Push to Sheet ===
            row = [video_data[h] for h in headers]
            self.sheet.append_row(row)

            logging.info("Video pushed to Google Sheet.")

        except Exception as e:
            logging.error(f"ERROR when running google sheet append data: {e}")

    def get_all_title(self):
        try:
            titles = self.sheet.col_values(2)  # 2 if "title" is in column B

            logging.info("ALL titles are retreive from google sheet")
            return titles
        except Exception as e:
            logging.error(f"ERROR when running Google Sheet to get_all_title: {e}")
