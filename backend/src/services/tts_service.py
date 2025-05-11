from kokoro import KPipeline
import soundfile as sf
import os
import wave
import numpy as np
from typing import Optional, Dict, List, Tuple
from src.services.ass_file_service import SRTTOASSConverter
import logging


class TTSService:
    def __init__(self, lang_code: str = "a"):
        """Initialize the TTS service with Kokoro"""
        self.pipeline = KPipeline(lang_code=lang_code)
        self.voice_presets = {
            "en-us": "af_heart",  # American English
            "en-uk": "bf_heart",  # British English
            "es": "es_heart",  # Spanish
            "fr": "fr_heart",  # French
            "hi": "hi_heart",  # Hindi
            "it": "it_heart",  # Italian
            "pt-br": "pt_heart",  # Brazilian Portuguese
            "ja": "ja_heart",  # Japanese
            "zh": "zh_heart",  # Mandarin Chinese
        }

    def _format_timestamp(self, seconds: float) -> str:
        """Convert seconds to SRT timestamp format HH:MM:SS,mmm"""
        try:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            seconds_part = seconds % 60
            milliseconds = int((seconds_part - int(seconds_part)) * 1000)
            
            return f"{hours:02d}:{minutes:02d}:{int(seconds_part):02d},{milliseconds:03d}"
        except Exception as e:
            logging.error(f"Error formatting timestamp: {e}")
            return "00:00:00,000"

    def write_sentence_srt(
        self, word_timestamps: List[Dict], output_file: str, max_words: int = 8
    ):
        """Generate subtitle file with synchronized timestamps"""
        try:
            os.makedirs(os.path.dirname(output_file), exist_ok=True)

            subtitles = []  # Store subtitle blocks
            subtitle_words = []  # Temporary list for words in current subtitle
            start_time = None  # Track start time of current subtitle

            for entry in word_timestamps:
                word = entry["word"]
                word_start = entry["start"]
                word_end = entry["end"]

                # Start a new subtitle block if needed
                if start_time is None:
                    start_time = word_start

                # Create a new subtitle if we have enough words or hit punctuation
                if len(subtitle_words) >= max_words or word.endswith((".", "!", "?")):
                    if subtitle_words:  # Only proceed if we have words to add
                        end_time = subtitle_words[-1][1]  # Use last word's end time
                        subtitle_text = " ".join(w[0] for w in subtitle_words)
                        subtitles.append((start_time, end_time, subtitle_text))

                        # Reset for next subtitle
                        subtitle_words = []
                        start_time = None if word.endswith((".", "!", "?")) else word_start

                # Add current word to subtitle
                subtitle_words.append((word, word_end))

            # Add any remaining words as final subtitle
            if subtitle_words:
                end_time = subtitle_words[-1][1]
                subtitle_text = " ".join(w[0] for w in subtitle_words)
                subtitles.append((start_time, end_time, subtitle_text))

            # Write subtitles to SRT file
            with open(output_file, "w", encoding="utf-8") as f:
                for i, (start, end, text) in enumerate(subtitles, start=1):
                    print(f"Writing subtitle {i}: {text} [{start} --> {end}]")
                    f.write(
                        f"{i}\n{self._format_timestamp(start)} --> {self._format_timestamp(end)}\n{text}\n\n"
                    )

            return output_file
        except Exception as e:
            logging.error(f"Error writing SRT file: {e}")
            return None

    def generate(
        self, text: str, voice: str = "en-us", output_path: Optional[str] = None
    ) -> Tuple[str, str]:
        """Generate audio from text using the specified voice and create synchronized subtitles"""
        try:
            logging.info(f"Generating audio for text: {text[:30]}...")
            if not text:
                raise ValueError("Text cannot be empty")

            if voice not in self.voice_presets:
                raise ValueError(
                    f"Unsupported voice: {voice}. Available voices: {list(self.voice_presets.keys())}"
                )

            if output_path is None:
                output_path = f"output/audio/output_{voice}.wav"

            # Ensure output directories exist
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            subtitles_dir = "output/subtitles"
            os.makedirs(subtitles_dir, exist_ok=True)

            subtitles_path = os.path.join(subtitles_dir, "subtitles.srt")

            generator = self.pipeline(
                text, voice=self.voice_presets[voice], speed=1, split_pattern=r"\n+"
            )

            # Prepare audio data
            word_timestamps = []
            current_offset = 0.0  # Track running time offset between segments
            all_audio = []

            for i, result in enumerate(generator):
                graphemes = result.graphemes  # text segment
                audio = result.audio  # audio tensor
                tokens = result.tokens  # List of tokens with timing info

                # Extract word timing information
                if tokens:  # Only process if tokens are available (English voices)
                    for t in tokens:
                        if t.text.strip():  # Skip empty tokens
                            word_timestamps.append(
                                {
                                    "word": t.text,
                                    "start": t.start_ts + current_offset,
                                    "end": t.end_ts + current_offset,
                                }
                            )

                # Convert audio tensor to numpy array
                audio_np = audio.numpy()
                all_audio.append(audio_np)

                # Update time offset for next segment
                segment_duration = len(audio_np) / 24000  # in seconds
                current_offset += segment_duration

            # Concatenate all audio segments and write to file
            final_audio = np.concatenate(all_audio)
            sf.write(output_path, final_audio, 24000)

            # Generate subtitles if we have timestamps
            if word_timestamps:
                self.write_sentence_srt(word_timestamps, subtitles_path)

            return output_path

        except Exception as e:
            logging.error(f"Error generating audio: {e}")
            return None


def generate_audio(text: str, voice: str = "en-us"):
    """Generate audio and subtitles from text using Kokoro TTS"""
    try:
        service = TTSService()

        audio_file_path = service.generate(text=text)
        if audio_file_path:
            ass_converter = SRTTOASSConverter(
                input_file="output/subtitles/subtitles.srt",
                output_file="output/subtitles/subtitles.ass",
            )
            ass_converter.generate_ass_file()

        return audio_file_path
    except Exception as e:
        logging.error(f"Error geneate_audio: {e}")



if __name__ == "__main__":
    # Example usage
    text = """
Your morning eyes, I could stare like watching stars
I could walk you by, and I'll tell without a thought
You'd be mine, would you mind if I took your hand tonight?
Know you're all that I want this life"""
    audio_file = generate_audio(text=text)
    print(f"Generated audio file: {audio_file}")