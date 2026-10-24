import os
from dotenv import load_dotenv
from google import genai

from models import ResumeData


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in the .env file.")

client = genai.Client(api_key=api_key)


def extract_resume_data(input_text: str) -> ResumeData:
    """
    Extract structured resume information from unstructured text.
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

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_json_schema": ResumeData.model_json_schema(),
        },
    )

    result = ResumeData.model_validate_json(response.text)

    return result