 # type: ignore
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled
from dotenv import load_dotenv
from pydantic import BaseModel
import os, asyncio

load_dotenv()
set_tracing_disabled(disabled=True)

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise KeyError("Error 405: Does not found an api key") 

client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client,
)

async def call_agent_without_output_type():
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant", 
        model=model
    )
    result = await Runner.run(agent, "Hello")
    #! In this case the final_output would be of type str
    print(f"\nType of result.final_output is {type(result.final_output)}")
    print(f"result.final_output: {result.final_output}")


async def call_agent_with_output_type():
    class OutputType(BaseModel):
        is_math_relevant_question: bool 
        question: str
        reason: str

    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant", 
        model=model,
        output_type=OutputType
    )
    result = await Runner.run(agent, "Hello")
    #! In this case the final_output would be of type obj
    print(f"\nType of result.final_output is {type(result.final_output)}")
    print(f"result.final_output:\nis_math_relevant_question: {result.final_output.is_math_relevant_question}\nquestion: {result.final_output.question}\nreason: {result.final_output.reason}")


asyncio.run(call_agent_without_output_type())
asyncio.run(call_agent_with_output_type())