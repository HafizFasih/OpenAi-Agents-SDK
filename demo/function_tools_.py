from agents import function_tool, FunctionTool, Agent, RunContextWrapper
from rich import print
import asyncio
import json

@function_tool
def add(a: int, b: int):
    return a + b

# print(add)

# my_dict={"a": 3, "b": 33}
# str_dict=json.dumps(my_dict)

# print(type(json.loads(str_dict)))

async def main():
    result = await add.on_invoke_tool(
        RunContextWrapper(
            context=None
        ),
        '{"a": 10, "b": 29}'
    )   
    print(result)

asyncio.run(main())