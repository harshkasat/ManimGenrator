import os
from google import genai
from google.genai import types as genai_types
from dotenv import load_dotenv
import re
import logging
# from CloudStorage.utils import CloudinaryStorage

load_dotenv()
from src.llmConfig import SAFE_SETTINGS, SYSTEM_PROMPT

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs/config.log"), logging.StreamHandler()],
)


class LLMConfig:
    def __init__(self):
        self.gemini_api_key = os.getenv("GENAI_API_KEY")
        if not self.gemini_api_key:
            logging.error("Gemini API key not found in environment variables.")
            raise ValueError(
                "Gemini API key not found. Please set "
                "the GENAI_API_KEY environment variable."
            )

    def generate_video(self, idea: str | None = None):
        generate_config = ""
        """
        Generate a video using the provided idea and the Manim guide.
        """

        client = genai.Client(api_key=self.gemini_api_key)
        logging.info("Gemini client initialized.")

        try:
            generate_config = genai_types.GenerateContentConfig(
                safety_settings=SAFE_SETTINGS, system_instruction=SYSTEM_PROMPT
            )
            logging.info("GenerateContentConfig created.")
        except Exception as e:
            logging.error(f"Failed to create GenerateContentConfig: {e}")
            return None

        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001", contents=idea, config=generate_config
            )
            logging.info("Content generated successfully.")
        except Exception as e:
            logging.error(f"Failed to generate content: {e}")
            return None

        return response

