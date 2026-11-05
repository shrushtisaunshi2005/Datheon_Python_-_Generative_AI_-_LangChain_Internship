
from pathlib import Path

from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI

from embeddings import create_vector_store, split_documents
from document_loader import load_documents


def build_rag_pipeline(
    file_paths: list[str],
    persist_directory: str,
) -> Chroma:
    """Load, split, embed, and store documents for retrieval."""

    documents = load_documents(file_paths)
    chunks = split_documents(documents)

    return create_vector_store(
        chunks=chunks,
        persist_directory=persist_directory,
    )


def answer_question(
    vector_store: Chroma,
    question: str,
    k: int = 4,
) -> dict:
    """
    Answer a question using retrieved document chunks.
    Return the answer and source citations.
    """

    if not question.strip():
        raise ValueError("Please enter a question.")

    retrieved_docs = vector_store.similarity_search(
        question,
        k=k,
    )

    if not retrieved_docs:
        return {
            "answer": "I couldn't find relevant information in the uploaded documents.",
            "sources": [],
        }

    context_parts = []
    sources = []

    for document in retrieved_docs:
        source = Path(
            document.metadata.get("source", "Unknown source")
        ).name
        page = document.metadata.get("page")

        if page is not None:
            citation = f"{source}, page {page}"
        else:
            citation = source

        context_parts.append(
            f"[Source: {citation}]\n{document.page_content}"
        )

        source_info = {
            "source": source,
            "page": page,
        }

        if source_info not in sources:
            sources.append(source_info)

    context = "\n\n".join(context_parts)

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.8-flash",
        temperature=0,
    )

    prompt = f"""
You are a document question-answering assistant.

Answer the user's question using ONLY the supplied context.
If the answer is not present in the context, clearly say that you
could not find the answer in the uploaded documents.
Do not invent facts or citations.
Mention relevant source filenames and page numbers in your answer.

Context:
{context}

Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)

    if isinstance(response.content, str):
        answer_text = response.content
    else:
      answer_text = "\n".join(
        block["text"]
        for block in response.content
        if isinstance(block, dict) and block.get("type") == "text"
    )

    return {
    "answer": answer_text,
    "sources": sources,
}