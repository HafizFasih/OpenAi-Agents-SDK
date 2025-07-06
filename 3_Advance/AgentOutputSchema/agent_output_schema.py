from agents import AgentOutputSchema
from pydantic import BaseModel
from rich import print
import json

class UserInfo(BaseModel):
    name: str
    age: int

output_schema=AgentOutputSchema(UserInfo)

#! AgentOutputSchema k total 5 methods hain
#! 1. name() -> str
print(output_schema.name())

#! 2. is_plain_text() -> bool
print(output_schema.is_plain_text())

#! 3. is_strict_json_schema -> bool
print(output_schema.is_strict_json_schema())

#! 4. json_schema() -> dict[str, any]
print(output_schema.json_schema())

#! 5. validate_json() -> Any
print(output_schema.validate_json('{"name": "Ali", "age": 1}'))

print(output_schema)
#! Output: 
"""
    AgentOutputSchema(
        output_type=<class '__main__.UserInfo'>,
        _type_adapter=TypeAdapter(UserInfo),
        _is_wrapped=False,
        _output_schema={
            'properties': {'name': {'title': 'Name', 'type': 'string'}, 'age': {'title': 'Age', 'type': 'integer'}},
            'required': ['name', 'age'],
            'title': 'UserInfo',
            'type': 'object',
            'additionalProperties': False
        },
        _strict_json_schema=True
    )
"""