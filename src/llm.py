import os
import time

from dotenv import load_dotenv
from google import genai

from models import ResumeData

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in the .env file.")

client = genai.Client(api_key=api_key)

MODEL_NAME = "gemini-3.8-flash"


def extract_resume_data(input_text: str) -> ResumeData:
    """
    Extract structured resume information from unstructured text.

    Retries temporary Gemini service failures before returning an error.
    """

    prompt = f"""
Extract structured resume information from the text below.

Identify:
- name
- email
- phone
- job_title
- experience_years
- skills

Resume text:

{input_text}
"""

    max_attempts = 3

    for attempt in range(1, max_attempts + 1):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_json_schema": ResumeData.model_json_schema(),
                },
            )

            return ResumeData.model_validate_json(response.text)

        except Exception as error:
            error_message = str(error)

            is_temporary_error = (
                "503" in error_message
                or "UNAVAILABLE" in error_message
                or "Server disconnected" in error_message
            )

            if not is_temporary_error or attempt == max_attempts:
                raise

            wait_seconds = 2 ** attempt

            print(
                f"Gemini temporarily unavailable. "
                f"Retrying in {wait_seconds} seconds "
                f"(attempt {attempt}/{max_attempts})..."
            )

            time.sleep(wait_seconds)