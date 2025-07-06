from agents import AgentOutputSchema
from rich import print
import json

#! ham ese direct dict ki is trah se type define nhi kr skty.
#! Is case ma UserError ayega.
agent_output = AgentOutputSchema(dict[str, str])
print(agent_output)

json_obj={"name": "Muhammad Fasih", "age": "10"}
json_obj_str=json.dumps(json_obj)
#! Backend ma ese hi validate kia jata ha output ko
#! source: _run_impl -> RunImpl (class) -> execute_tools_and_side_effects (method)
final_obj=agent_output.validate_json(json_obj_str)
print(final_obj)