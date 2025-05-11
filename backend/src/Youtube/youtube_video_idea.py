from src.llmConfig.config import LLMConfig
import logging

PROMPT = """I run a YouTube Shorts channel that explains deep math and science concepts visually using Manim, inspired by 3Blue1Brown.
Give me one original video idea that:
1. Is short (suitable for under 60 seconds),
2. Can be explained visually using Manim,
3. Has an intuitive "aha" insight,
4. Is beginner-friendly but mind-expanding.
The idea should be described in 2–3 sentences, enough for me to storyboard and animate it."""


def generate_video_idea():
    try:
        llm = LLMConfig()
        resposne = llm.general_content(idea=PROMPT)
        logging.info("YOUTUBE idea is created")
        return resposne.text
    except Exception as e:
        logging.error(f"ERROR when generate metadata content: {e}")

# if __name__ == '__main__':
#     print(generate_idea())
