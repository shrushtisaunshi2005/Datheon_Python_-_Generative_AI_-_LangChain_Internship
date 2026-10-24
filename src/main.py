from llm import extract_resume_data
import time

def main():
    print("=== Datheon Task 1: Resume JSON Extractor ===")
    print("Paste the resume text below.")
    print("When finished, press Enter twice.\n")

    lines = []

    while True:
        line = input()

        if line == "":
            break

        lines.append(line)

    input_text = "\n".join(lines)

    if not input_text.strip():
        print("No text provided.")
        return

    try:
        result = extract_resume_data(input_text)

        print("\n=== Extracted Data ===")
        print(result.model_dump_json(indent=4))

    except ValueError as error:
        print("\nInput or configuration error:")
        print(error)

    except Exception as error:
        print("\nAn unexpected error occurred.")
        print(f"Error: {error}")


if __name__ == "__main__":
    main()