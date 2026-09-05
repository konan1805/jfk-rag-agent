from dotenv import load_dotenv
from jfk_rag_agent.workflow import ask_jfk




def main() -> None:
    load_dotenv()

    question = input("Ask a question about the JFK files: ")
    result = ask_jfk(question)

    print("\nAnswer: ")
    print(result)


if __name__ == "__main__":
    main()