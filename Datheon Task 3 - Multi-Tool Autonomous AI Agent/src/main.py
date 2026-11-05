
from pathlib import Path
from dotenv import load_dotenv

# Load the API key from the project's .env file
PROJECT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_DIR / ".env")

from agent import build_agent, ask_agent


def main():
    print("\n========================================")
    print("   MULTI-TOOL AUTONOMOUS AI AGENT")
    print("========================================")
    print("Available tools:")
    print("1. DuckDuckGo Web Search")
    print("2. Python Calculator")
    print("3. Local File Reader")
    print("\nType 'exit' to stop the agent.")
    print("----------------------------------------")

    try:
        agent = build_agent()
        print("\nAI Agent is ready!")

        while True:
            question = input("\nYou: ").strip()

            if question.lower() in ["exit", "quit"]:
                print("Agent stopped. Goodbye!")
                break

            if not question:
                continue

            print("\nAgent is thinking...")

            answer = ask_agent(agent, question)

            print("\nAgent:", answer)

    except Exception as error:
        print(f"\nError: {error}")


if __name__ == "__main__":
    main()
