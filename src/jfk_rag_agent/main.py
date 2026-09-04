from dotenv import load_dotenv
from agents import Agent, Runner

from jfk_rag_agent.retrieval import search_jfk_documents


def main() -> None:
    load_dotenv()

    agent = Agent(
        name="JFK Research Agent",
        model="gpt-4o-mini",
        instructions="""
        You are a research assistant specializing in the JFK files.

        For questions about the JFK documents, always use the
        search_jfk_documents tool before answering.

        Base your answer only on evidence returned by the tool.

        When presenting documents:
        - Do not repeat the same document.
        - Only include documents that are clearly relevant to the question.
        - Include the filename and source URL.
        - Briefly explain why each document is relevant.
        - Do not invent dates, names, facts, or document details that are not
          present in the retrieved content.
        - If the retrieved evidence is weak or incomplete, say so.

        Prefer a concise, evidence-based answer over a long response.
        """,
        tools=[search_jfk_documents],
    )

    question = input("Ask a question about the JFK files: ")
    result = Runner.run_sync(
        agent,
        question,
    )

    print(result.final_output)


if __name__ == "__main__":
    main()