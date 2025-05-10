import os
import tempfile
import subprocess
import logging
from src.services.generate_service import generate_video
from src.llmConfig.fallback_fix_generation import fix_manim_code
from src.services.manim_service import create_manim_video
from src.services.tts_service import generate_audio


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def main():
    video_data = None
    script = None
    audio_file = None
    final_video = None

    # Get the idea from the user
    idea = input("Enter your idea: ")

    # Generate video using the idea
    video_data, script = generate_video(idea)

    if not video_data:
        logging.error("Failed to generate video data.")
        return

    if not script:
        logging.error("Failed to generate script.")
        return

    # Generate the audio script
    audi0_file = generate_audio(script)

    if not audi0_file:
        logging.error("Failed to generate audio file.")
        return

    max_retries = 1
    current_manim_code = video_data["manim_code"]
    current_script = script
    current_audio_file = audi0_file

    for attempt in range(max_retries + 1):
        try:
            logging.info(f"Attempt {attempt + 1} to create Manim video.")
            final_video = create_manim_video(
                {"manim_code": current_manim_code, "output_file": "output.mp4"},
                current_manim_code,
                audio_file=current_audio_file,
            )
            logging.info("Manim video creation successful.")
            break
        except subprocess.CalledProcessError as e:
            logging.error(f"Manim execution failed on attempt {attempt + 1}.")
            if attempt < max_retries:
                logging.info("Calling fallback Gemini to fix code.")
                error_message = (
                    e.stderr.decode()
                    if e.stderr
                    else "Manim execution failed without specific error output."
                )

                fixed_video_data, fixed_script = fix_manim_code(
                    faulty_code=current_manim_code,
                    error_message=error_message,
                    original_context=idea,
                )

                if fixed_video_data and fixed_script is not None:
                    logging.info("Fallback successful. Received fixed code.")
                    current_manim_code = fixed_video_data["manim_code"]
                    if fixed_script != current_script and fixed_script:
                        logging.info("Regenerating audio for updated script.")
                        current_script = fixed_script
                        try:
                            current_audio_file = generate_audio(current_script)
                        except ValueError as e:
                            current_audio_file = None
                    elif not fixed_script:
                        logging.warning("Fallback provided empty narration.")
                        current_script = ""
                        current_audio_file = None
                    else:
                        logging.info("Fallback kept the original narration.")
                else:
                    logging.error("Fallback failed to return valid code/script.")
                    final_video = None
                    break
            else:
                logging.error(f"Manim failed after {max_retries + 1} attempts.")
                final_video = None
        except Exception as e:
            logging.exception("Unexpected error during create_manim_video call.")
            final_video = None
            break

if __name__ == "__main__":
    main()