from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled, function_tool
from dotenv import load_dotenv
from pydantic import BaseModel
from rich import print
import os

set_tracing_disabled(disabled=True)
load_dotenv()

API_KEY = os.environ.get("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

model = OpenAIChatCompletionsModel(
    openai_client=client,
    model="gemini-1.5-flash"
)

class Developer(BaseModel):
    is_coding_related: bool
    is_technical_person: bool
    reason: str

agent = Agent(
    name="Assistant",
    instructions="You can extract out from the statement that wether the person talking is technical or not and wether the statement is coding related or not",
    output_type=Developer,
    model=model
)

result = Runner.run_sync(
    starting_agent=agent,
    input="Tell me about web development",
)

# print(result.final_output)
# print(result.final_output_as(cls=Developer, raise_if_incorrect_type=False))
# print(result.context_wrapper)
# print(result.input_guardrail_results)
# print(result.new_items)
# print(result.raw_responses)
print(result.to_input_list())