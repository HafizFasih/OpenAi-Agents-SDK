from agents import function_tool
from rich import print

@function_tool
def add(a: int, b: int) -> int: 
    """Add two numbers

    Args:
        a: first number
        b: second number
    """
    return a + b

#? @function_tool decorator ka kaam just itna ha k hamara function k as a parameter accept kre or FunctionTool ka instance return kre

#! @function_tool k decorator ne FunctioTool ka ek instance return kia ha jismy 5 propertoes hain 
print(add)
#! Output: Instance of FunctionTool

#! Tool ka name (Very Important)
print(add.name)
#! Output: add

#! Tool ki description agar di gai ho wrna None
print(add.description)
#! Output: Add two numbers

#! Tool k parameters ka JSON Schema (Very Important)
print(add.params_json_schema)
#! Output: 
#! {
#!     'properties': {
#!       # 'a': {'description': 'first number', 'title': 'A', 'type': 'integer'},
#!       # 'b': {'description': 'second number', 'title': 'B', 'type': 'integer'}
#!     },
#!     'required': ['a', 'b'],
#!     'title': 'add_args',
#!     'type': 'object',
#!     'additionalProperties': False
#! }

#! Ek bool value k kia strict_json_schema hona chahye ya nhi (default=True)
print(add.strict_json_schema)
#! True

#! ismy hamara asal function hota ha hamary case ma 'add' function (Very Important)
print(add.on_invoke_tool)
#! Hamara real function


