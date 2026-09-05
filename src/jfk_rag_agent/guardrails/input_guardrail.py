from pydantic import BaseModel

from agents import (
    Agent,
    GuardrailFunctionOutput,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
)
from agents.decorators import input_guardrail


class JFKInputCheck(BaseModel):
    is_jfk_related: bool
    reasoning: str


input_guardrail_agent = Agent(
    name="JFK Input Guardrail",
    model="gpt-5.4-mini",
    instructions="""
    Determine whether the user's question is relevant to research about:

    - President John F. Kennedy
    - the JFK assassination
    - Lee Harvey Oswald
    - Jack Ruby
    - CIA, FBI, Secret Service, or other government agencies connected
      to the JFK assassination
    - people, organizations, events, investigations, witnesses,
      intelligence activities, or documents related to the JFK case
    - the Warren Commission
    - JFK archival records or released government files

    A question can be relevant even if it does not explicitly contain
    the words "JFK" or "John F. Kennedy".

    For example:
    "Who was David Phillips?"
    can be relevant because David Atlee Phillips appears in JFK-related
    intelligence records.

    Mark clearly unrelated questions as not JFK-related.

    Examples of unrelated questions:
    - cooking recipes
    - general programming help
    - sports
    - unrelated historical events
    - general everyday questions

    Return your decision using the required structured output.
    """,
    output_type=JFKInputCheck,
)


@input_guardrail(run_in_parallel=False)
async def jfk_input_guardrail(
    ctx: RunContextWrapper[None],
    agent: Agent,
    input: str | list[TResponseInputItem],
) -> GuardrailFunctionOutput:
    result = await Runner.run(
        input_guardrail_agent,
        input,
        context=ctx.context,
    )

    check = result.final_output

    print("\n[INPUT GUARDRAIL]")
    print(f"JFK related: {check.is_jfk_related}")
    print(f"Reason: {check.reasoning}\n")

    return GuardrailFunctionOutput(
        output_info=check,
        tripwire_triggered=not check.is_jfk_related,
    )