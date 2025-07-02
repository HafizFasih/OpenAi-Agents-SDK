from agents import Agent, RunContextWrapper
from agents.handoffs import handoff
from rich import print
import asyncio
import json

handoff_agent=handoff(agent=Agent(name="Assistant"))

#! INVVOKING HANDOFF
async def main():
    result = await handoff_agent.on_invoke_handoff(
        ctx=RunContextWrapper(context=None),
        input_json=json.dumps({})
    )
    print(f"[blue]Returned agent:[/blue] ", result)

asyncio.run(main())