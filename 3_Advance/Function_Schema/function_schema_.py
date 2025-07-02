from agents.function_schema import function_schema
from rich import print
import inspect

def add(a: int, b: int) -> int:
    """Add two numbers

    Args:
        a: first number
        b: second number
        
    Returns:
        int: The sum of the two numbers.
    """

    return a + b

#! function_schema takes 6 properties:
#* name_override (Required)
#* description_override
#* use_docstring_info
#* docstring_style
#* strict_json_schema

fs = function_schema(
    func=add,
    name_override="addition",
    description_override="Sum two numbers",
    docstring_style="google",
    use_docstring_info=True,
    strict_json_schema=True,
)

#! Function Schema returns instance of FunctionSchema which contains 7 attributes
#? 1 name

#? 2 description

#? 3 params_pydantic_model (ye ek class ha jismy tool k parameters ko as an attribute treat kia jata ha)
#* Code Example
params_pydantic_model_instance = fs.params_pydantic_model(a=10, b=20)
print(params_pydantic_model_instance) #* OUTPUT: addition_args(a=10, b=20)

#? 4 params_json_schema

#? 5 signature
#* Code Example
sig = inspect.signature(add)
print(sig)

#? 6 takes_context (ye ek bool value ha agar hamary tool ma context (RunContextWrapper) as a parameter accept ho rha hoga to ye True hogi wrna False)

#? 7 strict_json_schema

print(fs)
#! OUTPUT
"""
FuncSchema(
    name='add',
    description='Add two numbers',
    params_pydantic_model=<class 'agents.function_schema.add_args'>,
    params_json_schema={
        'properties': {
            'a': {'description': 'first number', 'title': 'A', 'type': 'integer'},
            'b': {'description': 'second number', 'title': 'B', 'type': 'integer'}
        },
        'required': ['a', 'b'],
        'title': 'add_args',
        'type': 'object',
        'additionalProperties': False
    },
    signature=<Signature (a: int, b: int) -> int>,
    takes_context=False,
    strict_json_schema=True
)
"""
    