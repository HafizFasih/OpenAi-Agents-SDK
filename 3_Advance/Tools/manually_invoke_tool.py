from agents import function_tool, RunContextWrapper
import json
import asyncio

#! VERY IMPORTANT FUNCTION (_on_invoke_tool_impl) MUST OVERVIEW ONCE

@function_tool
def add(a: int, b: int) -> int:
    """Add two numbers

    Args:
        a: first number
        b: second number
        
    Returns:
        int: The sum of the two numbers.
    """

    return a + b

json_data = json.dumps({"a": 10, "b": 20})

async def main():
    result = await add.on_invoke_tool( #type: ignore
        ctx=RunContextWrapper(
            context=None, 
        ),
        input=json_data
    )
    print(result)

asyncio.run(main())