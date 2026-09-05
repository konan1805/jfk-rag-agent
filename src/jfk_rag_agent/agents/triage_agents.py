from re import A
from agents import Agent
from jfk_rag_agent.guardrails.input_guardrail import jfk_input_guardrail

from jfk_rag_agent.agents.research_agents import research_agent

triage_agent = Agent(
    name="JFK Triage Agent",
    model="gpt-5.4-mini",
    instructions="""
    You are the entry-point agent for a JFK assassination research application.

    Your job is to determine whether the user's question is related to:
    - President John F. Kennedy
    - the JFK assassination
    - Lee Harvey Oswald
    - CIA, FBI, intelligence, or government records connected to the JFK case
    - people, events, organizations, or documents relevant to the JFK files

    If the question is relevant to JFK research, hand off the conversation
    to the JFK Research Agent.

    Do not attempt to perform JFK document research yourself.

    If the question is clearly unrelated to JFK research, politely explain
    that this application is designed specifically for questions about
    the JFK assassination and related records.
    """,
    handoffs=[research_agent],
    input_guardrails=[jfk_input_guardrail],
)