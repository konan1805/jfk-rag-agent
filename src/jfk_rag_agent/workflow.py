from agents import (
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered,
    Runner,
)

from jfk_rag_agent.agents.triage_agents import triage_agent


def ask_jfk(question: str) -> str:
    try:
        result = Runner.run_sync(
            triage_agent,
            question,
        )

        return result.final_output

    except InputGuardrailTripwireTriggered:
        return (
            "This application is designed specifically for "
            "questions about the JFK assassination and related records."
        )

    except OutputGuardrailTripwireTriggered:
        return (
            "The answer could not be returned because it did not pass "
            "the JFK evidence and source validation checks."
        )