
import os
from pathlib import Path

from dotenv import load_dotenv

from rag_pipeline import answer_question, build_rag_pipeline

from document_loader import SUPPORTED_EXTENSIONS


# Locate the Task 2 project directory.
PROJECT_DIR = Path(__file__).resolve().parent.parent
DOCUMENTS_DIR = PROJECT_DIR / "documents"
VECTOR_STORE_DIR = PROJECT_DIR / "vector_store"

# Load the API key from the Task 2 .env file.
load_dotenv(PROJECT_DIR / ".env")


def main():
    print("=" * 60)
    print("Datheon Task 2: Document Q&A Assistant (RAG)")
    print("=" * 60)

    if not os.getenv("GEMINI_API_KEY"):
        print("\nError: GEMINI_API_KEY is missing.")
        print(f"Add it to: {PROJECT_DIR / '.env'}")
        return

    DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)

    file_paths = [
    str(path)
    for path in DOCUMENTS_DIR.iterdir()
    if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
]

    if not file_paths:
        print("\nNo supported documents found.")
        print(f"Add your documents to: {DOCUMENTS_DIR}")
        return

    try:
        print(f"\nFound {len(file_paths)} document(s).")
        print("Loading documents and building the vector store...")

        vector_store = build_rag_pipeline(
            file_paths=file_paths,
            persist_directory=str(VECTOR_STORE_DIR),
        )

        print("\nYour documents are ready!")
        print("Ask questions about them. Type 'exit' to quit.\n")

        while True:
            question = input("Your question: ").strip()

            if question.lower() in {"exit", "quit"}:
                print("Goodbye!")
                break

            if not question:
                print("Please enter a question.")
                continue

            print("\nSearching documents and generating an answer...")

            result = answer_question(vector_store, question)

            print("\nAnswer:")
            print(result["answer"])

            print("\nSources:")
            if result["sources"]:
                for source in result["sources"]:
                    citation = source["source"]

                    if source["page"] is not None:
                        citation += f", page {source['page']}"

                    print(f"- {citation}")
            else:
                print("- No sources found.")

            print()

    except Exception as error:
        print(f"\nAn error occurred: {error}")


if __name__ == "__main__":
    main()
