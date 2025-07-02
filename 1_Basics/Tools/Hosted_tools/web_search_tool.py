from agents import Agent, Runner, WebSearchTool
import asyncio

agent = Agent(
    name="Assistant",
    instructions="You are an helpful assistant",
    tools=[WebSearchTool()],
)

async def main():
    result = await Runner.run(agent, "Compare the features and prices of latest iphone and latest samsung mobile.")
    print(result.final_output)

asyncio.run(main())