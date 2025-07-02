from agents import Agent
from agents.extensions.handoff_prompt import (
    RECOMMENDED_PROMPT_PREFIX, 
    prompt_with_handoff_instructions
)

billing_agent = Agent(
    name="Billing agent",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
    <Fill in the rest of your prompt here>.""",
)

billing_agent = Agent(
    name="Billing agent",
    instructions=prompt_with_handoff_instructions(
        """<Fill in the rest of your prompt here>."""
    )
)