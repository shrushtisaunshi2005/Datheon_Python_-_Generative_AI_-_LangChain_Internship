
import os
import tempfile
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from document_loader import SUPPORTED_EXTENSIONS, load_documents
from embeddings import split_documents, create_vector_store
from rag_pipeline import answer_question

PROJECT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_DIR / ".env")

st.set_page_config(
    page_title="Document Q&A Assistant",
    page_icon="📚",
    layout="wide",
)

st.title("📚 Document Q&A Assistant")
st.write("Upload documents and ask questions using RAG.")

if not os.getenv("GEMINI_API_KEY"):
    st.error("GEMINI_API_KEY is missing. Please check your .env file.")
    st.stop()

uploaded_files = st.file_uploader(
    "Upload your documents",
    type=[ext.lstrip(".") for ext in sorted(SUPPORTED_EXTENSIONS)],
    accept_multiple_files=True,
)

if uploaded_files:
    if st.button("Process Documents"):
        all_documents = []

        with st.spinner("Reading your documents..."):
            try:
                for uploaded_file in uploaded_files:
                    suffix = Path(uploaded_file.name).suffix.lower()

                    with tempfile.NamedTemporaryFile(
                        delete=False, suffix=suffix
                    ) as temp_file:
                        temp_file.write(uploaded_file.getvalue())
                        temp_path = temp_file.name

                    try:
                        documents = load_documents([temp_path])
                        for document in documents:
                            document.metadata["source"] = uploaded_file.name
                        all_documents.extend(documents)
                    finally:
                        Path(temp_path).unlink(missing_ok=True)

                chunks = split_documents(all_documents)

                if not chunks:
                    st.error("No readable text was found in the uploaded files.")
                    st.stop()

                vector_store = create_vector_store(
                    chunks=chunks,
                    persist_directory=str(
                        Path(tempfile.mkdtemp()) / "vector_store"
                    ),
                )

                st.session_state["vector_store"] = vector_store
                st.session_state["processed_files"] = [
                    file.name for file in uploaded_files
                ]
                st.session_state["chat_history"] = []
                st.success("Documents processed successfully!")

            except Exception as error:
                st.error(f"Could not process documents: {error}")

if "vector_store" in st.session_state:
    st.subheader("Ask questions")

    for item in st.session_state.get("chat_history", []):
        with st.chat_message(item["role"]):
            st.write(item["content"])

    question = st.chat_input("Ask a question about your documents")

    if question:
        st.session_state["chat_history"].append(
            {"role": "user", "content": question}
        )

        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):
            with st.spinner("Searching documents and generating an answer..."):
                try:
                    result = answer_question(
                        st.session_state["vector_store"], question
                    )
                    st.write(result["answer"])

                    if result["sources"]:
                        st.caption("Sources")
                        for source in result["sources"]:
                            citation = source["source"]
                            if source.get("page") is not None:
                                citation += f", page {source['page']}"
                            st.write(f"- {citation}")

                    st.session_state["chat_history"].append(
                        {"role": "assistant", "content": result["answer"]}
                    )

                except Exception as error:
                    st.error(f"Could not answer the question: {error}")

    with st.sidebar:
        st.subheader("Processed documents")
        for filename in st.session_state.get("processed_files", []):
            st.write(f"📄 {filename}")
