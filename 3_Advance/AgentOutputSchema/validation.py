from agents import AgentOutputSchema
from pydantic import BaseModel
from rich import print
import json

class UserInfo(BaseModel):
    name: str
    age: int

output_schema=AgentOutputSchema(UserInfo)
user_obj={"name": "Muhammad Fasih", "age": 10}
user_obj_str=json.dumps(user_obj)
#! Backend ma ese hi validate kia jata ha output ko
#! source: _run_impl -> RunImpl (class) -> execute_tools_and_side_effects (method)
final_obj=output_schema.validate_json(user_obj_str)
print(final_obj)