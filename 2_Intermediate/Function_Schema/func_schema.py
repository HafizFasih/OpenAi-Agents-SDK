from agents.function_schema import function_schema, generate_func_documentation
from rich import print
from openai import func

def addition(a: int, b: int) -> int:
    """Add two numbers.

    Args:
        a (int): The first number.
        b (int): The second number.

    Returns:
        int: The sum of the two numbers.
    """
    return a + b

func_schema=function_schema(
    func=addition,
    description_override="Sum two numbers",
    name_override="sum",
    docstring_style="google",
    strict_json_schema=True,
    use_docstring_info=True
)

print(func_schema)

