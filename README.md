# ManimGenrator: Automated Math Animation Video Generator

This project automates the creation of educational math animation videos using Manim, leveraging AI for script generation and video metadata creation.  It integrates with Google Sheets for managing video ideas and uploaded video data.

## 1. Project Title and Short Description

**ManimGenrator:** Automated Math Animation Video Generator

ManimGenrator is a Python-based application that automatically generates educational math animation videos using the Manim library. It utilizes AI to create video scripts and metadata, streamlining the video production process and integrating with Google Sheets for project management.


[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)  (Add other badges as appropriate, e.g., build status, code coverage)


## 2. Project Overview

ManimGenrator addresses the time-consuming nature of creating high-quality math animation videos.  It automates several key steps, including:

* **Idea Generation:** Uses AI to generate video ideas based on user input or existing data.
* **Script Writing:**  Generates scripts for the animations using AI.
* **Manim Code Generation:** Produces Manim code based on the generated script.
* **Video Rendering:** Renders the Manim code into a video file.
* **Metadata Generation:** Creates YouTube metadata (title, description, tags).
* **Upload to Cloudinary:** Uploads the rendered video to Cloudinary cloud storage.
* **Google Sheet Integration:** Manages video ideas and uploads video data to a Google Sheet.


## 3. Table of Contents

* [Project Title and Short Description](#project-title-and-short-description)
* [Project Overview](#project-overview)
* [Table of Contents](#table-of-contents)
* [Prerequisites](#prerequisites)
* [Installation Guide](#installation-guide)
* [Configuration](#configuration)
* [Usage Examples](#usage-examples)
* [Project Architecture](#project-architecture)
* [Contributing Guidelines](#contributing-guidelines)
* [License](#license)


## 4. Prerequisites

* Python 3.7+
* Manim library (installation instructions provided below)
* Google Cloud Platform (GCP) credentials (for Google Sheets integration)
* Cloudinary account (for video storage)
*  Libraries specified in `requirements.txt` (if applicable, create a requirements.txt file)


## 5. Installation Guide

1. **Clone the repository:**
   ```bash
   git clone https://github.com/harshkasat/ManimGenrator.git
   cd ManimGenrator
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt  #(Create requirements.txt if needed)
   ```

4. **Install Manim:** (Follow Manim's installation instructions; this may involve additional steps depending on your operating system and preferences).

5. **Configure environment variables:**  (See the Configuration section below)


## 6. Configuration

* **Google Cloud Credentials:**  Set the GOOGLE_APPLICATION_CREDENTIALS environment variable to point to your GCP service account key file.
* **Cloudinary Credentials:** Set CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, and CLOUDINARY_API_SECRET environment variables with your Cloudinary credentials.
* **Other settings:**  The project might use other configuration files or settings; consult the codebase for details.


## 7. Usage Examples

The main execution point is `backend/app.py`. The `_create_video()` function orchestrates the entire process:

```python
def _create_video():
    try:
        avoid_ideas = GoogleSheet().get_all_title()  # Get existing video titles from Google Sheet
        youtube_video_idea = generate_video_idea(avoid_this_ideas=avoid_ideas) # Generate a new video idea
        video_file_url = _create_manim_video(video_idea=youtube_video_idea) # Generate the Manim video

        if video_file_url is not None:
            video_metadata = generate_youtube_metadata(idea=youtube_video_idea) # Generate metadata
            GoogleSheet().append_data(video_url=video_file_url, video_title=video_metadata["title"], video_description=video_metadata["description"], video_tags=video_metadata["tags"]) # Update Google Sheet
    except Exception as e:
        logging.error(f"ERROR when running _create_video: {e}")

if __name__ == "__main__":
    _create_video()
```

The `_create_manim_video` function in `backend/main.py` calls the `main` function which handles Manim video generation, audio generation, and error handling:

```python
def _create_manim_video(video_idea: str):
    try:
        cloudinary_storage = CloudinaryStorage()
        video_file = main(idea=video_idea) # Calls the main function to generate the video
        if os.path.isfile(video_file):
            resposne = cloudinary_storage.upload_to_cloudinary(file_path=video_file, project_name=video_idea.strip()[:21])
            return resposne
        else:
            logging.warning(f"Could not find the file to upload: {video_file}")
            return None
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None
    finally:
        # ... cleanup code ...
```

A sample Manim scene (from `backend/generated_video.py`):

```python
class GaussianBlurAveraging(Scene):
    def construct(self):
        # ... Manim code to create the animation ...
```


## 8. Project Architecture

The project is structured into several modules:

* `src/services`: Contains services for video generation, audio generation, and Manim interaction.
* `src/llmConfig`: Handles AI interaction and code fixing.
* `src/CloudStorage`: Manages cloud storage interactions (Cloudinary).
* `src/GoogleSheet`: Handles Google Sheet integration.
* `src/Youtube`: Contains functions for generating video ideas and metadata.
* `src/utils`: Contains utility functions.


## 9. Contributing Guidelines

Contributions are welcome! Please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) file for details on how to contribute, the code of conduct, and the contribution process. (Create a CONTRIBUTING.md file)


## 10. License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. (Create a LICENSE file)


## 11. Acknowledgments

(Add any acknowledgments here)


## 12. Contact and Support

(Add contact information and support channels here)


**(Note:  This README is a template based on the provided code snippets.  You'll need to fill in missing sections, add more details based on the full project code, and create the missing files (CONTRIBUTING.md, LICENSE, requirements.txt).  The architecture section is a high-level overview; you might want to add more detailed diagrams or explanations.)**
