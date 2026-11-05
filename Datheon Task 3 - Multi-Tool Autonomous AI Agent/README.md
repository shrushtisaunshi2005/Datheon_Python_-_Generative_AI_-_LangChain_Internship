# Task 3 – Multi-Tool Autonomous AI Agent

## Project Overview
This project implements an autonomous AI agent using Python, LangChain, and Google Gemini. The agent can understand user questions, select appropriate tools, and perform tasks automatically.

## Objectives
- Build an autonomous AI agent using LangChain.
- Integrate multiple external and local tools.
- Enable automatic tool selection.
- Provide an interactive Streamlit interface.

## Technologies Used
- Python
- LangChain
- Google Gemini
- DuckDuckGo Search
- Streamlit
- python-dotenv

## Tools Implemented

### 1. DuckDuckGo Web Search
Searches the internet and retrieves relevant information.

### 2. Python Calculator
Performs mathematical calculations using safe expression evaluation.

### 3. Local File Reader
Reads TXT, MD, and CSV files from the project's documents folder.

## Key Features
- Autonomous tool selection.
- Multi-step problem solving.
- Gemini-powered responses.
- Interactive Streamlit chat interface.
- Chat history and clear chat option.
- Actual tool execution history.

## Project Structure

```text
Datheon Task 3 - Multi-Tool Autonomous AI Agent/
│
├── app.py
├── requirements.txt
├── README.md
├── .env
│
├── documents/
│   └── sample.txt
│
└── src/
    ├── agent.py
    ├── main.py
    ├── tools.py
    └── __init__.py
```

## Installation

1. Clone the repository.
2. Navigate to the Task 3 folder.
3. Create and activate a Python virtual environment.
4. Install the dependencies:

```bash
pip install -r requirements.txt
```

5. Create a `.env` file and add your Gemini API key:

```env
GEMINI_API_KEY=your_api_key
```

## Run the Application

Run the Streamlit interface:

```bash
python -m streamlit run app.py
```

To run the console application:

```bash
python src/main.py
```

## Testing

The following tests were performed:

- Calculator: 25% of 800 = 200.
- File Reader: Retrieved the Machine Learning definition from sample.txt.
- Web Search: Retrieved information about LangChain.
- Multi-tool execution: Successfully processed a request involving all three tools.

## Conclusion

The project demonstrates how LangChain can be used to develop an autonomous AI agent that selects and uses multiple tools to solve real-world tasks through an interactive interface.