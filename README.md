# Structured LLM Prompt Pipeline & JSON Extractor

A Python-based Generative AI application that extracts structured information from unstructured resume text using Google's Gemini API and validates the result with Pydantic.

## 📌 Project Overview

This project is part of the **Datheon Python + Generative AI & LangChain Internship**.

The application accepts unstructured resume text and uses a Large Language Model (LLM) to extract important candidate information into a structured JSON format.

### Extracted Information

- Name
- Email
- Phone number
- Job title
- Years of professional experience
- Skills

The extracted response is validated using a Pydantic model to ensure the output follows the expected structure.

## 🏗️ Project Structure

```text
datheon-task-1/
│
├── src/
│   ├── main.py
│   ├── models.py
│   └── llm.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## ⚙️ Technologies Used

- Python
- Google Gemini API
- Google GenAI Python SDK
- Pydantic
- python-dotenv
- JSON

## 🔄 How It Works

```text
Resume Text
    ↓
Prompt Construction
    ↓
Google Gemini
    ↓
Structured JSON Response
    ↓
Pydantic Validation
    ↓
Validated Resume Data
```

## 🚀 Setup

### 1. Create and activate the virtual environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Configure the API key

Create a `.env` file in the project root:

```text
GEMINI_API_KEY=your_api_key_here
```

Do not commit your API key to GitHub.

## ▶️ Run the Application

From the project directory:

```powershell
python src\main.py
```

Paste resume text into the terminal and press Enter twice when finished.

## 🧪 Testing

The application was tested with multiple resume inputs.

### Test 1 — Complete Resume

The extractor successfully identified:

- Candidate name
- Email
- Phone
- Job title
- Experience
- Skills

### Test 2 — Different Candidate

A second resume with a different job title, experience level, and skill set was successfully processed.

### Test 3 — Missing Information

A resume without email and phone information was also processed successfully.

Missing optional fields were returned as:

```json
{
    "email": null,
    "phone": null
}
```

## 📋 Example Output

```json
{
    "name": "Priya Nair",
    "email": null,
    "phone": null,
    "job_title": "Junior Python Developer",
    "experience_years": 1.0,
    "skills": [
        "Python",
        "Django",
        "Git",
        "MySQL"
    ]
}
```

## 🎯 Key Learning Outcomes

This project demonstrates:

- LLM-based information extraction
- Prompt engineering
- Structured JSON generation
- Pydantic data validation
- Gemini API integration
- Environment variable management
- Error handling
- Testing with different input scenarios

## 🔐 Security

API credentials are stored in a `.env` file and excluded from version control using `.gitignore`.

Never upload your Gemini API key to GitHub.

## 👩‍💻 Internship Task

**Datheon Internship — Python + Generative AI & LangChain**

**Task:** Structured LLM Prompt Pipeline & JSON Extractor