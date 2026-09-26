import os

from dotenv import load_dotenv
from kartify.agent.OrderAgent import run_chatbot


load_dotenv()


def main() -> None:
    print("Hello")
    # Storing API credentials in environment variables
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    os.environ["OPENAI_BASE_URL"] = os.getenv("OPENAI_BASE_URL")
    run_chatbot()

if __name__ == "__main__":
    main()
