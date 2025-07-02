from rich import print

#* OpenAI Agents SDK use Python's inspect module to extract the function signature, along with griffe to parse docstrings and pydantic for schema creation.

#? griffe -> parse docstrings
#? inspect ->  function signature
#? pydantic -> schema creation

#!  GRIFEE TO GET FUNCTION DOCUMENTATION 
#* Example
from agents.function_schema import generate_func_documentation
def sum(a: int, b: int) -> int:
    """Add two numbers.

    Args:
        a (int): The first number.
        b (int): The second number.

    Returns:
        int: The sum of the two numbers.
    """
    return a + b

docs=generate_func_documentation(
    func=sum,
    style="google"
)
print(docs)

#! INSPECT TO GET THE SIGNATURE OF THE FUNCTION
#* Example
import inspect
sig = inspect.signature(sum)
print(sig)

#! PYDANTIC MODEL FOR SCHEMA CREATION
#* Example
from pydantic import BaseModel, Field, create_model
from typing import Any

fields: dict[str, Any] = {}

fields['a'] = ( int, Field(default_factory=dict, description="The first number") ) #type: ignore
fields['b'] = ( int, Field(default_factory=dict, description="The second number") ) #type: ignore

dynamic_model = create_model(f"{sum.__name__}_args",__base__=BaseModel, **fields)
json_schema = dynamic_model.model_json_schema()

#? Ye jo dynamic model ha basically ye wo class ha jo **kwargs ki shakal ma values get kregi or phr ek instance return kregi
print(dynamic_model)

#? Output: sum_args(a=10, b=10)
print(dynamic_model(a=10, b=10))
#! Agar dynamic_model ma galat keys ya extra keys insert ki jaye to ye error nh dega

#? Ye hamara main json_schema ha jo pydantic ko use kr ky baanaya gya ha.
#? backend pr SDK bh isi trah se cheezon ko handle kr rha hota ha
print(json_schema)
#? Output: 
"""
{
    'properties': {
        'a': {'description': 'The first number', 'title': 'A', 'type': 'integer'},
        'b': {'description': 'The second number', 'title': 'B', 'type': 'integer'}
    },
    'title': 'sum_args',
    'type': 'object'
}
"""