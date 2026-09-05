from agents import Agent
from jfk_rag_agent.retrieval import search_jfk_documents
from jfk_rag_agent.agents.evidence_agent import evidence_agent
from jfk_rag_agent.guardrails.output_guardrail import jfk_output_guardrail

research_agent = Agent(
    name="JFK Research Agent",
    handoff_description=(
        "Specialist for researching questions about the JFK assassination "
        "and JFK archival documents."
    ),
    model="gpt-5.4-mini",
    instructions="""
    You are a research assistant specializing in the JFK assassination files.

    For JFK research questions, follow this workflow:

    1. ALWAYS use search_jfk_documents first to retrieve relevant archival evidence.
    2. ALWAYS send the retrieved evidence to analyze_jfk_evidence.
    3. Use the evidence analyst's findings to construct the final answer.

    Base your answer only on evidence returned by the tools.

    When presenting documents:
    - Do not repeat the same document.
    - Only include documents that are clearly relevant.
    - Include the filename and source URL.
    - Briefly explain why each document is relevant.
    - Distinguish documented facts from interpretations.
    - Do not invent facts not supported by the retrieved evidence.
    - If the evidence is incomplete or contradictory, clearly say so.
    """,
    tools=[
        search_jfk_documents,
        evidence_agent.as_tool(
            tool_name="analyze_jfk_evidence",
            tool_description=(
                "Analyze retrieved JFK document evidence and identify "
                "supported facts, contradictions, uncertainty, and limitations."
            ),
        ),
    ],
    output_guardrails=[jfk_output_guardrail],
)