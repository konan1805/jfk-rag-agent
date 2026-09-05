from pydantic import BaseModel

from agents import (
    Agent,
    GuardrailFunctionOutput,
    RunContextWrapper,
    Runner,
)
from agents.decorators import output_guardrail


class JFKOutputCheck(BaseModel):
    grounded: bool
    has_sources: bool
    unsupported_claims: bool
    reasoning: str


output_guardrail_agent = Agent(
    name="JFK Output Guardrail",
    model="gpt-4o-mini",
    instructions="""
    You evaluate final answers produced by a JFK archival research agent.

    Check whether the answer satisfies these requirements:

    1. The answer should be grounded in JFK archival evidence.
    2. Factual claims should not go beyond the evidence.
    3. The answer should include source references such as filenames
       and/or source URLs when presenting factual findings.
    4. The answer should clearly acknowledge uncertainty when the
       available evidence is incomplete or ambiguous.

    Set:
    - grounded = true when the answer appears evidence-based.
    - has_sources = true when useful document references are included.
    - unsupported_claims = true when the answer makes claims that appear
      unsupported, speculative, exaggerated, or invented.

    Return a concise explanation in reasoning.
    """,
    output_type=JFKOutputCheck,
)


@output_guardrail
async def jfk_output_guardrail(
    ctx: RunContextWrapper[None],
    agent: Agent,
    output: str,
) -> GuardrailFunctionOutput:
    result = await Runner.run(
        output_guardrail_agent,
        f"""
        Evaluate this final JFK research answer:

        {output}
        """,
        context=ctx.context,
    )

    check = result.final_output

    print("\n[OUTPUT GUARDRAIL]")
    print(f"Grounded: {check.grounded}")
    print(f"Has sources: {check.has_sources}")
    print(f"Unsupported claims: {check.unsupported_claims}")
    print(f"Reason: {check.reasoning}\n")

    passed = (
        check.grounded
        and check.has_sources
        and not check.unsupported_claims
    )

    return GuardrailFunctionOutput(
        output_info=check,
        tripwire_triggered=not passed,
    )