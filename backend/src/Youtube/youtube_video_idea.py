from src.llmConfig.config import LLMConfig
import logging

PROMPT = """I run a YouTube Shorts channel that explains deep math and science concepts visually using Manim, inspired by 3Blue1Brown.
Give me one original video idea that:
1. Is short (suitable for under 60 seconds),
2. Can be explained visually using Manim,
3. Has an intuitive "aha" insight,
4. Is beginner-friendly but mind-expanding.
The idea should be described in 2–3 sentences, enough for me to storyboard and animate it.
** IMPORTANT **
AVOID THIS IDEAS: {avoid_ideas}"""


def generate_video_idea(avoid_this_ideas):
    try:
        llm = LLMConfig()
        prompt = PROMPT.format(avoid_ideas=avoid_this_ideas)
        resposne = llm.general_content(idea=prompt)
        logging.info("YOUTUBE idea is created")
        return resposne.text
    except Exception as e:
        logging.error(f"ERROR when generate metadata content: {e}")

# if __name__ == '__main__':
#     print(generate_idea())
