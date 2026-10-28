# Datheon Task 1 – Structured LLM Prompt Pipeline & JSON Extractor

A Python-based resume information extractor built for the **Datheon Python + Generative AI & LangChain Internship**.

The application accepts an unstructured resume file and uses **Google Gemini** to extract structured information into validated JSON.

## Features

- Supports **TXT, PDF, and DOCX** resume files
- Extracts resume information using Google Gemini
- Produces structured JSON output
- Validates extracted data using **Pydantic**
- Provides a command-line interface
- Safely processes uploaded/local resume files

## Extracted Fields

The application extracts:

- Name
- Email
- Phone
- Job title
- Years of experience
- Skills

## Project Structure

```text
datheon-task-1/
├── .gitignore
├── README.md
├── requirements.txt
└── src/
    ├── file_parser.py
    ├── llm.py
    ├── main.py
    └── models.py
```

## Technologies Used

- Python
- Google Gemini API
- `google-genai`
- Pydantic
- python-dotenv
- PyPDF
- python-docx

## Setup

Clone the repository and navigate to the Task 1 directory.

Create and activate a virtual environment:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

Install the required dependencies:

```powershell
pip install -r requirements.txt
```

Create a `.env` file in the project directory:

```text
GEMINI_API_KEY=your_api_key_here
```

**Never commit your `.env` file or API key to GitHub.**

## Run the Application

From the `datheon-task-1` directory:

```powershell
python src/main.py
```

The application will ask for the path to a resume file.

Example:

```text
Enter the resume file path: test_resume.docx
```

The application reads the file, sends the extracted text to Gemini, and returns structured JSON.

## Example Output

```json
{
    "name": "Rahul Verma",
    "email": "rahul.verma@example.com",
    "phone": "9123456780",
    "job_title": "Software Engineer",
    "experience_years": 4.0,
    "skills": [
        "Python",
        "Java",
        "FastAPI",
        "Docker",
        "Git",
        "PostgreSQL"
    ]
}
```

## Supported File Formats

| Format | Supported |
|---|---|
| TXT | Yes |
| PDF | Yes |
| DOCX | Yes |

## Project Objective

The objective of this task is to demonstrate a structured LLM prompt pipeline that converts unstructured resume content into reliable, validated JSON data.

## Datheon Internship

**Program:** Python + Generative AI & LangChain Internship

**Task:** Task 1 – Structured LLM Prompt Pipeline & JSON Extractor