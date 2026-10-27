from pathlib import Path

from file_parser import extract_text_from_file
from llm import extract_resume_data


def main():
    print("=== Datheon Task 1: Resume JSON Extractor ===")
    print("Supported files: .txt, .pdf, .docx\n")

    file_path = input("Enter the resume file path: ").strip()

    if not file_path:
        print("No file path provided.")
        return

    try:
        # Check that the file exists
        if not Path(file_path).exists():
            print(f"File not found: {file_path}")
            return

        # Extract text from the file
        print("\nReading resume...")
        input_text = extract_text_from_file(file_path)

        input_text = extract_text_from_file(file_path)

        # Clean extracted text before sending it to the LLM
        input_text = "\n".join(
        line.strip()
        for line in input_text.splitlines()
        if line.strip()
)

        if not input_text.strip():
            print("No readable text found in the file.")
            return

        # Send extracted text to Gemini
        print("Extracting structured information with Gemini...")
        result = extract_resume_data(input_text)

        # Display JSON result
        print("\n=== Extracted JSON ===")
        print(result.model_dump_json(indent=4))

    except ValueError as error:
        print("\nInput or configuration error:")
        print(error)

    except Exception as error:
        print("\nAn unexpected error occurred.")
        print(f"Error: {error}")


if __name__ == "__main__":
    main()