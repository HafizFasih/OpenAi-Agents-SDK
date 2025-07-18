from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled, function_tool, AgentOutputSchemaBase
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Any
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

class CustomOutputSchema(AgentOutputSchemaBase):
    def is_plain_text(self) -> bool:
        return False
    
    def name(self) -> str:
        return "CustomSchema"
    
    def json_schema(self) -> dict[str, Any]:
        return Developer.model_json_schema()
    
    def is_strict_json_schema(self) -> bool:
        return True
    
    def validate_json(self, json_str: str) -> Any:
        return json_str


agent = Agent(
    name="Assistant",
    instructions="You can extract out from the statement that wether the person talking is technical or not and wether the statement is coding related or not",
    output_type=CustomOutputSchema(),
    model=model
)

result = Runner.run_sync(
    starting_agent=agent,
    input="Tell me about web development",
)

print(result.final_output)
print(agent.output_type)