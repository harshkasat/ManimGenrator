import pathlib
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs/load_manim.log"), logging.StreamHandler()],
)


def load_manim_examples():
    """
    Load Manim guid from the specified directory.
    """
    guid_path = guid_path = pathlib.Path(__file__).resolve().parents[2] / "guide.md"

    if not guid_path.exists():
        logging.warning(f"Manim guide file not found at {guid_path}.")
        return None

    logging.info(f"Loading Manim guide from {guid_path}.")
    return guid_path.read_text(encoding="utf-8")
