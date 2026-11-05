# Task 4 – Interactive Full-Stack AI Chatbot with Streamlit

## 1. Project Overview

This project implements an interactive AI-powered chatbot using Streamlit, LangChain, and Google Gemini. It provides a browser-based conversational interface with conversation memory, real-time response streaming, and multiple AI tools.

## 2. Objectives

- Develop an interactive chatbot using Streamlit.
- Implement conversation memory to retain previous messages.
- Display AI responses progressively using streaming.
- Maintain chat history during the session.
- Provide an option to clear conversation history.
- Integrate multiple AI tools for practical tasks.

## 3. Technologies Used

- Python
- Streamlit
- LangChain
- Google Gemini API
- DuckDuckGo Search
- python-dotenv

## 4. Features

### Interactive Chat Interface
Provides a user-friendly browser-based chatbot using Streamlit chat components.

### Conversation Memory
Uses Streamlit session state and conversation context to remember previous messages and answer follow-up questions.

### Real-Time Streaming
Displays generated AI responses progressively using LangChain streaming and Streamlit.

### Chat History
Maintains previous user and assistant messages during the active session.

### Clear Chat
Allows users to clear the current conversation using a sidebar button.

### AI Tools Integration
The chatbot supports three tools:

1. **Web Search:** Searches the internet using DuckDuckGo.
2. **Calculator:** Performs mathematical calculations.
3. **Local File Reader:** Reads supported local documents.

## 5. Project Structure

```text
Datheon Task 4 - Interactive Full-Stack AI Chatbot with Streamlit/
│
├── documents/
│   └── sample.txt
│
├── src/
│   ├── __init__.py
│   ├── agent.py
│   └── tools.py
│
├── app.py
├── requirements.txt
├── README.md
└── .env
```

Note: The `.env` file contains the API key and must not be uploaded to GitHub.

## 6. Installation and Execution

### Step 1: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Configure API key

Create a `.env` file and add:

```text
GEMINI_API_KEY=your_api_key_here
```

### Step 3: Run the application

```bash
streamlit run app.py
```

### Step 4: Open the application

The chatbot opens in the browser, usually at:

```text
http://localhost:8501
```

## 7. Testing

The following tests were performed:

| Test | Expected Result | Status |
|---|---|---|
| Mathematical calculation | Correct result | Passed |
| Web search | Search results | Passed |
| Local file reading | Document content | Passed |
| Conversation memory | Remembers previous questions | Passed |
| Response streaming | Progressive response display | Passed |
| Chat history | Previous messages visible | Passed |
| Clear chat | Conversation cleared | Passed |

## 8. Conclusion

The Interactive Full-Stack AI Chatbot successfully demonstrates conversational AI using Streamlit, LangChain, and Google Gemini. It combines conversation memory, response streaming, chat history, session management, and external tools to provide an interactive AI assistant.