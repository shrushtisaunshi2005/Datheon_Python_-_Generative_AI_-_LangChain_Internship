# Document Q&A Assistant with RAG & Vector Embeddings

## Project Overview
The Document Q&A Assistant is an AI-powered application that allows users to upload documents and ask questions about their content.

It uses Retrieval-Augmented Generation (RAG), vector embeddings, ChromaDB and Google's Gemini API to retrieve relevant information and generate context-based answers.

## Features
- Upload multiple documents.
- Supports PDF, DOCX, TXT, MD, XLSX, CSV and PPTX formats.
- Extracts text from uploaded documents.
- Splits documents into smaller chunks.
- Generates vector embeddings.
- Stores embeddings using ChromaDB.
- Retrieves relevant information using similarity search.
- Generates answers using Google Gemini.
- Displays source document references.
- Interactive Streamlit user interface.

## Technologies Used
- Python
- Streamlit
- LangChain
- Google Gemini API
- Google Generative AI Embeddings
- ChromaDB
- Vector Embeddings
- PyPDF
- Python-docx
- Pandas
- OpenPyXL
- Python-pptx

## Project Structure

```text
Datheon Task 2 - Document Q&A Assistant with RAG & Vector Embeddings/
│
├── documents/
│   └── sample.txt
│
├── src/
│   ├── main.py
│   ├── app.py
│   ├── document_loader.py
│   ├── embeddings.py
│   └── rag_pipeline.py
│
├── vector_store/
├── .env
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository.

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

2. Navigate to the Task 2 folder.

3. Install the dependencies.

```bash
pip install -r requirements.txt
```

4. Create a `.env` file and add your Gemini API key.

```env
GEMINI_API_KEY=your_api_key_here
```

## Run the Application

Start the Streamlit application:

```bash
streamlit run src/app.py
```

Open the local URL displayed in the terminal.

## How It Works

1. Upload documents through the Streamlit interface.
2. Extract text from the uploaded documents.
3. Split the extracted text into smaller chunks.
4. Generate vector embeddings for the chunks.
5. Store the embeddings in ChromaDB.
6. Retrieve relevant chunks using similarity search.
7. Send the retrieved context and question to Gemini.
8. Display the generated answer with source references.

## Expected Output

The application provides:
- Answers based on uploaded documents.
- Relevant source document references.
- An interactive question-and-answer interface.

## Conclusion

This project demonstrates how Retrieval-Augmented Generation can be used to build an intelligent document question-answering system. It combines document processing, vector search and generative AI to provide relevant, context-based answers.