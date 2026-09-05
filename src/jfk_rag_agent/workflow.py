from collections.abc import AsyncIterator

from openai.types.responses import ResponseTextDeltaEvent

from agents import (
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered,
    Runner,
)

from jfk_rag_agent.agents.triage_agents import triage_agent


async def stream_jfk(question: str) -> AsyncIterator[str]:
    accumulated_text = ""

    try:
        result = Runner.run_streamed(
            triage_agent,
            input=question,
        )

        async for event in result.stream_events():
            if (
                event.type == "raw_response_event"
                and isinstance(event.data, ResponseTextDeltaEvent)
            ):
                accumulated_text += event.data.delta
                yield accumulated_text

    except InputGuardrailTripwireTriggered:
        yield (
            "This application is designed specifically for "
            "questions about the JFK assassination and related records."
        )

    except OutputGuardrailTripwireTriggered:
        yield (
            "The answer could not be returned because it did not pass "
            "the JFK evidence and source validation checks."
        )