import json
import re
import logging
from src.llmConfig.config import LLMConfig


PROMPT = """
I run a YouTube Shorts channel that explains complex concepts visually using animations made with Manim, inspired by the 3Blue1Brown style.
Given the concept: {concept}, generate:

1. A catchy, short YouTube title
2. A brief description explaining the concept simply
3.5-7 relevant hashtags/tags to boost discoverability
THE response must like this:
{{
    "title" : "Title for YOUTUBE VIDEO",
    "description" : "Description for YOUTUBE VIDEO",
    "tags": ["LISTS of Tags for YOUTUBE VIDEO"]
}}"""


def extract_clean_json(raw_text):
    try:
        # remove ```json and ``` if present
        raw_text = raw_text.strip()
        cleaned = re.search(r'\{.*\}', raw_text, re.DOTALL)
        if not cleaned:
            logging.error("No valid JSON found in the input.")
            return None
        json_str = cleaned.group(0)
        return json.loads(json_str)
    except Exception as e:
        logging.error(f"Error parsing JSON from LLM output: {e}")
        return None


def validate_youtube_response(response: dict) -> bool:
    try:
        required_keys = {"title": str, "description": str, "tags": list}

        if not isinstance(response, dict):
            print("Response is not a dictionary.")
            return False
        for key, expected_type in required_keys.items():
            if key not in response:
                print(f"Missing key: {key}")
                return False
            if not isinstance(response[key], expected_type):
                print(
                    f"Key '{key}' must be of type {expected_type.__name__}. Got {type(response[key]).__name__} instead."
                )
                return False

        return True
    except Exception as e:
        logging.error(f"ERROR when validate youtube response: {e}")
        return False


def generate_metadata_content(title: str):

    try:
        llm = LLMConfig()
        prompt = PROMPT.format(concept=title)
        resposne = llm.general_content(idea=prompt)

        return resposne.text
    except Exception as e:
        logging.error(f"ERROR when generate metadata content: {e}")

def generate_youtube_metadata(idea, retry=3):
    if retry == 0:
        logging.error("Max retries reached. Failed to generate valid YouTube metadata.")
        return None

    response = generate_metadata_content(title=idea)
    try:
        # Ensure the response is parsed if it's a string
        if isinstance(response, str):
            response = extract_clean_json(raw_text=response)
    except Exception as e:
        logging.error(f"ERROR parsing LLM response to JSON: {e}")
        return generate_youtube_metadata(idea, retry=retry - 1)

    if validate_youtube_response(response):
        return response
    else:
        return generate_youtube_metadata(idea, retry=retry - 1)

# if __name__ == '__main__':
#     title = "Patterns in Multiplication: Show patterns that emerge when multiplying " \
#     "numbers (like the multiplication table) and how to recognize these patterns visually."
#     result = generate_youtube_metadata(idea=title)
#     print(result)
