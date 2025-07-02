# type: ignore
from agents import FunctionTool, RunContextWrapper
from rich import print
from typing import Any
from pydantic import BaseModel, create_model, Field
import json

#! EASY METHOD TO MAKE CUSTOM TOOL
class ParamArgs(BaseModel):
    a: int
    b: int

async def add(ctx: RunContextWrapper, args: str) -> int:
    parse = ParamArgs.model_validate_json(args)
    return parse.a + parse.b

easy_custom_tool=FunctionTool(
    name="addition",
    description="Add two numbers",
    strict_json_schema=True,
    params_json_schema=ParamArgs.model_json_schema(),
    on_invoke_tool=add
)

print(easy_custom_tool)

#! HARD BUT CAN BE MADE DYNAMIC METHOD TO MAKE CUSTOM TOOL
async def sum(ctx: RunContextWrapper[Any], input: str) -> int:
    print("sum function is called")
    data = json.loads(input) if input else {}
    return data['a'] + data['b']

fields: dict[str, Any] = {}
fields["a"] = (int, Field(default_factory=dict, description="first number")) 
fields["b"] = (int, Field(default_factory=dict, description="second number")) 
dynamic_class = create_model(f"{sum.__name__}_args", __base__=BaseModel, **fields)
params_json_schema = dynamic_class.model_json_schema()

hard_custom_tool=FunctionTool(
    name="addition",
    description="Add two numbers",
    strict_json_schema=True,
    params_json_schema=params_json_schema,
    on_invoke_tool=sum
)

print(hard_custom_tool)


