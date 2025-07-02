from agents import Agent, Runner, set_tracing_disabled, AsyncOpenAI, OpenAIChatCompletionsModel, RunResult
from dotenv import load_dotenv
from rich import print
import os, asyncio

set_tracing_disabled(disabled=True)
load_dotenv()

API_KEY=os.environ.get("GEMINI_API_KEY")

model=OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=AsyncOpenAI(
        api_key=API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
)
spanish_translator=Agent(
    name="Spanish Translator",
    instructions="You can translate text into spanish",
    model=model
)

async def extract_output(result: RunResult) -> str:
    print(result)
    return "Hello how are you ?"

agent=Agent(
    name="Asisstant",
    instructions="You are a helpful assistant",
    tools=[
        spanish_translator.as_tool(
            tool_name="spanish_translator",
            tool_description="Translate text into spanish",
            custom_output_extractor=extract_output
        )
    ],
    # tool_use_behavior="stop_on_first_tool",
    model=model
)

async def main():
    # result= await Runner.run(
    #     starting_agent=agent,
    #     input="Translate 'Hello' to spanish"
    # )

    # print(result.final_output)
    tools=await agent.get_all_tools()
    print(tools)

asyncio.run(main())