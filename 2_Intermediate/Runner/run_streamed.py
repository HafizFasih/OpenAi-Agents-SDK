from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled, enable_verbose_stdout_logging, function_tool, ModelSettings
from openai.types.responses import ResponseTextDeltaEvent
from dotenv import load_dotenv
from rich import print
import os, asyncio, random

load_dotenv()
set_tracing_disabled(disabled=True)
# enable_verbose_stdout_logging()

API_KEY=os.environ.get("GEMINI_API_KEY")

model=OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=AsyncOpenAI(
        api_key=API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai"
    )
)

@function_tool
def get_length() -> str:
    """Return's the length of the story"""
    return f"{random.randint(0, 15)} lines"

agent=Agent(
    name="Story Teller",
    instructions="You are good at story teller. Your speciality is that you can engage people by your intersting stories."
    "First CALL TOOL to get the lenth then write story according to it"
    ,
    model=model,
    tools=[get_length],
    model_settings=ModelSettings(
        tool_choice="required"
    )
)

async def main():
    result = Runner.run_streamed(
        starting_agent=agent,
        input="Tell me the intersting story about acient civilization of particular length"
    )
    async for event in result.stream_events():
        if event.type == "raw_response_event":
            pass
        elif event.type == "agent_updated_stream_event":
            print(f"Agent updated: {event.new_agent.name}")
        elif event.type == "run_item_stream_event":
            if event.item.type == "tool_call_item":
                print("Tool has been called")
            elif event.item.type == "tool_call_output_item":
                print(f"Tool has generated output: {event.item.output}")
            elif event.item.type == "message_output_item":
                print(f"Output message is created: \n'{event.item.raw_item.content[0].text}'")
            else:
                pass
        
asyncio.run(main())