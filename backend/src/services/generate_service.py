import os
import re
import logging
from src.llmConfig.config import LLMConfig
from src.llmConfig import BASE_PROMPT_INSTRUCTIONS, SYSTEM_PROMPT
from src.utils.load_manim import load_manim_examples


def generate_video(idea: str | None = None):
    contents = []

    manim_examples = load_manim_examples()
    if manim_examples:
        examples_prompt = (
            "Below are examples of Manim code that demonstrate proper usage patterns. Use these as reference when generating your animation:\n\n" + manim_examples
        )
        contents.append(examples_prompt)
        logging.info("Added Manim examples from guide.md to prime the model")
    else:
        logging.warning("No Manim examples were loaded from guide.md")

    user_prompt_text = ""

    if idea:
        logging.info(f"Generating video based on idea: {idea[:50]}...")
        user_prompt_text = f"Create a 30-second Manim video script about '{idea}'. {BASE_PROMPT_INSTRUCTIONS}"
        contents.append(user_prompt_text)

    response = LLMConfig().generate_video(idea=user_prompt_text)
    print(response.text)

    if response:
        try:
            content = response.text
            logging.info("Received response from Gemini.")
        except ValueError:
            logging.warning(
                "Could not extract text from the response. Response details:"
            )
            logging.warning(response)
            if response.prompt_feedback and response.prompt_feedback.block_reason:
                logging.error(
                    f"Content generation blocked. Reason: {response.prompt_feedback.block_reason.name}"
                )
                raise Exception(
                    f"Content generation blocked. Reason: {response.prompt_feedback.block_reason.name}"
                )
            else:
                logging.error(
                    "Failed to generate content. The response was empty or malformed."
                )
                raise Exception(
                    "Failed to generate content. The response was empty or malformed."
                )

        if "### NARRATION:" in content:
            manim_code, narration = content.split("### NARRATION:", 1)
            manim_code = re.sub(r"```python", "", manim_code).replace("```", "").strip()
            narration = narration.strip()
            logging.info("Successfully parsed code and narration using delimiter.")

            if "from manim import *" not in manim_code:
                logging.warning("Adding missing 'from manim import *'.")
                manim_code = "from manim import *\nimport numpy as np\n" + manim_code
            elif "import numpy as np" not in manim_code:
                logging.warning("Adding missing 'import numpy as np'.")
                lines = manim_code.splitlines()
                for i, line in enumerate(lines):
                    if "from manim import *" in line:
                        lines.insert(i + 1, "import numpy as np")
                        manim_code = "\n".join(lines)
                        break

            return {"manim_code": manim_code, "output_file": "output.mp4"}, narration
        else:
            logging.warning(
                "Delimiter '### NARRATION:' not found. Attempting fallback extraction."
            )
            code_match = re.search(r"```python(.*?)```", content, re.DOTALL)
            if code_match:
                manim_code = code_match.group(1).strip()
                narration_part = content.split("```", 2)[-1].strip()
                narration = narration_part if len(narration_part) > 20 else ""
                if not narration:
                    logging.warning(
                        "Fallback narration extraction resulted in empty or very short text."
                    )
                else:
                    logging.info(
                        "Successfully parsed code and narration using fallback regex."
                    )

                if "from manim import *" not in manim_code:
                    logging.warning("Adding missing 'from manim import *' (fallback).")
                    manim_code = (
                        "from manim import *\nimport numpy as np\n" + manim_code
                    )
                elif "import numpy as np" not in manim_code:
                    logging.warning("Adding missing 'import numpy as np' (fallback).")
                    lines = manim_code.splitlines()
                    for i, line in enumerate(lines):
                        if "from manim import *" in line:
                            lines.insert(i + 1, "import numpy as np")
                            manim_code = "\n".join(lines)
                            break

                return {
                    "manim_code": manim_code,
                    "output_file": "output.mp4",
                }, narration
            else:
                logging.error(
                    "Fallback extraction failed: No Python code block found in response."
                )
                logging.debug(f"Content without code block:\n{content}")
                raise Exception(
                    "The response does not contain the expected "
                    "'### NARRATION:' delimiter or a valid Python code block."
                )

    else:
        logging.error(
            "Error generating video content. No response received from Gemini."
        )
        raise Exception("Error generating video content. No response received.")
