#type: ignore
from agents.models.openai_responses import Converter
from agents import AgentOutputSchemaBase, AgentOutputSchema, Agent, Tool, Handoff, handoff, function_tool
from pydantic import BaseModel
from typing import Any, List
from rich import print

tool_list: List[Tool] = []
handsoff_list: List[Handoff] = []

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

agent=Agent(
    name="Math expert",
    instructions="you are good at maths",
    handoff_description="A perfect math teacher"
)

handsoff_list.append(handoff(agent))

@function_tool
def add(a: int, b: int) ->int:
    """Add two numbers

    Args:
        a: first number
        b: second number
    """
    return a + b

tool_list.append(add)

#! METHOD 1
unknown = Converter().convert_tool_choice('auto')
print(unknown)

#! METHOD 2
unknown = Converter.get_response_format(
    output_schema=AgentOutputSchema(output_type=Developer) 
)
print(unknown)

#! METHOD 3
unknown = Converter().convert_tools(
    handoffs=handsoff_list,
    tools=tool_list
)
print(unknown)
